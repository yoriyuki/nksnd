import math
import marisa_trie
import struct
from utils import words

def _decode_num(data):
    return struct.unpack('<I', data[0])[0]

class MarisaDict:
    def __init__(self, known_words, unigram_freq, next_types, bigram_freq):

        self.word_count = len(known_words)
        dictionary_items = ((words.surface_pronoun(word)[1], word.encode('utf-8')) for word in known_words)
        self._dict = marisa_trie.BytesTrie(dictionary_items)

        word_list = []
        for word, freq in unigram_freq.iteritems():
            word_list.append((word, (freq, next_types[word])))
        fmt="<II"
        self._unigram_stat = marisa_trie.RecordTrie(fmt,word_list)

        bytesitems = ((key, struct.pack('<I', freq)) for key, freq in bigram_freq.iteritems())
        self._bigram_stat = marisa_trie.BytesTrie(bytesitems)

    def _dict_get(self, pronoun):
        return [word.decode('utf-8') for word in self._dict[pronoun]]

    def _get_bigram_freq(self, word1, word2):
        k = words.compose_bigram_key(word1, word2)
        if k in self._bigram_stat:
            return _decode_num(self._bigram_stat(k))
        else:
            return 0

    def pronoun_prefixes(self, pronoun):
        return self._dict.prefixes(pronoun)

    def get_from_pronoun(self, pronoun):
        ret = []
        for word in self._dict_get(pronoun):
            n, t = self._unigram_stat[word]
            ret.append((word, math.log(float(n) / self.word_count)))
        return ret

    def _get_unigram_weight(self, word):
        n, t = self._unigram_stat[word]
        return math.log(float(n) / self.word_count)

    def get_unknownword_weight(self, unkown):
        return self._get_unigram_weight(unknown)

    def get_bigram_weight(self, word1, word2):
        word1_n, word1_t = self._unigram_stat[word1]
        escape = float(word1_t) / word1_n
        n = self._get_bigram_freq(word1, word2)
        if n = 0:
            return self._get_unigram_weight(word2) + math.log(escape)
        else:
            return math.log(float(n) / word1_n * (1 - escape))
