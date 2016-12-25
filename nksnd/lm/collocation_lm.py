from utils import genmaxent, words
import os
import math

def features(context, outcome):
    length = len(context)
    if length > 2:
        collocations = [':' + word for word in context[0:length-3]]
        return collocations + ['2' + context[-2], '1' + context[-1]]
    elif length == 2:
        return ['2' + context[0], '1' + context[1]]
    elif length == 1:
        return ['1' + context[0]]
    else:
        return []

class CollocationLM:

    def __init__(self, slm):
        self._model = genmaxent.GenMaxEntModel()
        self.known_features = set()
        self.known_outcomes = set()
        self.slm = slm

    def gen_data(self, words_seq):
        for words in words_seq:
            words =  [u'_BOS'] + words + [u'_EOS']
            for i in range(len(words)):
                fs = features(words[0:i-1], words[i])
                map(lambda f: self.known_features.add(f), fs)
                self.known_outcomes.add(words[i])
                yield (fs, words[i])

    def _eval(self, context, outcome):
        return self._model.eval(context, outcome)

    def train(self, words_seq):
        data = self.gen_data(words_seq)
        self._model.train(data, cutoff=1)

    def score(self, words):
        log_p = 0
        words =  [u'_BOS'] + words + [u'_EOS']
        for i in range(1, len(words) + 1):
            if self.known_outcomes(words[i]):
                fs = filter(lambda f: f in self.known_features, features(words[0:i-1], words[i]))
                p = p + math.log(self._eval(fs, words[i]))
            else:
                p = p + slm.get_bigram_weight(words[i-1], words[i])
        return p

    def save(self, path):
        param_filename = os.path.join(path, 'collocation_param')
        self._model.save(param_filename)
        marisa_known_fs = marisa_trie.Trie(self.known_features)
        marisa_known_fs.save(os.path.join(path, 'known_features'))
        marisa_known_outcomes = marisa_trie.Trie(self.known_outcomes)
        marisa_known_outcomes.save(os.path.join(path, 'known_outcomes'))

    def load(self, path):
        param_filename = os.path.join(path, 'collocation_param')
        self._model.load(param_filename)
        self.known_featuress = marisa_trie.Trie().mmap(os.path.join(path, 'known_features'))
        self.known_outcomes = marisa_trie.Trie().mmap(os.path.join(path, 'known_outcomes'))
