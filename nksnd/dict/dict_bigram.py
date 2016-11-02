import marisa_trie
from utils import numerics, words

class DictBigram:
    def __init__(self, known_words):
        self._dict = {}
        self._normalized_count = {}
        self._known_words = known_words
        self._count = 0

    def get(self, word1, word2):
        w1 = words.replace_word(self._known_words, word1)
        w2 = words.replace_word(self._known_words, word2)
        k = words.compose_bigram_key(w1, w2)
        if k in self._dict:
            return self._dict[k]
        else:
            return 0

    def update(self, g):
        self._count += 1
        for key in g.dict.keys():
            if word.is_bigram_key(key):
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
        dict_filename = os.path.join(path, 'bigram_dict')
        with open(dict_filename, 'w') as file:
            trie.write(f)
