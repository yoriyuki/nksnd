import math
from utils import words

class Dictionary:
    def _dict_get(self, pronoun):
        return [word.decode('utf-8') for word in self._dict[pronoun]]

    def pronoun_prefixes(self, pronoun):
        return self._dict.prefixes(pronoun)

    def get_from_pronoun(self, pronoun):
        ret = []
        for word in self._dict_get(pronoun):
            n, t = self._unigram_stat[word]
            ret.append((word, math.log(n) - math.log(self.word_count)))
        return ret

    def get_unknownword_weight(self, unknown):
        n, t = self._unigram_stat[unknown]
        return math.log(n) - math.log(self.word_count)

    def get_bigram_weight(self, word1, word2):
        word1_n, word1_t = self._unigram_stat[word1]
        escape = word1_t / word1_n
        k = words.compose_bigram_key(word1, word2)
        if key in self._bigram:
