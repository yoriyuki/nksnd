from __future__ import print_function
from lm import lm
import sys
import codecs
stdin = codecs.getreader('utf-8')(sys.stdin)
stdout = codecs.getwriter('utf-8')(sys.stdout)

lm = lm.LM()
lm.load('../data/')

for line in stdin:
    print(lm.convert(line), file=stdout)
