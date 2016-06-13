from ..basictypes import utils
from ..basictypes import morph

def _morph_from_word(word, cut_off_set):
    if word in cut_off_set:
        morph.Morph(word)
    else:
        morph.UnknownMorph(word)

def cut_off_set(files):
    sentences = (line.split() for line in utils.concat(files))
    counts = count_words(sentences)
    cut_off_set = utils.cut_off_set(counts, cut_off=1)
    for f in files:
        f.close()
    return cut_off_set

def corpus_tokenizer(files, cut_off_set):
    sentences = (line.split() for line in utils.concat(files))
    for sentence in sentences:
        yield [_morph_from_word(word, cut_off_set) for word in sentence]
