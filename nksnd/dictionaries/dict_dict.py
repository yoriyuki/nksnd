import itertools
import marisa_trie
from utils import numerics
from dictionaries import dictionary
from config import lmconfig

class DictDict(dictionary.Dictionary):
    def __init__(self, known_words):
        self._cost = {}
        self._updated_count = {}
        self._count = 0
        dictionary = {}
        for word in known_words:
            s, p = surface_pronoun(word)
            dictionary[p] = s.encode('utf-8')
        self._dict = marisa_trie.BytesTrie(dictionary.iteritems())

    def _cost_get(self, key):
        if key in self._cost:
            return self._cost[key]
        else:
            return 0

    def prefixes(self, pronoun):
        return self._dict.prefixes(pronoun)

    def get_from_pronoun(self, pronoun):
        words = self._dict[pronoun]
        return [word, self._cost[word] for word in words]

    def get_unknown_cost(self, unknown):
        return self._cost[unknown]

    def get_bigram_cost(self, word1, word2):
        k = words.compose_bigram_key(w1, w2)
        if k in self._cost:
            return self._cost[k]
        else:
            return 0

    def fobos_update(self, g):
        self._count += 1
        for key in g.dict.keys():
            w = self._cost_get(key) + lmconfig.eta * g.get(key)
            if key in self._updated_count:
                d = self._normalized_count[key]
            else:
                d = 0
            w = numerics.clip(w, lmconfig.normalization_factor * (self.count - d))
            if w == 0:
                del(self.cost, key)
            else:
                self._cost[key] = w
            self._normalized_count[key] = self._count

    def fobos_normalize(self):
        for key in self._cost:
            w = numerics.clip(self._cost[key], lmconfig.normalization_factor * (self.count - self._normalized_count[key]))
            if w == 0:
                del(self.cost, key)
            else:
                self._cost[key] = w

    def save(self, path):
        dictionary_with_cost = [p, (word, self._cost[word]) for p, word in self._dict.items]
        dict_trie = marisa_trie.RecordTrie('<sf', dictionary_with_cost)
        dict_filename = os.path.join(path, 'dictionary')
        dict_trie.save(dict_filename)

        costs = ((key, cost) for (key, cost) in self._cost.iteritems if not words.is_word(key))
        bytesitems = ((key, struct.pack('<f', v)) for key, costs in costs)
        cost_trie = marisa_trie.BytesTrie(bytesitems)
        costs_filename = os.path.join(path, 'costs')
        cost_trie.save(costs_filename)
