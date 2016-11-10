from utils import words

class Dictionary:
    #FIXME weight is misnomer.
    def _get_weight(self, key):
        if key in self._weight:
            return self._decode_weight(self._weight[key])
        else:
            return 0

    def _dict_get(self, pronoun):
        return [word.decode('utf-8') for word in self._dict[pronoun]]

    def pronoun_prefixes(self, pronoun):
        return self._dict.prefixes(pronoun)

    def get_from_pronoun(self, pronoun):
        words = self._dict_get(pronoun)
        return [(word, self._get_weight(word)) for word in words]

    def get_unknownword_weight(self, unknown):
        return self._get_weight(unknown)

    def get_bigram_weight(self, word1, word2):
        k = words.compose_bigram_key(word1, word2)
        return self._get_weight(k)
