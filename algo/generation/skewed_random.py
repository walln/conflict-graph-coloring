from algo.structures.graph import Graph
import random


def generate_skewed_random_graph(num_vertices, num_conflicts) -> Graph:
    """
    This function generates a random undirected graph with a skewed random
    distribution for selecting vertex pairs.

    Args:
        num_vertices (int): The number of vertices in the graph.
        num_conflicts (int): The number of distinct edges to add to the graph.

    Returns:
        A random undirected graph object.
    """

    assert num_conflicts <= (num_vertices*(num_vertices-1))/2, \
        "Number of edges cannot be greater than the maximum possible number of edges"

    graph = Graph(num_vertices)

    existing_edge_count = 0
    existing_edges = set(graph.edges())

    # Calculate degree distribution
    degree_sum = sum(range(1, num_vertices+1))
    probs = [(num_vertices-i) / degree_sum for i in range(num_vertices)]

    # Add edges
    while existing_edge_count < num_conflicts:
        v1 = random.choices(range(num_vertices), weights=probs)[0]
        v2 = random.choices(range(num_vertices), weights=probs)[0]

        if v1 != v2:
            if (v1, v2) not in existing_edges and (v2, v1) not in existing_edges:
                graph.add_edge(v1, v2)
                graph.add_edge(v2, v1)
                existing_edges.add((v1, v2))
                existing_edges.add((v2, v1))
                existing_edge_count += 1

    return graph
