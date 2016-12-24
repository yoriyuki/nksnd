from __future__ import print_function
from config import conversion_config
from lm import lm
import sys
import codecs
import argparse
stdin = codecs.getreader('utf-8')(sys.stdin)
stdout = codecs.getwriter('utf-8')(sys.stdout)

if __name__ == "__main__":

    lm = lm.LM()
    lm.load('../data/')

    parser = argparse.ArgumentParser(description='Convert kana')
    parser.add_argument('-n',
        default=1, type=int,
        help='number of candidates for reranking')
    parser.add_argument('-d', default=False, type=bool, help='debug mode')
    args = parser.parse_args()
    conversion_config.candidates_num = args.n

    for line in stdin:
        line = line.strip('\n')
        path = lm.convert(line)
        if args.d:
            viterbis = lm.n_candidates(line, args.n)
            for viterbi in viterbis:
                output = u' '.join(['(' + node.deep + "," + unicode(node.weight) + ')' for node in viterbi])
                print(output, file=stdout)
            output = u' '.join(['(' + node.deep + "," + unicode(node.weight) + ')' for node in path])
            print(output, file=stdout)
        else:
            output = u''.join([node.surface for node in path])
            print(output, file=stdout)
