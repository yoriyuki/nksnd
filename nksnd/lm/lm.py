from __future__ import print_function
import collocation_lm
import codecs
import pickle
import os
import sys
import marisa_trie
from utils import words
from config import lmconfig, conversion_config
from crf import parameter_estimater
from dictionaries import marisa_dict
from graph import graph, viterbi

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
        self.collocationLM = collocation_lm.CollocationLM()

    def train(self, file_names):
        print("Counting words...")
        files = [codecs.open(fname, encoding='utf-8') for fname in file_names]
        lines = concat(files)
        sentences = (line.split(' ') for line in lines)
        counts, lines_num = count_words_and_lines(sentences)
        self.known_words = cut_off_set(counts, lmconfig.unknownword_threshold)
        map(lambda f: f.close(), files)

        print("Training the CRF model...")
        files = [codecs.open(fname, encoding='utf-8') for fname in file_names]
        lines = concat(files)
        sentences = (line.split(' ') for line in lines)
        data = ((pronounciation(s), s) for s in sentences)
        crf_estimater = parameter_estimater.CRFEsitimater(self.known_words)
        crf_estimater.fit(data, lines_num)
        self.dict = crf_estimater.dict
        map(lambda f: f.close(), files)

        print("Learning collocations...")
        files = [codecs.open(fname, encoding='utf-8') for fname in file_names]
        lines = concat(files)
        sentences = (line.split(' ') for line in lines)
        words_seq = ([words.replace_word(self.known_words, word) for word in sentence] for sentence in sentences)
        self.collocationLM.train(words_seq)
        map(lambda f: f.close(), files)

    def score(self, path):
        deep_words = [node.deep for node in path]
        return self.collocationLM.score(deep_words)

    def n_candidates(self, pronoun, n):
        gr = graph.Graph(self.dict, pronoun)
        viterbi.forward_dp(self.dict, gr)
        paths = viterbi.backward_a_star(self.dict, gr, n)
        paths = [path[1:-1] for path in paths]
        return paths

    def convert(self, pronoun):
        paths = self.n_candidates(pronoun, conversion_config.candidates_num)
        return sorted(paths, key=lambda path: self.score(path), reverse=True)[0]

    def save(self, path):
        print("Saving the collocation language model...", file=sys.stderr)
        self.collocationLM.save(path)

        print("Saving the CRF model...", file=sys.stderr)
        self.dict.save(path)

    def load(self, path):
        print("loading collocation paramaters...", file=sys.stderr)
        self.collocationLM.load(path)
        print("loading the CRF model...", file=sys.stderr)
        self.dict = marisa_dict.MarisaDict()
        self.dict.mmap(path)
