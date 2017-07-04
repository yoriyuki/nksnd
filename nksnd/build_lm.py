from lm import lm
from config import lmconfig, slm_config
import argparse
import os

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='Generate a language model')
    parser.add_argument('-o', '--outdir',
        default='../data',
        help='output directory: default:../data')
    parser.add_argument('--unknownword_threshold', type=int,
        default = lmconfig.unknownword_threshold,
        help='threshold which we consider a word in corpus as an unknownword')
    parser.add_argument('inputs', nargs='+',
        help='corpus')
    args = parser.parse_args()
    lmconfig.unknownword_threshold = args.unknownword_threshold
    inputs = args.inputs

    model = lm.LM()
    model.train(inputs)
    model.save(args.outdir)
