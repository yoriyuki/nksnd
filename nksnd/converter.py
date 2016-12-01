from __future__ import print_function
from lm import lm
import sys
import codecs
import argparse
stdin = codecs.getreader('utf-8')(sys.stdin)
stdout = codecs.getwriter('utf-8')(sys.stdout)

lm = lm.LM()
lm.load('../data/')

parser = argparse.ArgumentParser(description='Convert kana')
parser.add_argument('-n',
    default=1, type=int,
    help='number of candidates')
parser.add_argument('-d', default=False, type=bool, help='debug mode')
args = parser.parse_args()

for line in stdin:
    paths = lm.n_candidates(line, args.n)
    for path in paths:
        if args.d:
            output = u' '.join(['(' + node.deep + "," + unicode(node.weight) + ')' for node in path])
            print(output, file=stdout)
        else:
            output = u''.join([node.surface for node in path])
            print(output, file=stdout)
