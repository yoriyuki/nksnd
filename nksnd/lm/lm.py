from __future__ import print_function
import collocation_lm
import codecs
import pickle
import os
import sys
import marisa_trie
from utils import words
from config import lmconfig, conversion_config, learn_config
from dictionaries import marisa_dict
from graph import graph, viterbi
from slm import stats

def concat(files):
    for file in files:
        for line in file:
            yield line.strip('\n')

def count_words_and_lines(sentences):
    counts = {}
    lines_num = 0
    for sentence in sentences:
        lines_num += 1
        for word in sentence:
            if word in counts:
                counts[word] += 1
            else:
                counts[word] = 1
    return counts, lines_num

def cut_off_set(counts, cut_off):
    return marisa_trie.Trie((x for x in counts.keys() if counts[x] > cut_off))

def pronounciation(sentence):
    pronoun = u""
    for word in sentence:
        s, p = words.surface_pronoun(word)
        pronoun = pronoun + p
    return pronoun

class LM:

    def __init__(self):
        pass

    def train(self, file_names):
        print("Counting words...")
        files = [codecs.open(fname, encoding='utf-8') for fname in file_names]
        lines = concat(files)
        sentences = (line.split(' ') for line in lines)
        counts, lines_num = count_words_and_lines(sentences)
        self.known_words = cut_off_set(counts, lmconfig.unknownword_threshold)
        map(lambda f: f.close(), files)

        print("Building statistical model...")
        files = [codecs.open(fname, encoding='utf-8') for fname in file_names]
        lines = concat(files)
        sentences = (line.split(' ') for line in lines)
        slm = stats.SLM()
        slm.fit(sentences)
        unigram_freq, next_types, bigram_freq = slm.output()
        self.dict = marisa_dict.MarisaDict()
        self.dict.populate(unigram_freq, next_types, bigram_freq)
        map(lambda f: f.close(), files)

        if learn_config.learn_collocation:
            print("Learning collocations...")
            self.collocationLM = collocation_lm.CollocationLM(self.dict)
            files = [codecs.open(fname, encoding='utf-8') for fname in file_names]
            lines = concat(files)
            sentences = (line.split(' ') for line in lines)
            self.collocationLM.train(sentences)
            map(lambda f: f.close(), files)
        print("training end.")

    def score(self, path):
        deep_words = [node.deep for node in path]
        return self.collocationLM.score(deep_words)

    def n_candidates(self, pronoun, n):
        gr = graph.Graph(self.dict, pronoun)
        viterbi.forward_dp(self.dict, gr)
        paths = viterbi.backward_a_star(self.dict, gr, n)
        return paths

    def convert(self, pronoun):
        paths = self.n_candidates(pronoun, conversion_config.candidates_num)
        return sorted(paths, key=lambda path: - self.score(path))[0]

    def save(self, path):

        print("Saving the language model...", file=sys.stderr)
        marisa_known_words = marisa_trie.Trie(self.known_words)
        marisa_known_words.save(os.path.join(path, 'known_words'))
        self.dict.save(path)
        if learn_config.learn_collocation:
            print("Saving the collocation language model...", file=sys.stderr)
            self.collocationLM.save(path)
        print("end.", file=sys.stderr)


    def load(self, path):
        print("loading the language model...", file=sys.stderr)
        self.dict = marisa_dict.MarisaDict()
        self.dict.mmap(path)
        self.known_words = marisa_trie.Trie().mmap(os.path.join(path, 'known_words'))
        print("loading collocation paramaters...", file=sys.stderr)
        self.collocationLM = collocation_lm.CollocationLM(self.dict)
        self.collocationLM.load(path)
        print("end.", file=sys.stderr)
