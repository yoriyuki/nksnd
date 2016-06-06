from sklearn.linear_model import LogisticRegression
from scipy.sparse import lil_matrix
from numpy import array, zeros
from sklearn.decomposition import TruncatedSVD
from sklearn.cluster import AgglomerativeClustering
import mmh3

def _samples(sentences):
    for sentence in sentences:
        for i in range(len(sentence)):
            features = set(map(lambda m: m.key(), sentence[0:i-1]))
            yield (features, sentence[i].key())

_hash_num = 2**21

def _sign(n):
    return n / abs(n)

def _hash(s):
    h = mmh3.hash(s)
    return _sign(h) * (abs(h) % _hash_num)

def _hashed_samples(samples):
    for features, outcome in samples:
        yield (map(_hash, features), abs(_hash(outcome)))

def _decompose_features(d):
    keys=[]
    vals=[]
    for key, val in d:
        keys.append(key)
        vals.append(val)
    return (keys, vals)

def _merge(it1, it2):
    d = {}
    for x in it1:
        d[x] = it2.next()
    return d

def _inverse(x):
    y = {}
    for i in range(len(x)):
        y[x[i]] = i
    return y

class CollationLM:
    def __init__(self, penalty='l2', solver='lbfgs', max_iter=10, feature_num=1000, outcome_num=1000):
        self._model = LogisticRegression(penalty=penalty, solver=solver, verbose=1, max_iter=max_iter)
        self._decomp_features = TruncatedSVD(n_components=feature_num)
        self._n_features = _hash_num
        self._n_outcomes = _hash_num
        self._feature_num = feature_num
        self._outcome_num = outcome_num

    def _cluster_outcome(self, outcome):
        return self._outcome_cluster_ids[self._inverse_y[outcome]]

    def feature_num(self):
        return self._feature_num

    def outcome_num(self):
        return self._outcome_num

    def train(self, sentences):
        print "building samples..."
        hashed_samples = list(_hashed_samples(_samples(sentences)))
        print len(hashed_samples), "samples"

        print "building the feature matrix..."
        raw_x = lil_matrix((len(hashed_samples), _hash_num))
        outcome_ids = []
        for i in range(len(hashed_samples)):
            feature_ids, outcome_id = hashed_samples[i]
            outcome_ids.append(outcome_id)
            for feature_id in feature_ids:
                raw_x[i, abs(feature_id)] += _sign(feature_id)

        print "compressing features..."
        x = self._decomp_features.fit_transform(raw_x)

        print("building the outcome matrix")
        y_feature_sums = lil_matrix((self._n_outcomes, self.feature_num()))
        y_count = {}
        for i in range(len(hashed_samples)):
            feature_ids, outcome_id = hashed_samples[i]
            if outcome_id in y_count:
                y_count[outcome_id] += 1
                y_feature_sums[outcome_id] += x[i]
            else:
                y_count[outcome_id] = 1
                y_feature_sums[outcome_id] = x[i]
        y = y_count.keys()
        y_features = array([y_feature_sums[i] / y_count[i] for i in y])
        
        print "clustering outcomes..."
        decomp_outcomes = AgglomerativeClustering(n_clusters=self._outcome_num)
        cluster_ids = decomp_outcomes.fit_predict(y_features)
        self._cluster_ids = cluster_ids
        self._inverse_y = _inverse(y)
        print "training..."
        self._model.fit(x, map(self._cluster_outcome, outcome_ids))
        sparcity = (self._model.coef_ == 0).sum() / float(self._model.coef_.size)
        print "Sparcity:", sparcity
        if sparcity >= 0.5:
            self._model.sparsify()

    def eval(self, context, outcome):
        x = lil_matrix(1, self._feature_num())
        for feature_id in map(self._feature_id, context):
            x[1, feature_id] = 1.0
        y = [self._outcome_id(outcome)]
        return self._model.score(x, y)
