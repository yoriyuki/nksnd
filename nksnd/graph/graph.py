class Node:
    def __init__(self, start_pos, key, word):
        self.start_pos = start_pos
        self.word = word
        self.key = key

class BOS(Node):
    word = "_BOS"
    def __init__(self):
        Node.__init__(None, "", BOS.word)

class EOS(Node):
    word = "_EOS"
    def __init__(self, start_pos):
        Node.__init__(start_pos, "", EOS.word)

class Graph:
    def __init__(self, dict, string):
        self.x_length = len(string)
        self.nodes_list = [[] for i in range(1 + len(string))]
        self.nodes_list[0].append(BOS())

        for i in range(len(string)):
            sub = string[i:-1]
            prefixes = dict.preficxes(sub)
            for key in prefixes:
                for word in dict[key]:
                    self.nodes_list[i+len(key)].append(Node(i, key, word)

            if prefixes == []:
                for j in range(i, len(string)):
                    if dict.prefixes(string[j:-1]) != []: #slow
                        s = string[i:j]
                        self.nodes_list[j].append(Node(i, s, literal_word(s)))
                        self.nodes_list[j].append(Node(i, s, katakana_word(s))
                        self.nodes_list[j].append(Node(i, s, latin_word(s)))

        self.nodes_list.append(EOS(1 + len(s)))
