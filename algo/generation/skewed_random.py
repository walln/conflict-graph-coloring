import random
from algo.structures.graph import Graph

def generate_skewed_graph(num_vertices, num_edges):
    """
    This function generates a skewed graph with the specified number of vertices and edges.

    A skewed graph is a graph in which the degree distribution is not uniform,
    with some vertices having much higher degrees than others.
    This results in a graph with an uneven distribution of edges among vertices.

    Args:
        num_vertices (int): The number of vertices in the skewed graph.
        num_edges (int): The total number of edges in the skewed graph.

    Returns:
        A skewed graph object.
    """
    assert num_edges <= num_vertices * (num_vertices - 1) // 2, \
        "Number of edges must be less than or equal to the maximum possible edges"

    graph = Graph(num_vertices)

    [(i, j) for i in range(num_vertices) for j in range(i + 1, num_vertices)]

    # Create a linearly decreasing probability distribution
    weights = [num_vertices - i for i in range(num_vertices)]

    # Sample vertex pairs with the skewed distribution
    selected_edges = set()
    while len(selected_edges) < num_edges:
        vertex_pair = tuple(random.choices(range(num_vertices), weights, k=2))
        if vertex_pair[0] != vertex_pair[1] and (vertex_pair[1], vertex_pair[0]) not in selected_edges:
            selected_edges.add(vertex_pair)

    # Add the selected edges to the graph
    for edge in selected_edges:
        graph.add_edge(edge[0], edge[1])

    return graph
