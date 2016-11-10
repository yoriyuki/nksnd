from utils import numerics

def set_log_alpha(d, graph):
    for last_pos in range(2 + graph.x_length):
        for node in graph.nodes_list[last_pos]:
            prev_nodes = graph.nodes_list[node.start_pos]
            node.log_alpha = node.weight
            for prev_node in prev_nodes:
                w = d.get_bigram_weight(prev_node.deep, node.deep)
                node.log_alpha = numerics.logsumexp(node.log_alpha, prev_node.log_alpha + w)

def set_log_beta(d, graph):
    for last_pos in range(graph.x_length + 2):
        for node in graph.nodes_list[last_pos]:
            node.log_beta = node.weight

    for last_pos in range(graph.x_length + 2, 0, -1):
        for node in graph.nodes_list[last_pos]:
            prev_nodes = graph.nodes_list[node.start_pos]
            for prev_node in prev_nodes:
                w = d.get_bigram_weight(prev_node.deep, node.deep)
                prev_node.log_beta = numerics.logsumexp(prev_node.log_beta, node.log_beta + w)
