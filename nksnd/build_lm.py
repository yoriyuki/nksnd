from lm import lm
from config import lmconfig, parallel_config, learn_config, slm_config
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
    parser.add_argument('--crf_processes', type=int,
        default = parallel_config.processes,
        help='number of processes used for learning CRF')
    parser.add_argument('--crf_chunk', type=int,
        default = parallel_config.chunk_size,
        help='size of chunk processed sent to each learning process')
    parser.add_argument('--max_escape_rate', type=float,
        default = slm_config.max_escape_rate,
        help='Maximal escape rate')
    parser.add_argument('--additive_smoothing', type=float,
        default = slm_config.additive_smoothing,
        help='Smoothing constant for additive smoothing')
    parser.add_argument('--skip_collocation', type=bool,
        default = False,
        help='Learn collocation?')
    parser.add_argument('inputs', nargs='+',
        help='corpus')
    args = parser.parse_args()
    lmconfig.iteration = args.iter
    lmconfig.gaussian = args.gaussian
    lmconfig.unknownword_threshold = args.unknownword_threshold
    lmconfig.eta = args.crf_fobos_eta
    lmconfig.regularization_factor = args.crf_fobos_c
    parallel_config.processes = args.crf_processes
    parallel_config.chunk_size = args.crf_chunk
    slm_config.max_escape_rate = args.max_escape_rate
    slm_config.additive_smoothing = args.additive_smoothing
    learn_config.learn_collocation = not args.skip_collocation
    inputs = args.inputs

    model = lm.LM()
    model.train(inputs)
    model.save(args.outdir)
