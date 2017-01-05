from __future__ import print_function
from utils import genmaxent, words
import os
import math
import marisa_trie
import codecs
import sys
from itertools import chain
stdout = codecs.getwriter('utf-8')(sys.stdout)

def features(context):
    length = len(context)
    if length > 1:
        collocations = [':' + word for word in context[0:length-1]]
        return collocations + ['1' +context[-1]]
    elif length == 1:
        return ['1' + context[-1]]
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
                fs = features(words[0:i])
                map(lambda f: self.known_features.add(f), fs)
                self.known_outcomes.add(words[i])
                yield (fs, words[i])

    def _eval(self, context, outcome):
        return self._model.eval(context, outcome)

    def train(self, words_seq):
        data = self.gen_data(words_seq)
        data = chain([([], u'_unknown')], data)
        self._model.train(data, cutoff=1)

    def score(self, words, debug=False):
        log_p = 0
        words =  [u'_BOS'] + words + [u'_EOS']
        for i in range(1, len(words)):
            if words[i] in self.known_outcomes:
                outcome = words[i]
            else:
                outcome = u'_unknown'
            fs = [f for f in features(words[0:i]) if f in self.known_features]
            score = self._eval(fs, outcome)
            if debug:
                print(u','.join(fs), outcome, math.log(score), file=stdout)
            log_p = log_p + math.log(score)
        return log_p

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
        self.known_features = marisa_trie.Trie().mmap(os.path.join(path, 'known_features'))
        self.known_outcomes = marisa_trie.Trie().mmap(os.path.join(path, 'known_outcomes'))
