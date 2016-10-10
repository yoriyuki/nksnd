from lm import collocation_lm
import argparse
import os

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='Generate colllation language model')
    parser.add_argument('-o', '--outdir',
        default='../data',
        help='output directory: default:../data')
    parser.add_argument('inputs', nargs='+',
        help='input corpus')
    args = parser.parse_args()
    inputs = args.inputs

    model = collocation_lm.CollocationLM()
    model.train(inputs)
    model.save(args.outdir)
