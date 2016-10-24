class Node:
    def __init__(self, start_pos, word, prev_nodes):
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
        graph = [[] for i in range(1 + len(string))]
        graph[0].append(BOS())

        for i in range(len(string)):
            sub = string[i:-1]
            prefixes = dict.preficxes(sub)
            for key in prefixes:
                for word in dict[key]:
                    graph[i+len(key)].append(Node(i, word, graph[i]))

            if prefixes == []:
                for j in range(i, len(string)):
                    if dict.prefixes(string[j:-1]) != []: #slow
                        s = string[i:j]
                        graph[j].append(Node(i, literal_word(s), graph[i]))
                        graph[j].append(Node(i, katakana_word(s), graph[i])
                        graph[j].append(Node(i, latin_word(s), graph[i]))

        graph.append(EOS(1 + len(s)))
