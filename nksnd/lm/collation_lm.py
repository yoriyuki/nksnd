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
