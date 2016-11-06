import heapq

def forward_dp(dictionary, graph):
    graph.node_list[0][0].f = 0
    for i in range(1, garph.x_length + 2):
        for node in graph.nodes_list[i]:
            score = float('-inf')
            best_prev = None
            for prev_node in graph.node_list[node.start_pos]:
                bigram_cost = dictionary.get_bigram_cost(prev_node.deep, node.deep)
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
    heapq.heappush(pq, [eos])

    while pq != [] and rest.length < n:
        cost, path = heapq.heappop(pq)
        front = path[0]
        if front.start_pos = -1:
            result.push(path)
        else:
            for prev_node in graph.nodes_list[front.start_pos]:
                path1 = [ prev_node ] + path
                bigram_cost = dictionary.get_bigram_cost(prev_node.deep, front.deep)
                cost1 = bigram_cost + front.cost + cost
                heapq.heappush(pq, (cost1, path1))

    return result
