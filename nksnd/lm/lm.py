import collocation_lm
import codecs
import pickle
import os
import marisa_trie
from utils import words
from config import lmconfig

def concat(files):
    for file in files:
        for line in file:
            yield line

def count_words(sentences):
    counts = {}
    for sentence in sentences:
        for word in sentence:
            if word in counts:
                counts[word] += 1
            else:
                counts[word] = 1
    return counts

def cut_off_set(counts, cut_off):
    return marisa_trie.Trie((x for x in counts.keys() if counts[x] > cut_off))

class LM:

    def __init__(self):
        self.collocationLM = collocation_lm.CollocationLM()

    def train(self, file_names):
        files = [codecs.open(fname, encoding='utf-8') for fname in file_names]
        lines = concat(files)
        sentences = (line.split(' ') for line in lines)
        counts = count_words(sentences)
        self.known_words = cut_off_set(counts, lmconfig.unknownword_threshold)
        map(lambda f: f.close(), files)

        files = [codecs.open(fname, encoding='utf-8') for fname in file_names]
        lines = concat(files)
        sentences = (line.split(' ') for line in lines)
        words_seq = ([words.replace_word_word(self.known_words, word) for word in sentence] for sentence in sentences)
        self.collocationLM.train(words_seq)
        map(lambda f: f.close(), files)

    def score(self, sentence):
        words = [words.replace_word(self.known_words, word) for word in sentence]
        return self.collocationLM.score(words)

    def save(self, path):
        print("Saving known words...")
        words_filename = os.path.join(path, 'known_words')
        with open(words_filename, 'w+b') as f:
            self.known_words.save(f)

        print("Saving the collocation language model...")
        self.collocationLM.save(path)

    def load(self, path):
        print("loading known words...")
        words_filename = os.path.join(path, 'known_words')
        self.known_words = marisa_trie.Trie.mmap(words_filename)
        print("loading collocation paramaters...")
        self.collocationLM.load(path)
