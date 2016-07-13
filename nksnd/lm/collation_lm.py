from learner.collation_vectorizer import CollationVectorizer
from learner.collation_vectorizer import collation_samples
from basictypes import utils
from sklearn.linear_model import LogisticRegression
from sklearn.decomposition import TruncatedSVD


class CollationLM:
    def __init__(self, penalty='l2', solver='lbfgs', max_iter=10, feature_num=1000, outcome_num=1000):
        self._model = LogisticRegression(penalty=penalty, solver=solver, verbose=1, max_iter=max_iter)
        self._decomp_features = TruncatedSVD(n_components=feature_num)
        self._feature_num = feature_num
        self._outcome_num = outcome_num

    def _probability(prob, mrphs):
        p = 1.0
        for i in range(len(mrphs)):
            c = self._vectorizer.outcome_cluster(mrphs[i])
            p = p * prob[tuple(mrphs[0:i-1])][c]
        return p

    def feature_num(self):
        return self._feature_num

    def outcome_num(self):
        return self._outcome_num

    def train(self, file_names):
        print("vectorizing...")
        self._vectorizer = CollationVectorizer(self._feature_num, self._outcome_num)
        x = self._vectorizer.fit_transform(file_names)
        y = self._vectorizer.clustered_outcomes

        print("training...")
        self._model.fit(x, y)
        sparcity = (self._model.coef_ == 0).sum() / float(self._model.coef_.size)
        print("Sparcity:", sparcity)
        if sparcity >= 0.5:
            self._model.sparsify()

    def predict_proba(mrphs_list):
        context_set = set((c for c, f in collation_samples(mrphs_list)))
        contexts = tuple(context_set)
        feature_vecs = self._vectorizer.feature_vecs(contexts)
        x = self._model.predict_proba(feature_vecs)
        prob={}
        for i in range(contexts):
            prob[contexts[i]] = x.getrow(i)
        return [self._probability(prob, mrphs) for mrphs in mrphs_list]
