from utils import genmaxent
import os

def features(context):
    length = len(context)
    if length > 2:
        collocations = [':' + word for word in context[0:length-3]]
        return collocations + ['2' + context[-2], '1' + context[-1]]
    elif length == 2:
        return ['2' + context[0], '1' + context[1]]
    elif length == 1:
        return ['1' + context[0]]
    else:
        return []

def gen_data(words_seq):
    for words in words_seq:
        for i in range(len(words)):
            yield (features(words[0:i-1]), words[i])

class CollocationLM:
    def __init__(self):
        self._model = genmaxent.GenMaxEntModel()

    def _eval(self, context, outcome):
        return self._model.eval(context, outcome)

    def train(self, words_seq):
        data = gen_data(words_seq)
        self._model.train(data, cutoff=1)

    def score(self, words):
        p = 1.0
        for i in range(len(words)):
            p = p * self._eval(features(words[0:i-1]), words[i])
        return p

    def save(self, path):
        param_filename = os.path.join(path, 'collocation_param')
        self._model.save(param_filename)

    def load(self, path):
        param_filename = os.path.join(path, 'collocation_param')
        self._model.load(param_filename)
