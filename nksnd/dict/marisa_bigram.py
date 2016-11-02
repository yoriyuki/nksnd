import marisa_trie
from utils import words

class MarisaUnigram:
    def __init__(self, known_words):
        self._known_words = known_words

    def get(self, word):
        w1 = words.replace_word(self._known_words, word1)
        w2 = words.replace_word(self._known_words, word2)
        self._dict[words.compose_bigram_key(w1, w2)]

    def map(self, path):
        fmt = "<f"
        dict_filename = os.path.join(path, 'bigram_dict')
        self._dict = marisa_trie.RecordTrie(fmt).mmap(dict_filename)
