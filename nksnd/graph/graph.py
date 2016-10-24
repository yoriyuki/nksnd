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
        graph = [[] for i in range(1 + len(s))]
        graph[0].append(BOS())
        graph[1 + len(s)].append(EOS(1 + len(s)))

        
