import marisa_trie
from dictionaries import dictionary

class MarisaDict(dictionary.Dictionary):
    def __init__(self, known_words):
        self._known_words = known_words

    def map(self, path):
        fmt = "<f"
        dict_filename = os.path.join(path, 'dict')
        self._dict = marisa_trie.RecordTrie(fmt).mmap(dict_filename)
