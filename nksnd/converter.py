from __future__ import print_function
from config import conversion_config, slm_config
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
    parser.add_argument('--max_escape_rate', type=float,
        default = slm_config.max_escape_rate,
        help='Maximal escape rate')
    parser.add_argument('--additive_smoothing', type=float,
        default = slm_config.additive_smoothing,
        help='Smoothing constant for additive smoothing')

    args = parser.parse_args()
    conversion_config.candidates_num = args.n
    slm_config.max_escape_rate = args.max_escape_rate
    slm_config.additive_smoothing = args.additive_smoothing

    for line in stdin:
        line = line.strip('\n')
        if args.d:
            path_and_scores = lm.convert(line, args.n)
            for path, score in path_and_scores:
                output = u''.join([node.surface for node in path])
                print(output, score, file=stdout)
        else:
            path, score = lm.convert(line, args.n)[0]
            output = u''.join([node.surface for node in path])
            print(output, file=stdout)
