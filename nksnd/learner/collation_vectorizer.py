from ..basictypes import utils, morph
from sklearn.decomposition import TruncatedSVD
from sklearn.cluster import AgglomerativeClustering
from scipy.sparse import csr_matrix, dok_matrix, linalg, diag

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
    def __init__(self, feature_dim, outcome_cluster_num):
        self._feature_num = 0
        self._feature_id_map = {}
        self._outcome_num = 0
        self._outcome_id_map = {}
        self._feature_dim = feature_dim
        self._outcome_cluster_num = outcome_cluster_num

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
            yield [self._feature_id(f) for f in features],     self._outcome_id[outcome]

    def fit_transform(self, file_names):
        files = [open(fname) for fname in file_names]
        lines = utils.concat(files)
        sentences = (line.split() for line in lines)
        self._cut_off_set = _cut_off_set(sentences)
        mrphs_list = _corpus_tokenier(sentences, self._cut_off_set)
        samples = _collation_samples(mrphs_list)
        numbered_samples = self._numbered(samples)

        indicies=[]
        data=[]
        indptr=[]
        for features, outcome in numbered_samples:
            for f in features:
                indices.append(f)
                data.append(1)
            indptr.append(len(indices))
            outcomes.append(outcome)
        x_raw = csr_matrix((data, indices, indptr), dtype=int)

        #compressing features
        self._svd = TruncatedSVD(n_components=self._feature_dim)
        x = self._svd.fit_transform(x_raw)

        #clustering outcomes
        y_raw = dok_matrix((len(outcomes), self._outcome_num), dtype=int)
        for i in range(len(outcomes)):
            y_raw[outcomes[i], i] = 1
        inverse_count = linalg.inv(diags(y_raw.sum(1)))
        self._cl = AgglomerativeClustering(n_clusters=self._outcome_cluster_num)
        self._outcome_clusters =
            self._cl.fit_predict(inverse_count.dot(y_raw.dot(x)))
        map(lambda f: f.close(), files)
        return x

    # Do funny things when file_names contain words
    # which are not contained in files given to fit.
    def transform(self, file_names):
        files = [open(fname) for fname in file_names]
        lines = utils.concat(files)
        sentences = (line.split() for line in lines)
        mrphs_list = _corpus_tokenier(sentences, self._cut_off_set)
        samples = _collation_samples(mrphs_list)
        numbered_samples = self._numbered(samples)
        indicies=[]
        data=[]
        indptr=[]
        for features, outcome in numbered_samples:
            for f in features:
                indices.append(f)
                data.append(1)
            indptr.append(len(indices))
        x_raw = csr_matrix((data, indices, indptr), dtype=int)
        x = self._svd.transform(x_raw)
        return x

    def outcome_cluster(self, outcome):
        return self._outcome_cluster[self._outcome_id[outcome]]
