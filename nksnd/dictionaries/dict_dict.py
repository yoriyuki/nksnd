import itertools
import os
import struct
import marisa_trie
from utils import numerics, words
from config import lmconfig
from dictionaries import dictionary

class DictDict(dictionary.Dictionary):
    def __init__(self, known_words):
        self._weight = {}
        self._updated_count = {}
        self._count = 0
        dictionary_items = ((words.surface_pronoun(word)[1], word.encode('utf-8')) for word in known_words) 
        self._dict = marisa_trie.BytesTrie(dictionary_items)

    def _decode_weight(self, f):
        return f

    def fobos_update(self, g):
        self._count += 1
        for key in g.dict.keys():
            w = self._get_weight(key) + lmconfig.eta * g.get(key)
            if key in self._updated_count:
                d = self._updated_count[key]
            else:
                d = 0
            w = numerics.clip(w, lmconfig.regularization_factor * (self._count - d))
            if w == 0 and key in self._weight:
                del(self._weight[key])
            else:
                self._weight[key] = w
            self._updated_count[key] = self._count

    def fobos_regularize(self):
        for key in self._weight.keys():
            w = numerics.clip(self._weight[key], lmconfig.regularization_factor * (self._count - self._updated_count[key]))
            if w == 0 and key in self._weight:
                del(self._weight[key])
            else:
                self._weight[key] = w

    def save(self, path):
        dict_filename = os.path.join(path, 'dictionary')
        self._dict.save(dict_filename)

        bytesitems = ((key, struct.pack('<f', weight)) for key, weight in self._weight.iteritems())
        weight_trie = marisa_trie.BytesTrie(bytesitems)
        weights_filename = os.path.join(path, 'weights')
        weight_trie.save(weights_filename)
