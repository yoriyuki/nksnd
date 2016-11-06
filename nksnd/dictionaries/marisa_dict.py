import marisa_trie
from dictionaries import dictionary

class MarisaDict(dictionary.Dictionary):
    def __init__(self):
        pass

    def _decode_cost(string):
        struct.unpack('<f', string)

    def map(self, path):
        dict_filename = os.path.join(path, 'dict')
        self._dict = marisa_trie.BytesTrie(fmt).mmap(dict_filename)
        costs_filename = os.path.join(path, 'costs')
        self._cost = marisa_trie.BytesTrie(fmt).mmap(costs_filename)
