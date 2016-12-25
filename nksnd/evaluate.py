from __future__ import print_function
import sys
import codecs
import argparse
stdout = codecs.getwriter('utf-8')(sys.stdout)
import numpy as np

def max3(x, y, z):
    return max(max(x, y), z)

def lcs(s1, s2):
    m = len(s1)
    n = len(s2)

    t = np.zeros((n + 2, m + 2), dtype=int)

    for j in range(1, n + 1):
        for i in range(1, m + 1):
            is_same = 0
            if s1[i-1] == s2[j-1]:
                is_same = 1
            t[j, i] = max3(t[j-1, i + 1] + is_same, t[j - 1][i], t[j][i - 1])

    return t[n, m]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Evaluate conversion results')
    parser.add_argument('originals',help='original texts')
    parser.add_argument('converted_texts',help='converted texts')
    parser.add_argument('--verbose', '-v', type=bool, help='verbose output')
    args = parser.parse_args()

    lcs_sum = 0
    conv_sum = 0
    orig_sum = 0
    sentences = 0
    correct_sentences = 0

    with open(args.originals, 'r') as originals:
        with open(args.converted_texts, 'r') as converted_texts:
            origs = codecs.getreader('utf-8')(originals)
            convs = codecs.getreader('utf-8')(converted_texts)

            for orig, conv in zip(origs, convs):
                orig.strip(' \n')
                conv.strip(' \n')
                sentences += 1
                if orig == conv:
                    correct_sentences += 1
                lcs_len = lcs(orig, conv)
                if args.verbose:
                    print(u'\"{}\", \"{}\", {}'.format(orig, conv, lcs_len), file=stdout)
                lcs_sum += lcs_len
                conv_sum += len(conv)
                orig_sum += len(orig)

            precision = lcs_sum/float(conv_sum)
            recall = lcs_sum/float(orig_sum)
            f_value = 2 * precision * recall / (precision + recall)
            sentence_accuracy = float(correct_sentences) / sentences
            if args.verbose:
                print(u',,,{},{},{},{}'.format(precision, recall, f_value, sentence_accuracy), file=stdout)
            else:
                print(u'{},{},{},{}'.format(precision, recall, f_value, sentence_accuracy), file=stdout)
