from ..basictypes import utils



def corpus_tokenizer(file_names):
    files = map(open, file_names)
    counts = count_words(utils.concat(files))
    cut_off_set = utils.cut_off_set(counts, cut_off=1)
    for f in files:
        f.close()

    files = map(open, file_names)
    for sentence in utils.concat(files):
        for word in sentence.split()
