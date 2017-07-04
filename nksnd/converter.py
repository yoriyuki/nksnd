from __future__ import print_function
from config import slm_config
from lm import lm
import sys
import codecs
import argparse

if __name__ == "__main__":

    lm = lm.LM()
    lm.load('../data/')

    parser = argparse.ArgumentParser(description='Convert kana')
    parser.add_argument('-d', default=False, type=bool, help='debug mode')
    parser.add_argument('--max_escape_rate', type=float,
        default = slm_config.max_escape_rate,
        help='Maximal escape rate')
    parser.add_argument('--additive_smoothing', type=float,
        default = slm_config.additive_smoothing,
        help='Smoothing constant for additive smoothing')

    args = parser.parse_args()
    slm_config.max_escape_rate = args.max_escape_rate
    slm_config.additive_smoothing = args.additive_smoothing

    for line in sys.stdin:
        line = line.strip('\n')
        path = lm.convert(line)
        output = u''.join([node.surface for node in path])
        print(output, file=sys.stdout)
