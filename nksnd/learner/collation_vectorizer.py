from ..basictypes import utils, morph
from sklearn.decomposition import TruncatedSVD
from sklearn.cluster import AgglomerativeClustering
from scipy.sparse import csr_matrix, dok_matrix, linalg, diag

def _cut_off_set(sentences):
    counts = count_words(sentences)
    cut_off_set = utils.cut_off_set(counts, cut_off=1)

def _corpus_tokenizer(sentences):
    for sentence in sentences:
        yield [morph.Morph(word) for word in sentence]

def _collation_samples(mrphs_list):
    for mrphs in mrphs_list:
        for i in range(len(mrphs)):
            features = set([m.key() for m in mrphs[0:i-1]])
            yield (features, mrphs[i].key())

class CollationVectorizer():
    def __init__(self, feature_dim, outcome_cluster_num):
        self._word_id = {}


    def _mrph_id(self, mrph):
        if mrph.key() in self._word_id:
            return morph.max_unkown_id + 1 + self._word_id{mrph.key()}
        else:
            return mrph.unknown_key()

    def _feature_id(self, feature):
        return self._mrph_id(feature)

    def _outcome_id(self, outcome):
        return self._mrph_id(outcome)

    def _numbered(self, samples):
        for features, outcome in samples:
            yield [self._feature_id(f) for f in features],     self._outcome_id(outcome)

    def fit_transform(self, file_names):
        files = [open(fname) for fname in file_names]
        lines = utils.concat(files)
        sentences = (line.split() for line in lines)

        word_count = {}
        for sentence in sentences:
            for word in sentence:
                if word in word_count:
                    word_count += 1
                else:
                    word_count = 1
        word_list = list((w for w, c in word_count.items() if c > 1))
        for i in range(len(word_list)):
            self._word_id[word_list[i]] = i

        mrphs_list = _corpus_tokenier(sentences)
        samples = _collation_samples(mrphs_list)
        numbered_samples = self._numbered(samples)

        indicies=[]
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
        x = self._svd.transform(x_raw)
        return x

    def outcome_cluster(self, outcome):
        outcome_id = self._outcome_id(outcome)
        if outcome_id in self._outcome_cluster:
            return self._outcome_cluster[outcome_id]
        else:
            # a word which does not appear in the corpus, even its unknown form, is mapped to 0
            return self._outcome_cluster[0]
