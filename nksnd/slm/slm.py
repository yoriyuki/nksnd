from utils import words
from dictionaries import marisa_dict

class SLM:
    def __init__(self):
        self.dict = marisa_dict.MarisaDict()

    def fit(self, sentences):
        unigram_freq = {}
        next_words = {}
        bigram_freq = {}
        for sentence in sentences:
            sentence = [u'_BOS'] + sentence + [u'_EOS']
            for word in sentence:
                if word in unigram_freq:
                    unigram_freq[word] += 1
                else:
                    unigram_freq[word] = 1

            for i in range(len(sentence) - 1):
                word1 = sentence[i]
                word2 = sentence[i+1]
                k = words.compose_bigram_key(word1, word2)
                if k in bigram_freq:
                    bigram_freq[k] += 1
                else:
                    bigram_freq[k] = 1
                if word1 in next_words:
                    next_words[word1].add(word2)
                else:
                    next_words[word1] = {word2}
        next_types = {}
        for word in next_words:
            next_types[word] = len(next_words[word])

        self.dict.populate(self.unigram_freq, next_types, self.bigram_freq)

    def save(path):
        self.dict.save(path)

    def mmap(path):
        self.dict = marisa_dict.MarisaDict()
        self.dict.mmap(path)

    def escape(self, word):
        if word in self._unigram_stat:
            n, t = self._get_unigram_stat(word)
            return slm_config.max_escape_rate * float(t) / n
        else:
            return slm_config.max_escape_rate

    def get_unigram_weight(self, word):
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
        escape = self.escape(word1)
        n = self._get_bigram_freq(word1, word2)
        if n == 0:
            return self._get_unigram_weight(word2) + math.log(escape)
        else:
            return math.log(float(n) / word1_n * (1 - escape))
