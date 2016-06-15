from ..basictypes import utils
from ..basictypes import utils
from ..basictypes import morph

def _morph_from_word(word, cut_off_set):
    if word in cut_off_set:
        morph.Morph(word)
    else:
        morph.UnknownMorph(word)

def _cut_off_set(sentences):
    counts = count_words(sentences)
    cut_off_set = utils.cut_off_set(counts, cut_off=1)

def _corpus_tokenizer(sentences, cut_off_set):
    for sentence in sentences:
        yield [_morph_from_word(word, cut_off_set) for word in sentence]

def _collation_samples(mrphs_list):
    for mrphs in mrphs_list:
        for i in range(len(mrphs)):
            features = set([m.key() for m in mrphs[0:i-1]])
            yield (features, mrphs[i].key())

class CollationVectorizer():
    def __init__(self):
        self._feature_num = 0
        self._feature_id_map = {}
        self._outcome_num = 0
        self._outcome_id_map = {}

    def _feature_id(self, feature):
        if feature.key() in self._feature_id_map:
            return self._feature_id_map[feature.key()]
        else:
            self._feature_num += 1
            self._feature_id_map[feature.key()] = self._feature_num
            return self._feature_num

    def _outcome_id(self, feature):
        if outcome.key() in self._outcome_id_map:
            return self._outcome_id_map[outcome.key()]
        else:
            self._come_num += 1
            self._outcome_id_map[outcome.key()] = self._outcome_num
            return self._outcome_num

    def _numbered(self, samples):
        for features, outcome in samples:
            yield [self._feature_id(f) for f in features],     self._outcome_id(outcome)

    def fit-transform(self, file_names):
        files = [open(fname) for fname in file_names]
        lines = utils.concat(files)
        sentences = (line.split() for line in lines)
        self._cut_off_set = _cut_off_set(sentences)
        mrphs_list = _corpus_tokenier(sentences, self._cut_off_set)
        samples = _collation_samples(mrphs_list)
        numbered_samples = self._numbered(samples)

        for features, outcome in numbered_samples:
     for term in d:
         index = vocabulary.setdefault(term, len(vocabulary))
         indices.append(index)
         data.append(1)
     indptr.append(len(indices))
     csr_matrix((data, indices, indptr), dtype=int).toarray()

        map(lambda f: f.close(), files)

    def transform(self, file_names):
