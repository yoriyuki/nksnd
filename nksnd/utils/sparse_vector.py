import math
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

    def logsumexp(self, sv):
        for key in sv.dict:
            self.set(key) = numerics.logsumexp(self.get(key), sv.get(key))
        return self

    def __iadd__(self, sv):
        for key, val in sv.iteritems():
            if key in self._dict:
                self.dict[key] = self.dict[key] + val
            else:
                self.dict[key] = val
        return self

    def minusexp(self, sv):
        for key in sv.dict:
            self.set(key) = self.get(key) - math.exp(sv.get(key))
        return self
