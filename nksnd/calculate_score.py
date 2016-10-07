from converter import collocation_score
from lm import collocation_lm
from basictypes import morph
import sys

lm = collocation_lm.CollocationLM()
lm.load('../data/collocation_lm')

while True:
    line = raw_input()
    words = line.split()
    morphs = map(morph.Morph, words)
    print collocation_score.collocation_score(lm, morphs)
