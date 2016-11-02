import marisa_trie
from utils import numerics
from dictionaries import dictionary
from config import lmconfig

class DictDict(dictionary.Dictionary):
    def __init__(self, known_words):
        self._dict = {}
        self._normalized_count = {}
        self._known_words = known_words
        self._count = 0

    def _dict_get(self, key):
        if key in self._dict:
            return self._dict[key]
        else:
            return 0

    def fobos_update(self, g):
        self._count += 1
        for key in g.dict.keys():
            if key in self._normalized_count:
                d = self._normalized_count[key]
            else:
                d = 0
            w = numerics.clip(self._dict_get(key), lmconfig.normalization_factor * d)
            self._dict[key] = w + lmconfig.eta * g.get(key)
            self._normalized_count[key] = self._count

    def save(self, path):
        fmt ="<f"
        bytesitems = ((key, struct.pack(fmt, v)) for key, v in self._dict.iteritems())
        trie = marisa_trie.BytesTrie(bytesitems)
        dict_filename = os.path.join(path, 'dict')
        trie.save(dict_filename)
