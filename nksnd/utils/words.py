# -*- coding: utf-8 -*-

def is_hiragana(string):
    for c in string:
        if u"ぁ" <= c <= u"ん":
            continue
        else:
            return False
    return True

def is_katakana(string):
    for c in string:
        if u"ァ" <= c <= u"ン":
            continue
        else:
            return False
    return True

def surface_pronoun(word):
    a = word.split('/')
    if len(a) != 2:
        print("Warning: mulformed wordkkci " + str(a))
    return (a[0], a[1])

def unknownword(word):
    s, p = surface_pronoun(word)
    if is_hiragana(s):
        kind = u'H'
    elif is_katakana(s):
        kind = u'K'
    elif s == p:
        kind = u'E'
    else:
        kind = u'O'
    if len(p) <= 6:
        length = len(p)
    else:
        length = 7
    return '_' + kind + str(length)
