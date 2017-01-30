from __future__ import print_function
from lm import lm
import sys
import codecs
stdin = codecs.getreader('utf-8')(sys.stdin)
stdout = codecs.getwriter('utf-8')(sys.stdout)


lm = lm.LM()
lm.load('../data/')
collationLM_sum = 0
ngramLM_sum = 0
count = 0

for line in stdin:
    sentence = line.split(' ')
    col_score = lm.collocationLM.score(sentence, debug=False)
    slm_score = lm.slm_score(sentence)
    print(line.rstrip('\n') + "," + str(col_score) + "," + str(slm_score), file=stdout)
    collationLM_sum += col_score
    ngramLM_sum += slm_score
    count += 1

print("cross_entropy, " + str(collationLM_sum / count) + "," + str(ngramLM_sum / count))
