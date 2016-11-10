from __future__ import print_function
import heapq
import copy
import codecs, sys
stdout = codecs.getwriter('utf-8')(sys.stdout)

def forward_dp(dictionary, graph):
    graph.nodes_list[0][0].f = 0
    for i in range(1, graph.x_length + 2):
        for node in graph.nodes_list[i]:
            score = float('-inf')
            best_prev = None
            for prev_node in graph.nodes_list[node.start_pos]:
                bigram_cost = dictionary.get_bigram_cost(prev_node.deep, node.deep)
#                print(node.surface, node.cost, bigram_cost)
                current_score = prev_node.f + bigram_cost + node.cost
                if current_score > score:
                    score = current_score
                    best_prev = prev_node
            node.best_prev = best_prev
            node.f = score

def backward_a_star(dictionary, graph, n):
    result = []
    pq = []
    eos = graph.nodes_list[graph.x_length + 1][0]
    eos.g = 0
    heapq.heappush(pq, (0, eos))

    while pq != [] and len(result) < n:
        cost, front = heapq.heappop(pq)
        if front.start_pos == -1:
            result.append(front)
        else:
            for prev_node in graph.nodes_list[front.start_pos]:
                bigram_cost = - dictionary.get_bigram_cost(prev_node.deep, front.deep)
                prev_node.g = bigram_cost + front.g - cost
                new_front = copy.copy(prev_node)
    #            print(new_front.surface, new_front.g, new_front.f, file=stdout)
                new_front.next = front
                heapq.heappush(pq, (- prev_node.f - prev_node.g, new_front))

    n_best = []
    for node in result:
        nodes = []
        while node != eos:
            nodes.append(node)
            node = node.next
        n_best.append(nodes)

    return n_best
