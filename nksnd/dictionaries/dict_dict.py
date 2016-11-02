import marisa_trie
from utils import numerics

class DictDict(Dictionary):
    def __init__(self, known_words):
        self._dict = {}
        self._normalized_count = {}
        self._known_words = known_words

    def fobos_update(self, g):
        self._count += 1
        for key in g.dict.keys():
            if key in self._normalized_count:
                d = self._normalized_count[key]
            else:
                d = 0
            w = numerics.clip(self._dict[key], lmconfig.normalization_factor * d)
            self._dict[key] = self._dict[key] + lmconfig.eta * g.get(key)
            self._normalized_count[k] = self._count

    def save(self, path):
        fmt ="<f"
        trie = marisa_trie.RecordTrie(fmt, self._dict.iteritems())
        dict_filename = os.path.join(path, 'unigram_dict')
        with open(dict_filename, 'w') as file:
            trie.write(f)
