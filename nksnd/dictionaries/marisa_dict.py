import math
import marisa_trie
import struct
import os
from utils import words

unigram_fmt="<II"

def _decode_num(data):
    return struct.unpack('<I', data[0])[0]

class MarisaDict:
    def __init__(self):
        pass

    def populate(self, known_words, unigram_freq, next_types, bigram_freq):
        dictionary_items = ((words.surface_pronoun(word)[1], word.encode('utf-8')) for word in known_words)
        self._dict = marisa_trie.BytesTrie(dictionary_items)

        word_list = []
        for word, freq in unigram_freq.iteritems():
            if word in next_types:
                t = next_types[word]
            else:
                t = 0
            word_list.append((word, (freq, t)))
        self.word_count = len(word_list)
        self._unigram_stat = marisa_trie.RecordTrie(unigram_fmt,word_list)

        bytesitems = ((key, struct.pack('<I', freq)) for key, freq in bigram_freq.iteritems())
        self._bigram_stat = marisa_trie.BytesTrie(bytesitems)

    def _dict_get(self, pronoun):
        return [word.decode('utf-8') for word in self._dict[pronoun]]

    def _get_bigram_freq(self, word1, word2):
        k = words.compose_bigram_key(word1, word2)
        if k in self._bigram_stat:
            return _decode_num(self._bigram_stat[k])
        else:
            return 0

    def pronoun_prefixes(self, pronoun):
        return self._dict.prefixes(pronoun)

    def get_from_pronoun(self, pronoun):
        ret = []
        for word in self._dict_get(pronoun):
            n, t = self._unigram_stat[word][0]
            ret.append((word, math.log(float(n) / self.word_count)))
        return ret

    def _get_unigram_weight(self, word):
        n, t = self._unigram_stat[word][0]
        return math.log(float(n) / self.word_count)

    def get_unknownword_weight(self, unknown):
        return self._get_unigram_weight(unknown)

    def get_bigram_weight(self, word1, word2):
        word1_n, word1_t = self._unigram_stat[word1][0]
        escape = 0.99999 * float(word1_t) / word1_n
        n = self._get_bigram_freq(word1, word2)
        if n == 0:
            return self._get_unigram_weight(word2) + math.log(escape)
        else:
            return math.log(float(n) / word1_n * (1 - escape))

    def save(self, path):
        dict_filename = os.path.join(path, 'dictionary')
        self._dict.save(dict_filename)
        unigram_filename = os.path.join(path, 'unigram')
        self._unigram_stat.save(unigram_filename)
        bigram_filename = os.path.join(path, 'bigram')
        self._bigram_stat.save(bigram_filename)

    def mmap(self, path):
        dict_filename = os.path.join(path, 'dictionary')
        self._dict = marisa_trie.BytesTrie()
        self._dict.mmap(dict_filename)
        unigram_filename = os.path.join(path, 'unigram')
        self._unigram_stat = marisa_trie.RecordTrie(unigram_fmt)
        self._unigram_stat.mmap(unigram_filename)
        bigram_filename = os.path.join(path, 'bigram')
        self._bigram_stat = marisa_trie.BytesTrie()
        self._bigram_stat.mmap(bigram_filename)
        self.word_count = len(self._unigram_stat)
