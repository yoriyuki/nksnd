from converter import collation_score
from lm import collation_lm
from basictypes import morph
import sys
import cPickle

lm = cPickle.load('../data/collation_lm')

while True:
    line = raw_input()
    words = line.split()
    morphs = map(morph.Morph, words)
    print collation_score.collation_score(lm, morphs)
