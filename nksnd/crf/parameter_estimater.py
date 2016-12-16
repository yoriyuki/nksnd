import tqdm
import copy_reg
import types
import multiprocessing
import gc
from graph import graph as gr, forward_backward
from config import lmconfig, parallel_config
from utils import sparse_vector, words, numerics
from dictionaries import dict_dict

def chunking(chunk_size, stream):
    buf = []
    for e in stream:
        buf.append(e)
        if len(buf) >= chunk_size:
            ret = buf
            buf = []
            yield ret
# from stacoverflow:-)
def _pickle_method(m):
    if m.im_self is None:
        return getattr, (m.im_class, m.im_func.func_name)
    else:
        return getattr, (m.im_self, m.im_func.func_name)

copy_reg.pickle(types.MethodType, _pickle_method)

class CRFEsitimater:
    def __init__(self, known_words):
        self.dict = dict_dict.DictDict(known_words)
        self.known_words = known_words

    def _Phi(self, y):
        sv = sparse_vector.SparseVector({})
        sv.set(gr.BOS.word, 1)
        prev_word = gr.BOS.word
        for word in y:
            bigram_key = words.compose_bigram_key(prev_word, word)
            sv.set(bigram_key, sv.get(bigram_key) + 1)
            sv.set(word, sv.get(word) + 1)
            prev_word = word
        bigram_key = words.compose_bigram_key(prev_word, gr.EOS.word)
        sv.set(bigram_key, sv.get(bigram_key) + 1)
        sv.set(gr.EOS.word, 1)
        return sv

    def _compute_alpha_beta(self, graph):
        forward_backward.set_log_alpha(self.dict, graph)
        forward_backward.set_log_beta(self.dict, graph)

    def _logZ(self, graph):
        eos = graph.nodes_list[graph.x_length + 1][0]
        return eos.log_alpha

    def _logP(self, node, graph):
        logP = -self._logZ(graph)
        logP += node.weight
        logP += node.log_alpha + node.log_beta
        return logP

    def _logP2(self, node1, node2, graph):
        logP = -self._logZ(graph)
        logP += self.dict.get_bigram_weight(node1.deep, node2.deep)
        logP += node1.log_alpha + node2.log_beta
        return logP

    def _logExpectedPhi(self, graph):
        expected_phi = sparse_vector.SparseVector({})
        graph.nodes_list[0][0].expected_phi = expected_phi
        for end_pos in range(graph.x_length + 2):
            for node in graph.nodes_list[end_pos]:
                log_expected_phi = sparse_vector.SparseVector({})
                log_expected_phi.set(node.deep, self._logP(node, graph))
                for prev_node in graph.nodes_list[node.start_pos]:
                    bigram_key = words.compose_bigram_key(prev_node.deep, node.deep)
                    log_expected_phi.set(bigram_key,  numerics.logsumexp(log_expected_phi.get(bigram_key), self._logP2(prev_node, node, graph)))
                    log_expected_phi.logsumexp(prev_node.log_expected_phi)
                node.log_expected_phi = log_expected_phi
        return graph.nodes_list[graph.x_length + 1][0].log_expected_phi

    def gradient(self, pair):
        x, y = pair
        graph = gr.Graph(self.dict, x)
        self._compute_alpha_beta(graph)
        logZ = self._logZ(graph)
        Phi = self._Phi(y)
        return Phi.minusexp(self._logExpectedPhi(graph))

    def fit(self, data, data_size):
        chunk_size = parallel_config.chunk_size * parallel_config.processes
        chunked_data = chunking(chunk_size, data)
        with tqdm.tqdm(total=data_size) as pbar:
            for chunk in chunked_data:
                workers = multiprocessing.Pool(parallel_config.processes)
                gs = workers.imap(self.gradient, chunk, parallel_config.chunk_size)
                g = reduce(lambda g, g1: g.setsum(g1), gs)
                workers.close()
                workers.join()
                self.dict.fobos_update(g)
                pbar.update(chunk_size)
        self.dict.fobos_regularize()
