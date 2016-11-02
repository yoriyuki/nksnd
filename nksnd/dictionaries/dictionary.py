from utils import words

class Dictionary:

    def get_unigram(self, word):
        w = words.replace_word(self._known_words, word)
        if w in self._dict:
            return self._dict[w]
        else:
            return 0

    def get_bigram(self, word1, word2):
        w1 = words.replace_word(self._known_words, word1)
        w2 = words.replace_word(self._known_words, word2)
        k = words.compose_bigram_key(w1, w2)
        if k in self._dict:
            return self._dict[k]
        else:
            return 0
