from utils import numerics

def set_log_alpha(unigram_weight, bigram_weight, graph):
    for last_pos in range(graph.x_length):
        nodes = graph.nodes_list[last_pos]
        for node in nodes:
            prev_nodes = graph_nodes_list[node.start_pos]
            log_alpha = unigram_weight.get(node)
            for prev_node in prev_nodes:
                w = bigram_weight.get(prev_node, node)
                log_alpha = numerics.logsumexp(log_alpha, w)
            node.log_alpha = log_alpha
