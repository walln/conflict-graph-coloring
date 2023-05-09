import os
import random
from argparse import ArgumentParser
from typing import List

SEPERATOR_LENGTH = 43

class Node:
    def __init__(self, value):
        self.vertex = value
        self.next = None

    def __iter__(self):
        curr = self
        while curr:
            yield curr
            curr = curr.next

class Graph:
    def __init__(self, num_verticies: int) -> None:
        self.V = num_verticies
        self.adj_list: List[Node] = [None] * self.V

    def vertices(self) -> list[int]:
        return list(range(self.V))

    def edges(self) -> list[tuple[int, int]]:
        """
        Returns a list of all edges in the graph as tuples (u, v), where u and v are connected vertices.
        """
        edges = set()
        for u in range(self.V):
            node = self.adj_list[u]
            while node:
                v = node.vertex
                if u < v:
                    edges.add((u, v))
                node = node.next
        return list(edges)

    def add_edge(self, s, d):
        # Create new node
        node = Node(d)
        node.next = self.adj_list[s]
        self.adj_list[s] = node

        node = Node(s)
        node.next = self.adj_list[d]
        self.adj_list[d] = node

    def edge_exists(self, u, v):
        temp = self.adj_list[u]
        while temp:
            if temp.vertex == v:
                return True
            temp = temp.next
        return False

    def print_graph(self):
        for i in range(self.V):
            print("Vertex " + str(i) + ":", end="")
            temp = self.adj_list[i]
            while temp:
                print(" -> {}".format(temp.vertex), end="")
                temp = temp.next
            print(" \n")

    def degree(self, vertex):
        """
        Returns the degree of the given vertex
        """
        degree = 0
        temp = self.adj_list[vertex]
        while temp:
            degree += 1
            temp = temp.next
        return degree


    def neighbors(self, vertex):
        """
        Returns a list of neighbors of the given vertex
        """
        neighbors = []
        temp = self.adj_list[vertex]
        while temp:
            neighbors.append(temp.vertex)
            temp = temp.next
        return neighbors

    def dfs(self, start, visited):
        """
        Depth-First Search algorithm starting from the given vertex.
        """
        visited[start] = True
        yield start

        for neighbor in self.neighbors(start):
            if not visited[neighbor]:
                yield from self.dfs(neighbor, visited)

    def connected_components(self):
        """
        Returns a list of connected components, where each component is a list of vertices.
        """
        visited = [False] * self.V
        components = []

        for vertex in range(self.V):
            if not visited[vertex]:
                component = list(self.dfs(vertex, visited))
                components.append(component)

        return components

def is_valid_filename(filename):
    """
    Check whether the given filename is valid and writable.

    Args:
        filename (str): The filename to validate.

    Returns:
        bool: True if the filename is valid and writable, False otherwise.
    """
    if not isinstance(filename, str) or not filename:
        return False

    if not all(c.isprintable() and c not in ['/', '\\', ':', '*', '?', '<', '>', '|'] for c in filename):
        return False

    if os.path.isdir(filename):
        return False

    if os.path.isfile(filename) and not os.access(filename, os.W_OK):
        return False

    if not os.access(os.path.dirname(os.path.abspath(filename)), os.W_OK):
        return False

    return True

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

def complete_edge_count(V: int):
    return int(V * (V - 1) / 2)

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

def generate_power_law_random_graph(num_vertices, num_conflicts, power=2.5) -> Graph:
    """
    This function generates a random undirected graph with a power-law random
    distribution for selecting vertex pairs.

    Args:
        num_vertices (int): The number of vertices in the graph.
        num_conflicts (int): The number of distinct edges to add to the graph.
        power (float): The power parameter for the power-law distribution.

    Returns:
        A random undirected graph object.
    """

    assert num_conflicts <= (num_vertices*(num_vertices-1))/2, \
        "Number of edges cannot be greater than the maximum possible number of edges"

    graph = Graph(num_vertices)

    existing_edge_count = 0
    existing_edges = set(graph.edges())

    # Calculate degree distribution
    degree_sum = sum([i**power for i in range(1, num_vertices+1)])
    probs = [i**power / degree_sum for i in range(1, num_vertices+1)]

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


def part1():
    """
    Part 1 of the CLI, generates a graph and outputs it to a file.
    Using the selected output file, number of edges, number of vertices,
    and graph generation method, a graph is generated and output to the
    selected file.
    """
    parser = ArgumentParser()
    parser.add_argument("-o",
                        "--output_file",
                        help="Output File name",
                        type=str,
                        required=True)
    parser.add_argument("-v",
                        "--vertices",
                        help="How many vertices to add to the graph.",
                        type=int,
                        required=True)
    parser.add_argument("-e",
                        "--edges",
                        help="How many edges to add to the graph.",
                        type=int,
                        required=True)
    parser.add_argument("-g",
                        "--generator",
                        help="Graph generation method.",
                        type=str,
                        choices=['complete', 'power_law', 'uniform_random', 'skewed_random', 'cyclic'],
                        required=True)

    args = parser.parse_args()

    methods = {
        "complete": generate_complete_graph,
        "power_law": generate_power_law_random_graph,
        "uniform_random": generate_uniform_random_graph,
        "skewed_random" : generate_skewed_random_graph,
        "cyclic": generate_cyclic_graph
    }

    V: int = args.vertices
    E: int = args.edges

    if args.generator not in methods:
        raise ValueError("Invalid graph generation method.")

    output_fname = args.output_file
    if not is_valid_filename(output_fname):
        raise ValueError("Invalid output filename.")

    method = methods[args.generator]

    if V > 10_000:
        raise ValueError("Input vertex amount exceeds maximum of 10,000.")
    if E > 2_000_000:
        raise ValueError("Input edge amount exceeds maximum of 2,000,000.")
    if args.generator == "complete" and E != complete_edge_count(V):
        raise ValueError(f'For a complete graph with {V} edges {complete_edge_count(V)} edges must exist.')

    print('-' * SEPERATOR_LENGTH)
    print("Using the following arguments:")
    print(f'{"Output file:":<30} {output_fname} 📄')
    print(f'{"Vertices:":<30} {V} 📏')
    print(f'{"Edges:":<30} {E} 📏')
    print(f'{"Graph generation method:":<30} {args.generator} 📈')
    print('-' * SEPERATOR_LENGTH)

    print(f'{"Generating graph..."} 📊')

    graph: Graph = method(V, E) if args.generator != "complete" else method(V)
    print('Graph generated 🎉')

    write_graph_to_file(graph, output_fname)
    print(f'Graph written to {output_fname} 🚀')
