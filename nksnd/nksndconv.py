from __future__ import print_function
import sys
import codecs
import argparse
from os import path as pth

import sexpdata as sexp

from nksnd.utils import words as wd
from nksnd.config import slm_config
from nksnd.lm import lm as langmodel

def main():

        lm = langmodel.LM()
        lm.load(pth.join(pth.dirname(__file__), '../data'))

        parser = argparse.ArgumentParser(description='Convert kana')
        parser.add_argument('-d', default=False, type=bool, help='debug mode')
        parser.add_argument('--max_escape_rate', type=float,
            default = slm_config.max_escape_rate,
            help='Maximal escape rate')
        parser.add_argument('--additive_smoothing', type=float,
            default = slm_config.additive_smoothing,
            help='Smoothing constant for additive smoothing')
        parser.add_argument('-m', '--mode', default='plain', help='IO mode, plain=plain text, sexp=S expression')

        args = parser.parse_args()
        slm_config.max_escape_rate = args.max_escape_rate
        slm_config.additive_smoothing = args.additive_smoothing

        if args.mode == 'plain':
            for line in sys.stdin:
                line = line.strip('\n')
                path = lm.convert(line)
                output = u''.join([node.surface for node in path])
                print(output, file=sys.stdout)

        elif args.mode == 'sexp':
            for line in sys.stdin:
                cmd = sexp.loads(line)
                if cmd[0] == 'best-path':
                    path = lm.convert(cmd[1])
                    words = [wd.surface_pronoun(node.deep) for node in path]
                    output = sexp.dumps(words)
                    print(output, file=sys.stdout)
                elif cmd[0] == 'list-candidates':
                    words = [wd.compose(t[0], t[1]) for t in cmd[1]]
                    candidates = lm.next_candidates(words, cmd[2], cmd[3])
                    candidates = list(map(wd.surface_pronoun, candidates))
                    output = sexp.dumps(candidates)
                    print(output, file=sys.stdout)
                else:
                    continue

        else:
            return -1

if __name__ == "__main__":
    main()
