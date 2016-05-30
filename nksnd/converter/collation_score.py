#TODO uknown word!
def collation_score(lm, morphs):
    p = 1.0
    for i in range(len(morphs)):
        p1 = lm.eval(morphs[0:i-1], morphs[i])
        if p1 == 0:
            p = p * 0.01
        else:
            p = p * p1

    return p

def collation_sort(lm, morphs_list):
    scores = map(lambda moprhs: (morphs, collation_score(moprhs)), morphs_list)
    scores.sort(key=lambda entry: entry[1])
    return scores
