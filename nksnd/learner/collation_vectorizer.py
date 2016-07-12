from basictypes import utils, morph
from sklearn.decomposition import TruncatedSVD
from sklearn.cluster import AgglomerativeClustering
from scipy.sparse import csr_matrix, dok_matrix, linalg, diags

def _cut_off_set(sentences):
    counts = count_words(sentences)
    cut_off_set = utils.cut_off_set(counts, cut_off=1)

def _corpus_tokenizer(sentences):
    for sentence in sentences:
        yield [morph.Morph(word) for word in sentence]

def collation_samples(mrphs_list):
    for mrphs in mrphs_list:
        for i in range(len(mrphs)):
            features = set(mrphs[0:i-1])
            yield (features, mrphs[i])

class CollationVectorizer():
    def __init__(self, feature_dim, outcome_cluster_num):
        self._word_id = {}
        self._feature_dim = feature_dim
        self._outcome_cluster_num = outcome_cluster_num

    def _mrph_id(self, mrph):
        if mrph.key() in self._word_id:
            return morph.max_unkown_id + 1 + self._word_id[mrph.key()]
        else:
            return mrph.unknown_key()

    def _feature_id(self, feature):
        return self._mrph_id(feature)

    def _outcome_id(self, outcome):
        return self._mrph_id(outcome)

    def _numbered(self, samples):
        for features, outcome in samples:
            yield [self._feature_id(f) for f in features],     self._outcome_id(outcome)

    def _outcome_num(self):
        morph.max_unkown_id + len(self._word_id)

    def fit_transform(self, file_names):
        files = [open(fname) for fname in file_names]
        lines = utils.concat(files)
        sentences = (line.split() for line in lines)
        word_count = {}
        for sentence in sentences:
            for word in sentence:
                if word in word_count:
                    word_count[word] += 1
                else:
                    word_count[word] = 1
        word_list = list((w for w, c in word_count.items() if c > 1))
        for i in range(len(word_list)):
            self._word_id[word_list[i]] = i
        map(lambda f: f.close(), files)

        files = [open(fname) for fname in file_names]
        lines = utils.concat(files)
        sentences = (line.split() for line in lines)
        mrphs_list = _corpus_tokenizer(sentences)
        samples = collation_samples(mrphs_list)
        numbered_samples = self._numbered(samples)

        indices=[]
        data=[]
        indptr=[0]
        outcomes=[0]
        for features, outcome in numbered_samples:
            for f in features:
                indices.append(f)
                data.append(1)
            indptr.append(len(indices))
            outcomes.append(outcome)
        x_raw = csr_matrix((data, indices, indptr), dtype=int)

        #compressing features
        self._feature_reduction = TruncatedSVD(n_components=self._feature_dim)
        x = self._feature_reduction.fit_transform(x_raw)

        #clustering outcomes
        y = dok_matrix((self.outcome_num(), self._feature_dim))
        for i in range(self.outcome_num()):
            y[outcomes[i], i] = 1
        #FIXME! 1 + ... Hack to avoid div by 0!
        inverse_count = linalg.inv(diags(1 + y_raw.sum(1)))
        self._cl = AgglomerativeClustering(n_clusters=self._outcome_cluster_num)
        self._outcome_clusters = self._cl.fit_predict(inverse_count.dot(y_raw.dot(x)))
        map(lambda f: f.close(), files)
        self.clustered_outcomes = [self._outcome_clusters[i] for i in outcomes]
        return x

    def transform(self, file_names):
        files = [open(fname) for fname in file_names]
        lines = utils.concat(files)
        sentences = (line.split() for line in lines)
        mrphs_list = _corpus_tokenier(sentences)
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
        self.clustered_outcomes = [self._outcome_clusters[i] for i in outcomes]
        x = self._feature_reduction.transform(x_raw)
        return x

    def outcome_cluster(self, morph):
        return self._outcome_clusters[self._outcome_id(morph)]

    def feature_vecs(self, contexts):
        features_seq = ((self._feature_id(morph) for morph in context) for context in contexts)
        indicies=[]
        data=[]
        indptr=[]
        for features in features_list:
            for f in feature_ids:
                indices.append(f)
                data.append(1)
            indptr.append(len(indices))
        x_raw = csr_matrix((data, indices, indptr), dtype=int)
        x = self._feature_reduction.transform(x_raw)
        return x
