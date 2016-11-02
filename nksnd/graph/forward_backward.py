from utils import numerics

def set_log_alpha(weights, graph):
    for last_pos in range(graph.x_length):
        for node in graph.nodes_list[last_pos]:
            prev_nodes = graph_nodes_list[node.start_pos]
            node.log_alpha = weights.get_unigram(node.word)
            for prev_node in prev_nodes:
                w = weights.get_bigram(prev_node.word, node.word)
                node.log_alpha =
                    numerics.logsumexp(node.log_alpha, prev_node.log_alphe + w)

def set_log_beta(unigram_weight, bigram_weight, graph):
    for last_pos in range(graph.x_length):
        for node in graph.nodes_list[last_pos]:
            node.log_beta = weights.get_unigram(node.word)

    for last_pos in range(graph.x_length, 0, -1):
        for node in graph.nodes_list[last_pos]:
            prev_nodes = graph_nodes_list[node.start_pos]
            for prev_node in prev_nodes:
                w = weights.get_bigram(prev_node.word, node.word)
                prev_node.log_beta =
                    numerics.logsumexp(prev_node.log_beta, node.log_beta + w)
