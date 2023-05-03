import random
from algo.structures.graph import Graph

def generate_cyclic_graph(num_vertices, num_edges) -> Graph:
    """
    This function generates a cyclic graph (at least 1 cycle in the graph)
    with the specified number of vertices and edges.

    A cyclic graph is a graph containing at least one graph cycle. In this function,
    the generated graph will have a specified number of vertices and edges, with each
    vertex being part of at least one cycle.

    Args:
        num_vertices (int): The number of vertices in the cyclic graph.
        num_edges (int): The number of edges in the cyclic graph.

    Returns:
        A cyclic graph object.
    """

    assert num_edges >= num_vertices, "Number of edges must be greater than or equal to the number of vertices"

    graph = Graph(num_vertices)

    # Create a cycle
    for i in range(num_vertices - 1):
        graph.add_edge(i, i + 1)
    graph.add_edge(num_vertices - 1, 0)

    existing_edges = set(graph.edges())

    # Add extra edges
    extra_edges = num_edges - num_vertices
    while extra_edges > 0:
        v1 = random.randint(0, num_vertices - 1)
        v2 = random.randint(0, num_vertices - 1)

        if v1 != v2 and (v1, v2) not in existing_edges and (v2, v1) not in existing_edges:
            graph.add_edge(v1, v2)
            existing_edges.add((v1, v2))
            existing_edges.add((v2, v1))
            extra_edges -= 1

    return graph
