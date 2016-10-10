from utils import genmaxent, words
import codecs
import pickle
import os

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

def cut_off_set(counts, cut_off=1):
    return { x for x in counts.keys() if counts[x] > cut_off }

def replace_word(known_words, word):
    if word in known_words:
        return words.escapeword(word)
    else:
        return words.unknownword(word)

def features(context):
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

def gen_data(known_words,sentences):
    for sentence in sentences:
        words = [replace_word(known_words, word) for word in sentence]
        for i in range(len(words)):
            yield (features(words[0:i-1]), words[i])

class CollocationLM:
    def __init__(self):
        self._model = genmaxent.GenMaxEntModel()

    def _eval(self, context, outcome):
        return self._model.eval(context, outcome)

    def train(self, file_names):

        files = [codecs.open(fname, encoding='utf-8') for fname in file_names]
        lines = concat(files)
        sentences = (line.split() for line in lines)
        counts = count_words(sentences)
        self.known_words = cut_off_set(counts)
        map(lambda f: f.close(), files)

        files = [codecs.open(fname, encoding='utf-8') for fname in file_names]
        lines = concat(files)
        sentences = (line.split() for line in lines)
        data = gen_data(self.known_words, sentences)
        self._model.train(data, cutoff=1)
        map(lambda f: f.close(), files)

    def collocation_score(self, sentence):
        words = [replace_word(self.known_words, word) for word in sentence]
        p = 1.0
        for i in range(len(words)):
            p = p * self._eval(features(words[0:i-1]), words[i])
        return p

    def save(self, path):
        param_filename = os.path.join(path, 'collocation_param')
        self._model.save(param_filename)
        words_filename = os.path.join(path, 'known_words')
        with open(words_filename, 'w+b') as f:
            pickle.dump(self.known_words, f, pickle.HIGHEST_PROTOCOL)

    def load(self, path):
        param_filename = os.path.join(path, 'collocation_param')
        self._model.load(param_filename)
        words_filename = os.path.join(path, 'known_words')
        with open(words_filename, 'r+b') as f:
            self.known_words = pickle.load(f)
