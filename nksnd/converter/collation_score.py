def collation_score(lm, morphs):
    p = 1.0
    for i in range(len(morphs)):
        p = p * lm.eval(morphs[0:i-1], morphs[i])
    return p

def collation_sort(lm, morphs_list):
    scores = map(lambda moprhs: (morphs, collation_score(moprhs)), morphs_list)
    scores.sort(key=lambda entry: entry[1])
    return scores
