import random

from algo.structures.graph import Graph

def generate_uniform_random_graph(num_vertices, num_conflicts) -> Graph:
    """
    This function generates a random undirected graph with a uniform random
    distribution for selecting vertex pairs.

    Args:
        num_vertices (int): The number of vertices in the graph.
        num_edges (int): The number of distinct edges to add to the graph.

    Returns:
        A random undirected graph object.
    """

    assert num_conflicts <= (num_vertices*(num_vertices-1))/2, \
        "Number of edges cannot be greater than the maximum possible number of edges"

    graph = Graph(num_vertices)

    existing_edge_count = 0
    existing_edges = set(graph.edges())

    # Add edges
    while existing_edge_count < num_conflicts:
        v1 = random.randint(0, num_vertices - 1)
        v2 = random.randint(0, num_vertices - 1)

        if v1 != v2:
            if (v1, v2) not in existing_edges and (v2, v1) not in existing_edges:
                graph.add_edge(v1, v2)
                graph.add_edge(v2, v1)
                existing_edges.add((v1, v2))
                existing_edges.add((v2, v1))
                existing_edge_count += 1

    return graph
