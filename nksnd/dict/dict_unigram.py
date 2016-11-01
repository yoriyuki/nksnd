import marisa_trie
import words

class DictUnigram:
    def __init__(self, known_words):
        self._dict = {}
        self._normalized_count = {}
        self._known_words = known_words

    def get(self, word):
        w = words.replace_word(self._known_words, word)
        if w in self._dict:
            return self._dict[w]
        else:
            return 0

    def set(self, word, weight):
        self._dict[repalce(self._known_words, word)] = weight

    def last_normalized(self, word):
        if word in self._normalized_count:
            return self._normalized_count[word]
        else:
            return 0

    def set_normalized(self, word, count):
        self._normalized_count[word] = count

    def save(self, path):
        fmt ="<f"
        trie = marisa_trie.RecordTrie(fmt, self._dict.iteritems())
        dict_filename = os.path.join(path, 'unigram_dict')
        with open(dict_filename, 'w') as file:
            trie.write(f)

    def map(self, path):
        fmt = "<f"
        dict_filename = os.path.join(path, 'unigram_dict')
        self.dict = marisa_trie.RecordTrie(fmt).mmap(dict_filename)
