# -*- coding: utf-8 -*-

import jaconv
import romkan

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
    a = word.split(u'/')
    if len(a) != 2:
        print("Warning: mulformed wordkkci " + str(a))
    return (a[0], a[1])

def unknownword(word):
    if is_unknown(word):
        return word
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
    return u'_' + kind + unicode(str(length))


def replace_word(known_words, word):
    if word in known_words:
        return word
    else:
        return unknownword(word)

def literal_word(string):
    return string + u'/' + string

def katakana_word(string):
    return jaconv.hira2kata(string) + u'/' + string

def latin_word(string):
    return romkan.to_roma(string) + u'/' + string

def is_unknown(word):
    return not u'/' in word

def unknown_length(word):
    return word[2]

def compose_bigram_key(word1, word2):
    return word1 + u' ' + word2

def is_bigram_key(key):
    return u' ' in key

def decompose_bigram_key(key):
    a = key.split(u' ')
    return a[0], a[1]
