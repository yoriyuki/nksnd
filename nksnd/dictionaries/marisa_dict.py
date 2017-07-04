import math
import marisa_trie
import struct
import os
import json
from utils import words
from config import slm_config

unigram_fmt="<II"

def _decode_num(data):
    return struct.unpack('<I', data[0])[0]

class MarisaDict:
    def __init__(self):
        pass

    def populate(self, unigram_freq, next_types, bigram_freq):
        vocaburary = (key for key in unigram_freq.keys() if words.is_word(key))
        dictionary_items = ((words.surface_pronoun(word)[1], word.encode('utf-8')) for word in vocaburary)
        self.dict = marisa_trie.BytesTrie(dictionary_items)

        word_list = []
        self.word_count = 0
        for word, freq in unigram_freq.items():
            self.word_count += freq
            if word in next_types:
                t = next_types[word]
            else:
                t = 0
            word_list.append((word, (freq, t)))
        self.vocaburaly_size = len(word_list)
        self._unigram_stat = marisa_trie.RecordTrie(unigram_fmt,word_list)

        bytesitems = ((key, struct.pack('<I', freq)) for key, freq in bigram_freq.items())
        self._bigram_stat = marisa_trie.BytesTrie(bytesitems)

    def _dict_get(self, pronoun):
        return [word.decode('utf-8') for word in self._dict[pronoun]]

    def pronoun_prefixes(self, pronoun):
        return self._dict.prefixes(pronoun)

    def get_unigram_stat(self, word):
        if word in self._unigram_stat:
            return self._unigram_stat[word][0]
        else:
            return (0, 0)

    def get_bigram_freq(self, word1, word2):
        k = words.compose_bigram_key(word1, word2)
        if k in self._bigram_stat:
            return _decode_num(self._bigram_stat[k])
        else:
            return 0

    def save(self, path):
        dict_filename = os.path.join(path, 'dictionary')
        self.dict.save(dict_filename)
        unigram_filename = os.path.join(path, 'unigram')
        self._unigram_stat.save(unigram_filename)
        bigram_filename = os.path.join(path, 'bigram')
        self._bigram_stat.save(bigram_filename)
        with open(os.path.join(path, 'metadata'), 'w') as f:
            json.dump(self.word_count, f)

    def mmap(self, path):
        dict_filename = os.path.join(path, 'dictionary')
        self.dict = marisa_trie.BytesTrie()
        self.dict.mmap(dict_filename)
        unigram_filename = os.path.join(path, 'unigram')
        self._unigram_stat = marisa_trie.RecordTrie(unigram_fmt)
        self._unigram_stat.mmap(unigram_filename)
        bigram_filename = os.path.join(path, 'bigram')
        self._bigram_stat = marisa_trie.BytesTrie()
        self._bigram_stat.mmap(bigram_filename)
        self.vocaburaly_size = len(self._unigram_stat)
        with open(os.path.join(path, 'metadata'), 'r') as f:
            self.word_count = json.load(f)
