from sklearn.linear_model import LogisticRegression
from scipy.sparse import lil_matrix
from numpy import array
from sklearn.decomposition import TruncatedSVD
from sklearn.cluster import AgglomerativeClustering
import mmh3

def _samples(sentences):
    for sentence in sentences:
        for i in range(len(sentence)):
            features = set(map(lambda m: m.key(), sentences[0:i-1]))
            yield (features, sentence[i].key())

def _hash_num = 2**21

def _sign(n) = n / abs(n)

def _hash(s):
    h = mmh3.hash(s)
    return _sign(h) * (abs(h) % _hash_num)

def _hashed_samples(samples):
    for features, outcome in samples:
        yield (map(_hash, features), _hash(outcome))

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

class CollationLM:
    def __init__(self, penalty='l2', solver='lbfgs', max_iter=10, n_features=1000, n_outcomes=1000, feature_num=1000, outcome_num=1000):
        self._model = LogisticRegression(penalty=penalty, solver=solver, verbose=1, max_iter=max_iter)
        self._decomp_features = TruncatedSVD(n_components=feature_num)
        self._n_features = n_features
        self._n_outcomes = n_outcomes
        self._feature_num = feature_num
        self._outcome_num = outcome_num

    def _cluster_outcome(self, outcome):
        return self._outcome_cluster_ids[outcome]

    def feature_num(self):
        return self._feature_num

    def outcome_num(self):
        return self._outcome_num

    def train(self, sentences):
        print "building samples..."
        hashed_samples = list(_hashed_sample(_samples(sentences)))
        print len(hashed_samples), "samples"

        print "building the feature matrix..."
        raw_x = lil_matrix((len(hashed_samples), _hash_num))
        outcome_ids = []
        for i in range(len(samples)):
            feature_ids, outcome_id = hashed_samples[i]
            outcome_ids.append(outcome_id)
            for feature_id in feature_ids:
                raw_x[i, abs(feature_id)] += sign(feature_id)

        print "compressing features..."
        x = self._decomp_features.fit_transfrom(raw_x)

        print("building the outcome matrix")
        y_feature_sums = lil_matrix((self._n_outcomes, self.feature_num()))
        y_count = {}
        for i in range(len(samples)):
            feature_ids, outcome_id = hashed_samples[i]
            if outcome_id in y:
                for j, v in x.getrowview(i)
                y_feature_sums[outcome_id, j] += v
                y_count[outcome_id] += 1
            else:
                y_feature_sums[oucome_id, j] = v
                y_count[outcome_id] = 1
        y_features = lil_matrix((self._n_outcomes, self.feature_num()))
        for outcome_id, count in y_count:
            for j, v in y_feature_sums.getrowview(outcome_id):
                y_features[outcome_id, j] = v / count

        print "clustering outcomes..."
        decomp_outcomes = AgglomerativeClustering(n_cluster=outcome_num)
        cluster_ids = decomp_outcomes.fit_transform(y_features)
        self.outcome_cluster_ids = cluster_ids
        print "training..."
        self._model.fit(x, map(self._cluster_outcome, outcome_ids))
        sparcity = (self._model.coef_ == 0).sum() / float(self._model.coef_.size)
        print "Sparcity:", sparcity
        if sparcity >= 0.5:
            self._model.sparsify()

    def eval(self, context, outcome):
        x = lil_matrix(1, self._feature_num()))
        for feature_id in map(self._feature_id, context):
            x[1, feature_id] = 1.0
        y = [self._outcome_id(outcome)]
        return self._model.score(x, y)
