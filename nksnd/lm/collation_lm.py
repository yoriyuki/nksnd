import genmaxent

class CollationLM:
    def __init__(self):
        self._model = GenMaxEntModel()

    def train(self, data):
        self._model.train(data)

    def eval(self, context, outcome):
        return self._model.eval(context, outcome)

    def save(self, file):
        self._model.save(file)

    def load(self, file):
        self._model.load(file)

def _gen_data(lines):
    for line in lines:
        words = line.split()
        for i in range(len(words)):
            yield map(Morph, words[0:i-1]), Morph(words)

if __name__ == "__main__":
    import argparse
    import os
    parser = argparse.ArgumentParser(
        description='Generate colllation language model')
    parser.add_argument('-o', '--outdir',
        default='../../data',
        help='output directory: default=../../data')
    parser.add_argument('inputs', nargs='?'
        help='input corpus')
    args = parser.parse_args()
    output_file = os.path.join(args.outdir, 'collation_lm')
    inputs = args.inputs

    import concat_filfes
    lines = concat(map(open, inputs))

    model = CollationLM()
    model.train(_gen_data(lines))
    model.save(output_file)

    map(lambda f: f.close(), inputs)
