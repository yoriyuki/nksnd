def concat(files):
    for file in files:
        for line in file:
            yield line

def count_words(sentences):
    counts = {}
    for sentence in sentences:
        for word in sentence:
            if word in counts:
                counts[word] += 1
            else:
                count[word] = 1
    return counts

def cut_off_set(counts, cut_off=1):
    return { x for x in counts.keys() if counts[x] > cut_off }

def reverse_map(dict):
    return { v: k for (k ,v) in dict.items()}

def is_hiragana(string):
    for c in string:
        if "ぁ" <= ch <= "ん":
            continue
        else:
            return False
    return True

def is_katakana(string):
    for c in string:
        if "ァ" <= ch <= "ン":
            continue
        else:
            return False
    return True
