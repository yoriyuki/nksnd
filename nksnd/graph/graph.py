from utils import words

class Node:
    def __init__(self, start_pos, key, surface, deep, cost):
        self.start_pos = start_pos
        self.deep = deep
        self.key = key
        self.cost = cost
        self.surface = surface

class BOS(Node):
    word = u"_BOS"
    def __init__(self):
        Node.__init__(self, -1, u"", u"", BOS.word, 0)

class EOS(Node):
    word = u"_EOS"
    def __init__(self, start_pos):
        Node.__init__(self, start_pos, u"", u"", EOS.word, 0)

class Graph:
    def __init__(self, d, string):
        self.x_length = len(string)
        self.nodes_list = [[] for i in range(3 + len(string))]
        self.nodes_list[0].append(BOS())

        for i in range(len(string)):
            sub = string[i:-1]
            prefixes = d.pronoun_prefixes(sub)
            for p in prefixes:
                for word, cost in d.get_from_pronoun(p):
                    s, p = words.surface_pronoun(word)
                    n = Node(i, p, s, word, cost)
                    self.nodes_list[i+len(p)].append(n)

            if prefixes == []:
                for j in range(i, len(string)):
                    if d.pronoun_prefixes(string[j:-1]) != []: #slow
                        rest = string[i:j]
                        if words.is_hiragana(rest):
                            s1 = rest
                            w1 = words.hiragana_unknown_word(len(rest))
                            c1 = d.get_unknownword_cost(w1)
                            w2 = words.katakana_unknown_word(len(rest))
                            s2 = words.katakana(rest)
                            c2 = d.get_unknownword_cost(w2)
                            self.nodes_list[j].append(Node(i, rest, s1, w1, c1))
                            self.nodes_list[j].append(Node(i, rest, s2, w2, c2))
                        else:
                            w1 = words.other_unknown_word(len(rest))
                            s1 = rest
                            c1 = d.get_unknownword_cost(w1)
                            w2 = words.other_unknown_word(len(rest))
                            s2 = words.latin(rest)
                            c2 = d.get_unknownword_cost(w2)
                            self.nodes_list[j].append(Node(i, rest, s1, w1, c1))
                            self.nodes_list[j].append(Node(i, rest, s2, w2, c2))

        self.nodes_list[1 + len(string)].append(EOS(len(string)))
