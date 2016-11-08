from lm import lm
import sys
import codecs
stdin = codecs.getreader('utf-8')(sys.stdin)
stdout = codecs.getwriter('utf-8')(sys.stdout)

lm = lm.LM()
lm.load('../data/')

for line in stdin:
    line.strip('\n ')
    print(lm.convert(line))
