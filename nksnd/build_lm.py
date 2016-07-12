from lm import collation_lm
from basictypes import utils
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
    parser.add_argument('-f', '--featurenum', default=1000, help='number of features', type=int)
    parser.add_argument('-c', '--clusternum', default=1000, help="number of outcome clusters", type=int)
    parser.add_argument('inputs', nargs='+',
        help='input corpus')
    args = parser.parse_args()
    output_file = os.path.join(args.outdir, 'collation_lm')
    inputs = args.inputs
    penalty = args.penalty
    solver = args.solver
    max_iter = args.max_iter
    feature_num = args.featurenum
    outcome_num = args.clusternum

    model = collation_lm.CollationLM(penalty=penalty, solver=solver,
        max_iter=max_iter, feature_num=feature_num, outcome_num=outcome_num)
    model.train(inputs)

    with open(output_file, 'wb') as f:
        cPickle.dump(model, f, 2)
