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

def escapeword(word):
    if word[0] == '_':
        return '_' + word
    else:
        return word

def unknownword(word):
    if is_hiragana(word):
        kind = u'H'
    elif is_katakana(word):
        kind = u'K'
    else:
        kind = u'O'
    if len(word) <= 6:
        length = len(word)
    else:
        length = 7
    return '_' + kind + str(length)
