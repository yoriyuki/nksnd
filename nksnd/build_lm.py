from lm import lm
from config import lmconfig
import argparse
import os

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='Generate colllation language model')
    parser.add_argument('-o', '--outdir',
        default='../data',
        help='output directory: default:../data')
    parser.add_argument('--iter', type=int, default = lmconfig.iteration,
        help='iteration number of lbfgs optimization')
    parser.add_argument('--gaussian', type=float, default = lmconfig.gaussian,
        help='gaussian prior')
    parser.add_argument('--unknownword_threshold', type=int,
        default = lmconfig.unknownword_threshold,
        help='threshold which we consider a word in corpus as an unknownword')
    parser.add_argument('--crf_fobos_eta', type=float,
        default = lmconfig.eta,
        help='learning rate of CRF fobos learning algorithm')
    parser.add_argument('--crf_fobos_c', type=float,
        default = lmconfig.regularization_factor,
        help='L1 rugularization constant of CRF fobos learning algorithm')
    parser.add_argument('inputs', nargs='+',
        help='corpus')
    args = parser.parse_args()
    lmconfig.iteration = args.iter
    lmconfig.gaussian = args.gaussian
    lmconfig.unknownword_threshold = args.unknownword_threshold
    lmconfig.eta = args.crf_fobos_eta
    lmconfig.regularization_factor = args.crf_fobos_c
    inputs = args.inputs

    model = lm.LM()
    model.train(inputs)
    model.save(args.outdir)
