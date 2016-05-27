from maxent import MaxentModel

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
            self.__add_event(context, outcome)
        self.__end_add_event()
        self.__train()

    def save(self, name):
        self.__m.save(name)

    def load(self, name):
        self.__m.load(name)

    def eval(self, context, outcome):
        self.__m.eval(context, outcome)

    def eval_all(self, context):
        self.__m.eval_all(context)

def _test():
    model = GenMaxEntModel()
    model.train([(['1', '2'], '3'), (['1', '3'], '4')])
    print model.eval(['1', '2'], '3')
    print model.eval(['1', '2'], '4')

if __name__ == "__main__":
    _test()
