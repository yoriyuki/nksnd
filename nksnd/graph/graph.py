class Node:
    def __init__(self, start_pos, word):
        self.start_pos = start_pos
        self.word = word
        self.prev_nodes = prev_nodes

class BOS(Node):
    def __init__(self):
        Node.__init__(None, None)

class EOS(Node):
    def __init__(self, start_pos):
        Node.__init__(start_pos, None)

class Graph:
    def __init__(self, dict, string):
        self.nodes_list = [[] for i in range(1 + len(string))]
        self.nodes_list[0].append(BOS())

        for i in range(len(string)):
            sub = string[i:-1]
            prefixes = dict.preficxes(sub)
            for key in prefixes:
                for word in dict[key]:
                    self.nodes_list[i+len(key)].append(Node(i, word)

            if prefixes == []:
                for j in range(i, len(string)):
                    if dict.prefixes(string[j:-1]) != []: #slow
                        s = string[i:j]
                        self.nodes_list[j].append(Node(i, literal_word(s)))
                        self.nodes_list[j].append(Node(i, katakana_word(s))
                        self.nodes_list[j].append(Node(i, latin_word(s)))

        self.nodes_list.append(EOS(1 + len(s)))
