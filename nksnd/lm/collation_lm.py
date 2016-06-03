from sklearn.linear_model import LogisticRegression
from scipy.sparse import lil_matrix
from numpy import array

def _id(dict, elem):
    if elem.key() in dict['map']:
        return dict['map'][elem.key()]
    else:
        num = dict['num']
        dict['map'][elem.key()] = num
        dict['num'] = num + 1
        return num


class CollationLM:
    def __init__(self, penalty='l2', solver='lbfgs', max_iter=10):
        self._model = LogisticRegression(penalty=penalty, solver=solver, verbose=1, max_iter=max_iter)
        self._features = {'num':0, 'map':{}}
        self._outcomes = {'num':0, 'map':{}}

    def _feature_id(self, feature):
        return _id(self._features, feature)

    def _feature_num(self):
        return self._features['num']

    def _outcome_id(self, outcome):
        return _id(self._outcomes, outcome)

    def _outcome_num(self):
        return self._outcomes['num']

    def _samples(self, sentences):
        samples=[]
        for sentence in sentences:
            for i in range(len(sentence)):
                samples.append((map(self._feature_id, sentence[0:i-1]),
                                self._outcome_id(sentence[i])))
        return samples

    def train(self, sentences):
        print "building samples..."
        samples = self._samples(sentences)
        print len(samples), "samples", self._feature_num(), "features"
        print "building the matrix..."
        x = lil_matrix((len(samples), self._feature_num()))
        y = []
        col = 0
        for i in range(len(samples)):
            feature_ids, outcome_id = samples[i]
            y.append(outcome_id)
            for feature_id in feature_ids:
                x[i, feature_id] = 1.0
        print "training..."
        self._model.fit(x, y)
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
