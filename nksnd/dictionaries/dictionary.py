from utils import words

class Dictionary:

    def _get_cost(self, key):
        if key in self._cost:
            return self._decode_cost(self._cost[key])
        else:
            return 0

    def _dict_get(self, pronoun):
        return [word.decode('utf-8') for word in self._dict[pronoun]]

    def pronoun_prefixes(self, pronoun):
        return self._dict.prefixes(pronoun)

    def get_from_pronoun(self, pronoun):
        words = self._dict_get(pronoun)
        return [(word, self._get_cost(word)) for word in words]

    def get_unknownword_cost(self, unknown):
        return self._get_cost(unknown)

    def get_bigram_cost(self, word1, word2):
        k = words.compose_bigram_key(word1, word2)
        return self._get_cost(k)
