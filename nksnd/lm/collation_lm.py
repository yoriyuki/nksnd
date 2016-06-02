from skearn.linear_model import LogisticRegression
from scipy.sparse import lil_matrix
from numpy import array

def _id(dict, elem):
    if elem.key() in dict['map']:
        return dict['map'][elem.key()]
    else:
        dict['num'] = dict['num'] + 1
        dict['map'][elem.key()] = dict['num']
        return dict['num']


class CollationLM:
    def __init__(self):
        self._model = LogisticRegression(penalty='l1')
        self._features = {'num':0, {}}
        self._outcomes = {'num':0, {}}

    def _feature_id(self, feature):
        return _id(self._features, feature)

    def _feature_num(self):
        return self._features['num']

    def _outcome_id(self, outcome):
        return _id(self.outcomes, outcome)

    def _outcome_num(self):
        return self._outcomes['num']

    def _samples(sentences):
        samples=[]
        for sentence in lines:
            mrphs = line.split()
            for i in range(len(mrphs)):
                samples.append((map(self._feature_id, mrphs[0:i-1]),
                                map(self._outcome_id, mrphs[i])))
        return samples

    def train(self, sentences):
        samples = _samples(sentences)
        x = lil_matrix((self._feature_num, len(samples)))
        y = []
        col = 0
        for i in len(samples):
            features, outcome = samples[i]
            y.append(outcome)
            for feature_id in feature_ids:
                x[i][feature_id]=1
        self._model.fit(x, y)
        self._model.sparsify()

    def eval(self, context, outcome):
        return self._model.score(map(self._feature_id, context),
                                self._outcome_id(outcome))
