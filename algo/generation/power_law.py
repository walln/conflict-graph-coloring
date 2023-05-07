import random
from algo.structures.graph import Graph

def generate_power_law_graph(num_vertices, num_edges_total) -> Graph:
    """
    This function generates a power-law graph with the specified number of vertices and total number of edges.

    A power-law graph is a graph where the degree distribution follows a power-law, meaning that a small
    number of vertices have a high degree while the majority of vertices have a low degree.

    Args:
        num_vertices (int): The number of vertices in the power-law graph.
        num_edges_total (int): The total number of edges in the power-law graph.

    Returns:
        A power-law graph.
    """
    # Calculate the number of edges per vertex
    num_edges_per_vertex = int(num_edges_total / num_vertices)

    graph = Graph(num_vertices)

    # Start with a small complete graph (at least 2 vertices)
    for i in range(num_edges_per_vertex):
        for j in range(i + 1, num_edges_per_vertex):
            graph.add_edge(i, j)

    # For each new vertex, connect to existing vertices with probability proportional to their degree
    for vertex in range(num_edges_per_vertex, num_vertices):
        connected_vertices = set()
        while len(connected_vertices) < num_edges_per_vertex:
            candidate_vertex = random.choice(range(vertex))
            if candidate_vertex not in connected_vertices:
                connected_vertices.add(candidate_vertex)
                graph.add_edge(vertex, candidate_vertex)

    return graph
