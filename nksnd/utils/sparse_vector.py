from utils import numerics

class SparseVector:
    def __init__(self, dic):
        self.dict = dic

    def set(self, key, val):
        self.dict[key] = val

    def get(self, key):
        if key in self.dict:
            return self.dict[key]
        else:
            return 0

    def logsumexp(self, val):
        for key in self._dict:
            self.dict[key] = numerics.logsumexp(self.dict[key], val)
        return self

    def __iadd__(self, sv):
        for key, val in sv.iteritems():
            if key in self._dict:
                self.dict[key] = self.dict[key] + val
            else:
                self.dict[key] = val
        return self
