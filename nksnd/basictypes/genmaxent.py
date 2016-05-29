from maxent import MaxentModel

def get_features(context):
    return map(lambda data: data.key(), context)

class GenMaxEntModel:
    def __init__(self):
        self.__m = MaxentModel()

    def __begin_add_event(self):
        self.__m.begin_add_event()

    def __end_add_event(self):
        self.__m.end_add_event()

    def __add_event(self, context, outcome):
        self.__m.add_event(context, outcome)

    def __train(self):
        self.__m.train()

    def train(self, events):
        self.__begin_add_event()
        for event in events:
            context, outcome = event
            features = get_features(context)
            self.__add_event(features, outcome.key())
        self.__end_add_event()
        self.__train()

    def save(self, name):
        self.__m.save(name)

    def load(self, name):
        self.__m.load(name)

    def eval(self, context, outcome):
        return self.__m.eval(get_features(context), outcome.key())


def _test():
    class Data:
        def __init__(self, data):
            self._data = data
        def key(self):
            return self._data
    model = GenMaxEntModel()
    model.train([([Data('1'), Data('2')], Data('3')),
                ([Data('1'), Data('3')], Data('4'))])
    print(model.eval([Data('1'), Data('2')], Data('3')))
    print(model.eval([Data('1'), Data('2')], Data('4')))

if __name__ == "__main__":
    _test()
