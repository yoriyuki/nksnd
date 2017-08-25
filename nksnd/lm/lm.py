from __future__ import print_function
import codecs
import pickle
import os
import sys
import marisa_trie

from nksnd.utils import words
from nksnd.dictionaries import marisa_dict
from nksnd.graph import graph, viterbi
from nksnd.slm import slm
from nksnd.config import lmconfig, slm_config

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
        self.slm = slm.SLM()
        self.slm.fit(sentences)
        map(lambda f: f.close(), files)

        print("training end.")

    def score(self, words):
        words = [u'_BOS'] + words + [u'_EOS']
        score = 0
        for i in range(len(words) - 1):
            score += self.slm.get_bigram_weight(words[i], words[i+1])
        return score

    def n_candidates(self, pronoun, n):
        gr = graph.Graph(self.slm, pronoun)
        viterbi.forward_dp(self.slm, gr)
        paths = viterbi.backward_a_star(self.slm, gr, n)
        return paths

    def convert(self, pronoun):
        return self.n_candidates(pronoun, 1)[0]

    def next_candidates(self, words, pronoun, num):
        candidates = self.slm.get_from_pronoun(pronoun)
        if len(words) > 0:
            candidates_with_weight = [(word, self.slm.get_bigram_weight(words[-1], word)) for word in candidates]
        else:
            candidates_with_weight = [(word, self.slm.get_unigram_weight(word)) for word in candidates]
        sorted_tuples = sorted(candidates_with_weight, key=lambda t: - t[1])
        sorted_candidates = list(map(lambda t: t[0], sorted_tuples))
        if num > 0:
            return sorted_candidates[:num]
        else:
            return sorted_candidates

    def save(self, path):

        print("Saving the language model...", file=sys.stderr)
        marisa_known_words = marisa_trie.Trie(self.known_words)
        marisa_known_words.save(os.path.join(path, 'known_words'))
        self.slm.save(path)
        print("end.", file=sys.stderr)

    def load(self, path):
        self.slm = slm.SLM()
        self.slm.mmap(path)
        self.known_words = marisa_trie.Trie().mmap(os.path.join(path, 'known_words'))
