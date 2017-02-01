from __future__ import print_function
from lm import lm
import sys
import codecs
stdin = codecs.getreader('utf-8')(sys.stdin)
stdout = codecs.getwriter('utf-8')(sys.stdout)


lm = lm.LM()
lm.load('../data/')

for line in stdin:
    line = line.rstrip('\n')
    words = line.split(' ')
    prediction = lm.collocationLM.predict(words, 10)
    print(line, file=stdout)
    total_p = 0.0
    for word, p in prediction:
        print(word + ": " + str(p), file=stdout)
        total_p += p
    print("total:" + str(total_p), file=stdout)
