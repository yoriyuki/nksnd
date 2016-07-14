from converter import collation_score
from lm import collation_lm
from basictypes import morph
import sys
import pickle

lm = pickle.load(open('../data/collation_lm', 'rb'))

mrphs_list=[]
lines = []
for line in sys.stdin:
    lines.append(line.strip())
    words = line.split()
    mrphs_list.append(list(map(morph.Morph, words)))

prob_list = lm.predict_proba(mrphs_list)

for i in range(len(mrphs_list)):
    print("\"" + lines[i] + "\"," + str(prob_list[i]))
