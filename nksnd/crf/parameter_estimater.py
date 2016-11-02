from graph import graph, forward_backward
from config import lmconfig
from utils import sparse_vector, words
from dictionaries import dict_dict

class Esitimater:
    def __init__(self, known_words):
        self.dict = DictDict(known_words)

    def _Phi(self, y):
        sv = SparseVector({})
        sv.set(BOS.word) = 1
        prev_word = BOS.bos_word
        for word in y:
            bigram_key = compose_bigram_key(prev_word, word)
            sv.set(bigram_key) = sv.get(bigram_key) + 1
            sv.set(word) = sv.get(word) + 1
            prev_word = word
        bigram_key = compose_bigram_key(prev_word, EOS.word)
        sv.set(bigram_key) = sv.get(bigram_key) + 1
        sv.set(EOS.word) = 1
        return sv

    def _compute_alpha_beta(self, graph):
        forward_backward.set_log_alpha(self.dict, graph)
        forward_backward.set_log_beta(self.dict, graph)

    def _logZ(self, graph):
        eos = graph.nodes_list[graph.x_length + 1][0]
        return eos.logalpha

    def _logP(self, node, graph):
        logP = -self._logZ(graph)
        logP += self.dict.get_unigram(node.word)
        logP += node.log_alpha + node.log_beta
        return logP

    def _logP2(self, node1, node2, graph):
        logP = -self._logZ(graph)
        logP += self.dict.get_bigram(node1.word, node2.word)
        logP += node1.log_alpha + node2.log_beta
        return logP

    def _logExpectedPhi(self, graph):
        expected_phi = SparseVector({})
        graph.nodes_list[0][0].expected_phi = expected_phi
        for end_pos in range(graph.x_length + 1):
            for node in graph.nodes_list[end_pos]:
                log_expected_phi = SparseVector({})
                log_expected_phi.set(node.word) = self._logP(node, graph)
                for prev_node in graph.nodes_list[node.start_pos]:
                    bigram_key = compose_bigram_key(prev_node.word, node.word)
                    log_expected_phi.set(bigram_key) = log_expected_phi.get(bigram_key).logsumexp(self._logP(prev_node, node))
                    log_expected_phi.logsumexp(prev_node.log_expected_phi)
                node.log_expected_phi = log_expected_phi
        return graph.nodes_list[graph.x_length + 1][0].log_expected_phi

    def fit(data):
        for x, y in data:
            graph = Graph(known_words, x):
            self.compute_alphe_beta(graph)
            logZ = self._logZ(graph)
            Phi = self._Phi(y)
            g = Phi.minusexp(self._logExpectedPhi(graph))
            self.dict.update(g)
