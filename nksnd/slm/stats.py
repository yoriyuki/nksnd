from utils import words
from dictionaries import marisa_dict

class SLM:
    def __init__(self):
        self.unigram_freq = {}
        self.next_words = {}
        self.bigram_freq = {}

    def fit(self, sentences):
        for sentence in sentences:
            sentence = [u'_BOS'] + sentence + [u'_EOS']
            for word in sentence:
                if word in self.unigram_freq:
                    self.unigram_freq[word] += 1
                else:
                    self.unigram_freq[word] = 1

            for i in range(len(sentence) - 1):
                word1 = sentence[i]
                word2 = sentence[i+1]
                k = words.compose_bigram_key(word1, word2)
                if k in self.bigram_freq:
                    self.bigram_freq[k] += 1
                else:
                    self.bigram_freq[k] = 1
                if word1 in self.next_words:
                    self.next_words[word1].add(word2)
                else:
                    self.next_words[word1] = {word2}

    def output(self):
        next_types = {}
        for word in self.next_words:
            next_types[word] = len(self.next_words[word])

        return (self.unigram_freq, next_types, self.bigram_freq)
