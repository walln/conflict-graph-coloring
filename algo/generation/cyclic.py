from algo.structures.graph import Graph


def generate_cyclic_graph(num_vertices: int) -> Graph:
    """
    This function generates a cyclic graph (at least 1 cycle in the graph)
    with the specified number of vertices.

    A cyclic graph is a graph containing at least one graph cycle. In this function,
    the generated graph will have a specified number of vertices, with each
    vertex being part of at least one cycle.

    Args:
        num_vertices (int): The number of vertices in the cyclic graph.

    Returns:
        A cyclic graph object.
    """

    graph = Graph(num_vertices)

    # Create a cycle
    for i in range(num_vertices - 1):
        graph.add_edge(i, i + 1)
    graph.add_edge(num_vertices - 1, 0)

    return graph
