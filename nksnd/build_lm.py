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
    parser.add_argument('inputs', nargs='+',
        help='input corpus')
    args = parser.parse_args()
    output_file = os.path.join(args.outdir, 'collation_lm')
    inputs = args.inputs

    files = map(open, inputs)
    lines = concat_files.concat(files)
    word_lists = map(lambda line: line.split(), lines)
    sentences = map(morph.Morph, word_lists)

    model = collation_lm.CollationLM()
    model.train(sentences)

    map(lambda f: f.close(), files)

    with open(output_file) as f:
        cPickle.dump(model, output_file, 2) 
