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
                    s, p = surface_pronoun(word)
                    n = Node(i, key, s, word, cost)
                    self.nodes_list[i+len(key)].append(n)

            if prefixes == []:
                for j in range(i, len(string)):
                    if dict.prefixes(string[j:-1]) != []: #slow
                        s = string[i:j]
                        if words.is_hiragana(s):
                            w2 = words.katakana_unknown_word(len)
                            s2 = words.katakana(s)
                            c1 = d.unknownword_cost(w2)
                            self.nodes_list[j].append(Node(i, s1, w1, c1)
                            self.nodes_list[j].append(Node(i, s2, w2, c2)
                        else:
                            w1 = words.other_unknown_word(len)
                            s1 = s
                            c1 = d.unknownword_cost(w1)
                            w2 = words.other_unknown_word(len)
                            s2 = words.latin(s)
                            c1 = d.unknownword_cost(w2)
                            self.nodes_list[j].append(Node(i, s1, w1, c1)
                            self.nodes_list[j].append(Node(i, s2, w2, c2)

        self.nodes_list[1 + len(string)].append(EOS(len(string)))
