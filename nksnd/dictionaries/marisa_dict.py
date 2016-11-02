import marisa_trie
import words

class MarisaUnigram:
    def __init__(self, known_words):
        self._known_words = known_words

    def get(self, word):
        w = words.replace_word(self.known_words, word)
        self._dict[w]

    def map(self, path):
        fmt = "<f"
        dict_filename = os.path.join(path, 'unigram_dict')
        self._dict = marisa_trie.RecordTrie(fmt).mmap(dict_filename)
