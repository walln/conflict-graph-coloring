import random
from algo.structures.graph import Graph

def generate_uniform_random_graph(num_vertices, num_edges):
    """
    This function generates a uniform random graph with the specified number of vertices and edges.

    A uniform random graph is a graph where each pair of distinct vertices has an equal probability
    of being connected by an edge. The resulting graph has a uniform degree distribution,
    with the degrees of vertices being approximately equal.

    Args:
        num_vertices (int): The number of vertices in the uniform random graph.
        num_edges (int): The total number of edges in the uniform random graph.

    Returns:
        A uniform random graph object.
    """

    assert num_edges <= num_vertices * (num_vertices - 1) // 2, \
          "Number of edges must be less than or equal to the maximum possible edges"

    graph = Graph(num_vertices)

    all_possible_edges = [(i, j) for i in range(num_vertices) for j in range(i + 1, num_vertices)]
    selected_edges = random.sample(all_possible_edges, num_edges)

    for edge in selected_edges:
        graph.add_edge(edge[0], edge[1])

    return graph
