import genmaxent

class CollationModel:
    def __init__(self):
        self._model = GenMaxEntModel()

    def train(self, data):
        self._model.train(data)

    def eval(self, context, outcome):
        return self._model.eval(context, outcome)
