class Node:
    def __init__(self, start_pos, word):
        self.start_pos = start_pos
        self.word = word

class BOS(Node):
    def __init__(self):
        Node.__init__(None, None)

class EOS(Node):
    def __init__(self, start_pos):
        Node.__init__(start_pos, None)

class Graph:
    def __init__(self, dict, string):
        graph = []
        graph.append([BOS()])

        for i in range(len(string)):
            sub = string[i:-1]
            nodes = [Node(i, word) for word in dict.iter_prefixes(sub)]
            if nodes == []:
            for j in range(i, len(string)):
                if dict.prefixes(string[j:-1]) != []:
                    s = string[i:j]
                    nodes = [
                        Node(i, literal_word(s)),
                        Node(i, katakana_word(s)),
                        Node(i, latin_word(s))
                    ]
                    break
            graph.append(nodes)

        graph.append(EOS(1 + len(s)))
