import math

def logsumexp(x, y):
    if x > y:
        return x + math.log(1 + math.exp(y-x))
    else:
        return x + math.log(1 + math.exp(x-y))

def clip(w, c):
    if w >= 0:
        if w > c:
            return w - c
        else:
            return 0
    else:
        return - clip(-w, c)
