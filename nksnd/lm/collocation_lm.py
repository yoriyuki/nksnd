from __future__ import print_function
from utils import genmaxent, words
import os
import math
import marisa_trie
import codecs
import sys
from itertools import chain
from config import lmconfig
stdout = codecs.getwriter('utf-8')(sys.stdout)

def features(context):
    fs = ['0']
    for i in range(1, 1+lmconfig.max_depth):
        fs += [str(i) + word for word in context[-i:]]
    fs += [':' + word for word in context]
    return fs

def count_features(data):
    feature_count = {}
    for fs, outcome in data:
        for f in fs:
            if f in feature_count:
                feature_count[f] = feature_count[f]+1
            else:
                feature_count[f] = 1
    feature_set = {'0'}
    for f, c in feature_count.iteritems():
        if c > lmconfig.unknown_feature_threshold or f[0] == '1':
            feature_set.add(f)
    return feature_set

def replace_features(feature_set, fs0):
    fs = []
    for f in fs0:
        if f in feature_set:
            fs.append(f)
        else:
            fs.append(f[0] + '_')
    return fs

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
                self.known_outcomes.add(words[i])
                yield (fs, words[i])

    def _eval(self, context, outcome):
        return self._model.eval(context, outcome)

    def _eval_all(self, context):
        return self._model.eval_all(context)

    def train(self, words_seq):
        words_seq = ([u'_BOS'] + words + [u'_EOS'] for words in words_seq)
        data = self.gen_data(words_seq)
        unknown_fs = [str(i) + '_' for i in range(1, 1+lmconfig.max_depth)]
        data = list(chain([(unknown_fs + [':_', '0'], u'_unknown')], data))
        self.known_features = count_features(data)
        data = [(replace_features(self.known_features, fs), outcome) for (fs, outcome) in data]
        self._model.train(data, cutoff=1)

    def predict(self, words, n):
        words = [u'_BOS'] + words
        fs = replace_features(self.known_features, features(words))
        prediction = self._eval_all(fs)[0:n]
        return [(word.decode('utf-8'), self._eval(fs, word.decode('utf-8'))) for (word, p) in prediction]

    def score(self, words, debug=False):
        log_p = 0
        words =  [u'_BOS'] + words + [u'_EOS']
        for i in range(1, len(words)):
            if words[i] in self.known_outcomes:
                outcome = words[i]
            else:
                outcome = u'_unknown'
            fs = replace_features(self.known_features, features(words))
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
