from lm import collation_lm
from basictypes import concat_files
from basictypes import morph
import argparse
import os
import cPickle

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='Generate colllation language model')
    parser.add_argument('-o', '--outdir',
        default='../data',
        help='output directory: default:../data')
    parser.add_argument('-p', '--penalty', default='l2', help='penalty')
    parser.add_argument('-s', '--solver', default='lbfgs', help='solver')
    parser.add_argument('-m', '--max_iter', default=10, type=int,
        help='max iteraion')
    parser.add_argument('inputs', nargs='+',
        help='input corpus')
    args = parser.parse_args()
    output_file = os.path.join(args.outdir, 'collation_lm')
    inputs = args.inputs
    penalty = args.penalty
    solver = args.solver
    max_iter = args.max_iter

    files = map(open, inputs)
    lines = concat_files.concat(files)
    word_lists = map(lambda line: line.split(), lines)
    sentences = map(lambda word_list: map(morph.Morph, word_list), word_lists)

    model = collation_lm.CollationLM(penalty=penalty, solver=solver,
        max_iter=max_iter)
    model.train(sentences)

    map(lambda f: f.close(), files)

    with open(output_file, 'wb') as f:
        cPickle.dump(model, f, 2)
