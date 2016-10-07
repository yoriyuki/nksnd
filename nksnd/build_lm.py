from lm import collocation_lm
from basictypes import concat_files
from basictypes import morph
import argparse
import os

def gen_data(lines):
    for line in lines:
        words = line.split()
        for i in range(len(words)):
            yield (map(morph.Morph, words[0:i-1]), morph.Morph(words[i]))

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='Generate colllation language model')
    parser.add_argument('-o', '--outdir',
        default='../data',
        help='output directory: default:../data')
    parser.add_argument('inputs', nargs='+',
        help='input corpus')
    args = parser.parse_args()
    output_file = os.path.join(args.outdir, 'collocation_lm')
    inputs = args.inputs

    files = map(open, inputs)
    lines = concat_files.concat(files)

    model = collocation_lm.CollocationLM()
    model.train(gen_data(lines))
    model.save(output_file)

    map(lambda f: f.close(), files)
