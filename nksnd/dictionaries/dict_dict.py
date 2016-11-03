import itertools
import os
import struct
import marisa_trie
from utils import numerics, words
from dictionaries import dictionary
from config import lmconfig

class DictDict():
    def __init__(self, known_words):
        self._cost = {}
        self._updated_count = {}
        self._count = 0
        dictionary = {}
        for word in known_words:
            s, p = words.surface_pronoun(word)
            dictionary[p] = word.encode('utf-8')
        self._dict = marisa_trie.BytesTrie(dictionary.iteritems())

    def _cost_get(self, key):
        if key in self._cost:
            return self._cost[key]
        else:
            return 0

    def _dict_get(self, pronoun):
        return [word.decode('utf-8') for word in self._dict[pronoun]]

    def pronoun_prefixes(self, pronoun):
        return self._dict.prefixes(pronoun)

    def get_from_pronoun(self, pronoun):
        words = self._dict_get(pronoun)
        return [(word, self._cost_get(word)) for word in words]

    def get_unknownword_cost(self, unknown):
        return self._cost_get(unknown)

    def get_bigram_cost(self, word1, word2):
        k = words.compose_bigram_key(word1, word2)
        return self._cost_get(k)

    def fobos_update(self, g):
        self._count += 1
        for key in g.dict.keys():
            w = self._cost_get(key) + lmconfig.eta * g.get(key)
            if key in self._updated_count:
                d = self._updated_count[key]
            else:
                d = 0
            w = numerics.clip(w, lmconfig.normalization_factor * (self._count - d))
            if w == 0 and key in self._cost:
                del(self._cost[key])
            else:
                self._cost[key] = w
            self._updated_count[key] = self._count

    def fobos_regularize(self):
        for key in self._cost.keys():
            w = numerics.clip(self._cost[key], lmconfig.normalization_factor * (self._count - self._updated_count[key]))
            if w == 0 and key in self._cost:
                del(self._cost[key])
            else:
                self._cost[key] = w

    def save(self, path):
        dictionary_with_cost = [(p, (word, self._cost[word])) for p, word in self._dict.items()]
        dict_trie = marisa_trie.RecordTrie('<sf', dictionary_with_cost)
        dict_filename = os.path.join(path, 'dictionary')
        dict_trie.save(dict_filename)

        costs = ((key, cost) for (key, cost) in self._cost.iteritems() if not words.is_word(key))
        bytesitems = ((key, struct.pack('<f', cost)) for key, cost in costs)
        cost_trie = marisa_trie.BytesTrie(bytesitems)
        costs_filename = os.path.join(path, 'costs')
        cost_trie.save(costs_filename)
