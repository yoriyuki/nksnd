import marisa_trie
import words

class DictBigram:
    def __init__(self, known_words):
        self._dict = {}
        self._normalized_count = {}
        self._known_words = known_words

    def get(self, word1, word2):
        w1 = words.replace_word(self._known_words, word1)
        w2 = words.replace_word(self._known_words, word2)
        if (w1, w2) in self._dict:
            return self._dict[(w1, w2)]
        else:
            return 0

    def set(self, word1, word2, weight):
        w1 = words.replace_word(self._known_words, word1)
        w2 = words.replace_word(self._known_words, word2)
        self._dict[(w1, w2)] = weight

    def save(self, path):
        items = ((ws[0] + ' ' + ws[1], score) for ws, score in self._dict.iteritems())
        fmt ="<f"
        trie = marisa_trie.RecordTrie(fmt, items)
        dict_filename = os.path.join(path, 'bigram_dict')
        with open(dict_filename, 'w') as file:
            trie.write(f)
