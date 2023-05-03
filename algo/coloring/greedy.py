from algo.structures.graph import Graph

def greedy_coloring(graph: Graph, ordering: list[int]) -> dict[int, int]:
    """
    Given a graph and an ordering of its vertices, performs a greedy graph coloring using the specified vertex ordering.

    The greedy coloring algorithm assigns the smallest legal color to each vertex in the specified order. A legal color
    for a vertex is a color that is not used by any of its adjacent vertices.

    Args:
        graph (Graph): The input graph to be colored.
        ordering (list[int]): A list of vertex indices specifying the order in which the vertices should be colored.

    Returns:
        dict[int, int]: A dictionary mapping vertex indices to their assigned colors.
    """
    # Initialize color assignment dictionary
    colors = {}

    # Iterate through the ordering
    for vertex in ordering:
        # Get adjacent vertices for the current vertex
        if graph.adj_list[vertex] is None:
            adjacent = []
        else:
            adjacent = [node.vertex for node in graph.adj_list[vertex]]

        # Get colors of the adjacent vertices
        adjacent_colors = [colors[v] for v in adjacent if v in colors]

        # Find the smallest color that is not already used by an adjacent vertex
        color = 0
        while color in adjacent_colors:
            color += 1

        # Assign the color to the current vertex
        colors[vertex] = color

    return colors
