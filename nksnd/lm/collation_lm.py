from basictypes import genmaxent

class CollationLM:
    def __init__(self):
        self._model = genmaxent.GenMaxEntModel()

    def train(self, data):
        self._model.train(data)

    def eval(self, context, outcome):
        return self._model.eval(context, outcome)

    def save(self, file):
        self._model.save(file)

    def load(self, file):
        self._model.load(file)
