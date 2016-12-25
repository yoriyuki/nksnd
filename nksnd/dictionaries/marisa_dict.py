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
        vocaburary = (key for key in unigram_freq.iterkeys() if words.is_word(key))
        dictionary_items = ((words.surface_pronoun(word)[1], word.encode('utf-8')) for word in vocaburary)
        self._dict = marisa_trie.BytesTrie(dictionary_items)

        word_list = []
        self.word_count = 0
        for word, freq in unigram_freq.iteritems():
            self.word_count += freq
            if word in next_types:
                t = next_types[word]
            else:
                t = 0
            word_list.append((word, (freq, t)))
        self.vocaburaly_size = len(word_list)
        self._unigram_stat = marisa_trie.RecordTrie(unigram_fmt,word_list)

        bytesitems = ((key, struct.pack('<I', freq)) for key, freq in bigram_freq.iteritems())
        self._bigram_stat = marisa_trie.BytesTrie(bytesitems)

    def _dict_get(self, pronoun):
        return [word.decode('utf-8') for word in self._dict[pronoun]]

    def _get_unigram_stat(self, word):
        if word in self._unigram_stat:
            return self._unigram_stat[word][0]
        else:
            return (0, 0)

    def _get_bigram_freq(self, word1, word2):
        k = words.compose_bigram_key(word1, word2)
        if k in self._bigram_stat:
            return _decode_num(self._bigram_stat[k])
        else:
            return 0

    def _escape(self, word):
        if word in self._unigram_stat:
            n, t = self._get_unigram_stat(word)
            return slm_config.max_escape_rate * float(t) / n
        else:
            return slm_config.max_escape_rate

    def _get_unigram_weight(self, word):
        n, t = self._get_unigram_stat(word)
        return math.log((n + slm_config.additive_smoothing) / (self.word_count + slm_config.additive_smoothing))

    def pronoun_prefixes(self, pronoun):
        return self._dict.prefixes(pronoun)

    def get_from_pronoun(self, pronoun):
        ret = []
        for word in self._dict_get(pronoun):
            #w = self._get_unigram_weight(word)
            ret.append((word, 0))
        return ret

    def get_unknownword_weight(self, unknown):
        return self._get_unigram_weight(unknown)

    def get_bigram_weight(self, word1, word2):
        word1_n, word1_t = self._get_unigram_stat(word1)
        escape = self._escape(word1)
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
        with open(os.path.join(path, 'metadata'), 'w') as f:
            json.dump(self.word_count, f)

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
        self.vocaburaly_size = len(self._unigram_stat)
        with open(os.path.join(path, 'metadata'), 'r') as f:
            self.word_count = json.load(f)
