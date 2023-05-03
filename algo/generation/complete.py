from algo.structures.graph import Graph

def generate_complete_graph(num_vertices: int) -> Graph:
    """
    This function generates a complete graph with the specified number of vertices.

    A complete graph is a graph where every vertex has an edge connecting it to every
    other vertex within the vertex set.

    Args:
        num_vertices (int): The number of vertices in the complete graph.

    Returns:
        A complete graph object.
    """
    # Step 1: Create a new Graph object with the specified number of vertices
    graph = Graph(num_vertices)

    # Step 2: Iterate through all possible pairs of vertices and add an edge between them
    for i in range(num_vertices):
        for j in range(i + 1, num_vertices):
            graph.add_edge(i, j)

    return graph
