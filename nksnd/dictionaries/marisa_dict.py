import marisa_trie
import os
import struct
from dictionaries import dictionary

class MarisaDict(dictionary.Dictionary):
    def __init__(self):
        pass

    def _decode_cost(self, data):
        return struct.unpack('<f', data[0])[0]

    def mmap(self, path):
        dict_filename = os.path.join(path, 'dictionary')
        self._dict = marisa_trie.BytesTrie()
        self._dict.mmap(dict_filename)
        costs_filename = os.path.join(path, 'costs')
        self._cost = marisa_trie.BytesTrie()
        self._cost.mmap(costs_filename)
