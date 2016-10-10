from lm import collocation_lm
import sys
import codecs
stdin = codecs.getreader('utf-8')(sys.stdin)
stdout = codecs.getwriter('utf-8')(sys.stdout)

lm = collocation_lm.CollocationLM()
lm.load('../data/')

for line in stdin:
    sentence = line.split()
    print line.rstrip('\n') + "," + str(lm.collocation_score(sentence))
