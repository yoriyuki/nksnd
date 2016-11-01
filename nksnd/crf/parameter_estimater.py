from graph import graph, forward_backward
from config import lmconfig
from utils import sparse_vector, words

#Use FOBOS
class SGD:
    def __init__(self, unigram, bigram):
        self.unigram_dict = unigram
        self.bigram_dict = bigram

    def _Phi(self, y):
        sv = SparseVector({})
        prev_word = BOS.bos_word
        sv.set(BOS.word) = sv.get(BOS.word) + 1
        for word in y:
            bigram_key = compose_bigram_key(prev_word, word)
            sv.set(bigram_key) = sv.get(bigram_key) + 1
            sv.set(word) = sv.get(word) + 1
            prev_word = word
        bigram_key = compose_bigram_key(prev_word, EOS.word)
        sv.set(bigram_key) = sv.get(bigram_key) + 1
        sv.set(EOS.word) = sv.get(EOS.word) + 1
        return sv

    

    def fit(data):
        for x, y in data:
