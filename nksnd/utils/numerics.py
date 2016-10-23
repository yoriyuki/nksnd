import math

def logsumexp(x, y):
    if x > y:
        return x + math.log(1 + math.exp(y-x))
    else:
        return x + math.log(1 + math.exp(x-y))
