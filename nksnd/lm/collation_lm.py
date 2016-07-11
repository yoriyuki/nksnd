from ..lerner.collation_vectorizer import CollationVectorizer

class CollationLM:
    def __init__(self, penalty='l2', solver='lbfgs', max_iter=10, feature_num=1000, outcome_num=1000):
        self._model = LogisticRegression(penalty=penalty, solver=solver, verbose=1, max_iter=max_iter)
        self._decomp_features = TruncatedSVD(n_components=feature_num)
        self._feature_num = feature_num
        self._outcome_num = outcome_num

    def feature_num(self):
        return self._feature_num

    def outcome_num(self):
        return self._outcome_num

    def train(self, file_names):
        vectorizer = CollationVectorizer(self._feature_num, self._outcome_num)
        x = vectorizer.fit_transform(file_names)
        

        print("building samples...")
        hashed_samples = list(_hashed_samples(_samples(sentences)))
        print len(hashed_samples), "samples"

        print("building the feature matrix...")
        raw_x = lil_matrix((len(hashed_samples), _hash_num))
        outcome_ids = []
        for i in range(len(hashed_samples)):
            feature_ids, outcome_id = hashed_samples[i]
            outcome_ids.append(outcome_id)
            for feature_id in feature_ids:
                raw_x[i, abs(feature_id)] += _sign(feature_id)

        print("compressing features...")
        x = self._decomp_features.fit_transform(raw_x)

        print("building the outcome matrix...")
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
        y_features = [y_feature_sums[i].toarray()[0] / float(y_count[i]) for i in y]

        print("clustering outcomes...")
        decomp_outcomes = AgglomerativeClustering(n_clusters=self.outcome_num())
        cluster_ids = decomp_outcomes.fit_predict(y_features)
        self._cluster_ids = cluster_ids
        self._inverse_y = _inverse(y)
        print("training...")
        self._model.fit(x, map(self._cluster_outcome, outcome_ids))
        sparcity = (self._model.coef_ == 0).sum() / float(self._model.coef_.size)
        print("Sparcity:"), sparcity
        if sparcity >= 0.5:
            self._model.sparsify()

    def eval(self, context, outcome):
        raw_x = lil_matrix(1, self._feature_num())
        for feature_num in _feature_vec(context):
            x[1, abs(feature_num)] += _sign(feature_num)
        x = self._decomp_features.transform(raw_x)
        y = [self._cluster_outcome(_outcome_id(outcome))]
        return self._model.score(x, y)
