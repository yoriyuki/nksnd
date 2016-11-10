import marisa_trie
import os
import struct
from dictionaries import dictionary

class MarisaDict(dictionary.Dictionary):
    def __init__(self):
        pass

    def _decode_weight(self, data):
        return struct.unpack('<f', data[0])[0]

    def mmap(self, path):
        dict_filename = os.path.join(path, 'dictionary')
        self._dict = marisa_trie.BytesTrie()
        self._dict.mmap(dict_filename)
        weights_filename = os.path.join(path, 'weights')
        self._weight = marisa_trie.BytesTrie()
        self._weight.mmap(weights_filename)
