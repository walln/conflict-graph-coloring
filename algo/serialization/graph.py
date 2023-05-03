from algo.structures.graph import Graph

def write_graph_to_file(graph: Graph, filename: str) -> None:
    """
    Writes the adjacency list of the given graph to a file in a simple adjacency list format.

    Args:
        graph (Graph): The graph to be written to a file.
        filename (str): The path to the file to which the graph will be written.

    Raises:
        ValueError: If the input graph is empty.
    """

    if graph.V == 0:
        raise ValueError("Cannot write an empty graph to a file")

    with open(filename, "w") as file:
        for u in graph.vertices():
            neighbors = graph.neighbors(u)
            neighbors_str = " ".join(str(v) for v in neighbors)
            file.write(f"{neighbors_str}\n")

def read_graph_from_file(filename: str) -> Graph:
    """
    Reads a graph from a file in a simple adjacency list format and returns a Graph object.

    Args:
        filename (str): The path to the file containing the graph.

    Returns:
        A Graph object representing the graph read from the file.

    Raises:
        FileNotFoundError: If the file is not found.
        ValueError: If the input file is empty or contains invalid data.
    """
    try:
        with open(filename, "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {filename}")

    if not lines:
        raise ValueError("Input file is empty")

    num_vertices = len(lines)
    graph = Graph(num_vertices)
    added_edges = set()

    for u, line in enumerate(lines):
        if line.strip():
            for v in map(int, line.strip().split()):
                if v < 0 or v >= num_vertices:
                    raise ValueError(f"Invalid vertex number: {v}")
                if u != v and (u, v) not in added_edges and (v, u) not in added_edges:
                    graph.add_edge(u, v)
                    added_edges.add((u, v))
                elif u == v:
                    raise ValueError(f"Self-loops are not allowed: ({u}, {v})")

    return graph
