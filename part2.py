from argparse import ArgumentParser
import os
import datetime
import time
from typing import Dict, List, Tuple, Union

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


def bron_kerbosch(graph: Graph, r=None, p=None, x=None, pivot=True):
    if r is None:
        r = set()
    if p is None:
        p = set(range(graph.V))
    if x is None:
        x = set()

    if not p and not x:
        return [r]

    cliques = []
    if pivot:

        u = max(p | x, key=lambda v: len(graph.neighbors(v)))
        neighbors = set(graph.neighbors(u))
        loop_over = p - neighbors
    else:
        loop_over = p.copy()

    for v in loop_over:
        neighbors = set(graph.neighbors(v))
        new_r = r | {v}
        new_p = p & neighbors
        new_x = x & neighbors
        cliques += bron_kerbosch(graph, new_r, new_p, new_x, pivot=pivot)
        p.remove(v)
        x.add(v)

    return cliques

def terminal_clique_size(graph: Graph):
    all_cliques = bron_kerbosch(graph)
    terminal_clique = max(all_cliques, key=len)
    return len(terminal_clique)


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

def incidence_ordering(graph: Graph) -> Tuple[List[int], Dict[str, Union[int, Dict[int, int]]]]:
    """
    This function computes the incidence degree ordering of the given graph.

    The incidence degree ordering is a vertex ordering based on the sum of the degrees of
    the two vertices incident to each edge in the graph. In this ordering, vertices are
    sorted in ascending order according to the sum of the degrees of their incident vertices.

    Args:
        graph (Graph): The input graph for which the incidence degree ordering will be computed.

    Returns:
        Tuple[List[int], Dict[str, Union[str, int, float]]]: A tuple containing a list of vertex indices representing
        the ordering of the vertices, and a dictionary of metadata.
    """
    start_time = time()

    ordering = []
    remaining_vertices = set(graph.vertices())

    while remaining_vertices:
        min_incidence_degree = float('inf')
        selected_vertex = None

        for vertex in remaining_vertices:
            vertex_degree = sum(graph.degree(neighbor) for neighbor in graph.neighbors(vertex))

            if (vertex_degree < min_incidence_degree) or \
                (vertex_degree == min_incidence_degree and vertex > selected_vertex):
                min_incidence_degree = vertex_degree
                selected_vertex = vertex

        remaining_vertices.remove(selected_vertex)
        ordering.append(selected_vertex)

    end_time = time()

    meta = {}
    meta['ordering_time'] = end_time - start_time


    return ordering, meta

def connected_sequential_ordering(graph: Graph) -> Tuple[List[int], Dict[str, Union[int, Dict[int, int]]]]:
    """
    Orders the vertices of a graph in a connected sequential ordering.

    Connected Sequential Ordering (CSO) is a vertex ordering method that starts with an arbitrary vertex,
    then iteratively selects the next vertex with the highest degree among all unvisited vertices that are connected to
    the already visited vertices. If there are no such connected vertices, the algorithm picks an unvisited vertex with
    the highest degree among all unvisited vertices and continues the process.

    Args:
    graph (Graph): An instance of the Graph class representing the input graph.

 Returns:
        Tuple[List[int], Dict[str, Union[str, int, float]]]: A tuple containing a list of vertex indices representing
        the connected sequential ordering of the vertices, and a dictionary of metadata.
    """
    start_time = time()

    visited = set()
    ordering = []

    while len(visited) < graph.V:
        # Find the highest degree unvisited vertex that is connected to the visited vertices
        highest_degree_vertex = None
        highest_degree = -1

        for v in range(graph.V):
            if v not in visited:
                if highest_degree_vertex is None:
                    highest_degree_vertex = v
                    highest_degree = graph.degree(v)

                connected_to_visited = any(u in visited for u in graph.neighbors(v))
                if connected_to_visited and graph.degree(v) > highest_degree:
                    highest_degree_vertex = v
                    highest_degree = graph.degree(v)
                elif not connected_to_visited and not any(u in visited for u in graph.neighbors(highest_degree_vertex)):
                    if graph.degree(v) > highest_degree:
                        highest_degree_vertex = v
                        highest_degree = graph.degree(v)

        visited.add(highest_degree_vertex)
        ordering.append(highest_degree_vertex)

    end_time = time()

    meta = {}
    meta['ordering_time'] = end_time - start_time


    return ordering, meta


def largest_last_vertex_ordering(graph: Graph) -> Tuple[List[int], Dict[str, Union[int, Dict[int, int]]]]:
    """
    This function computes the largest vertex last ordering of the given graph. In this ordering, vertices are sorted
    in ascending order based on their degree, but starting with the vertex of the largest degree. The purpose of this
    ordering is to prioritize the vertices with the highest degree at the end of the ordering.

    Args:
        graph (Graph): The input graph for which the largest vertex last ordering will be computed.

    Returns:
        Tuple[List[int], Dict[str, Union[str, int, float]]]: A tuple containing a list of vertex indices representing
        the ordering of the vertices, and a dictionary of metadata.
    """

    start_time = time()

    ordering = []

    # degrees = [len([_ for _ in node]) for node in graph.adj_list]
    degrees = [graph.degree(v) for v in range(graph.V)]

    while len(ordering) < graph.V:
        max_degree = -1
        max_vertex = -1

        # Find the vertex with the largest degree that is not in ordering
        for idx, degree in enumerate(degrees):
            if idx not in ordering and (degree > max_degree or (degree == max_degree and idx > max_vertex)):
                max_degree = degree
                max_vertex = idx

        ordering.append(max_vertex)

    end_time = time()

    meta = {}
    meta['ordering_time'] = end_time - start_time


    return ordering, meta

def largest_original_degree_last_vertex_ordering(graph: Graph) -> \
    Tuple[List[int], Dict[str, Union[int, Dict[int, int]]]]:
    """
    This function computes the largest original degree last ordering of the given graph.

    In this ordering, vertices are sorted in ascending order based on their
    original degree (degree before any modifications to the graph), but
    starting with the vertex with the largest original degree.
    The purpose of this ordering is to prioritize the vertices with the
    highest original degree at the end of the ordering.

    Args:
        graph (Graph): The input graph for which the largest original degree last ordering will be computed.

    Returns:
        Tuple[List[int], Dict[str, Union[str, int, float]]]: A tuple containing a list of vertex indices representing
        the ordering of the vertices, and a dictionary of metadata.
    """

    start_time = time()

    # Initialize an empty list for the final ordering
    ordering = []

    # Create a list of vertex degrees
    degrees = [graph.degree(v) for v in range(graph.V)]

    while len(ordering) < graph.V:
        # Find the maximum degree among unprocessed vertices
        max_degree = max(deg for idx, deg in enumerate(degrees) if idx not in ordering)

        # Get the indices of the vertices with the maximum degree
        max_degree_vertices = [idx for idx, deg in enumerate(degrees) if deg == max_degree and idx not in ordering]

        # Find the vertex with the largest label among the max_degree_vertices
        max_vertex = max(max_degree_vertices)

        # Add the selected vertex to the beginning of the ordering
        ordering.insert(0, max_vertex)

    end_time = time()

    meta = {}
    meta['ordering_time'] = end_time - start_time


    return ordering, meta

def smallest_last_vertex_ordering(graph: Graph) -> Tuple[List[int], Dict[str, Union[int, Dict[int, int]]]]:
    """
    This function computes the smallest last vertex ordering of the given graph.

    In this ordering, vertices are sorted based on their degrees in ascending order.
    At each step, the vertex with the smallest current degree is removed from the graph along with its edges,
    and the process is repeated until all vertices have been ordered.
    The purpose of this ordering is to prioritize vertices with lower degrees at the end of the ordering.

    Args:
        graph (Graph): The input graph for which the smallest last vertex ordering will be computed.


    Returns:
        Tuple[List[int], Dict[str, Union[str, int, float]]]: A tuple containing a list of vertex indices representing
        the ordering of the vertices, and a dictionary of metadata.
    """

    start_time = time()

    remaining_vertices = set(graph.vertices())
    degrees = [graph.degree(vertex) for vertex in graph.vertices()]
    ordering = []
    deleted_degrees = {}

    while remaining_vertices:
        # Find the vertex with the smallest degree
        min_degree = float('inf')
        min_vertex = None
        for v in remaining_vertices:
            if degrees[v] < min_degree:
                min_degree = degrees[v]
                min_vertex = v

        # Remove the vertex from the graph and add it to the ordering
        remaining_vertices.remove(min_vertex)
        ordering.append(min_vertex)
        deleted_degrees[min_vertex] = min_degree
        if graph.adj_list[min_vertex] is not None:
            for node in graph.adj_list[min_vertex]:
                neighbor = node.vertex
                if neighbor in remaining_vertices:
                    degrees[neighbor] -= 1

    end_time = time()

    meta = {'deleted_degrees': deleted_degrees}
    meta['ordering_time'] = end_time - start_time
    return ordering, meta

def smallest_original_degree_last_vertex_ordering(graph: Graph) -> \
    Tuple[List[int], Dict[str, Union[int, Dict[int, int]]]]:
    """
    This function computes the smallest original degree last ordering of the given graph.

    In this ordering, vertices are sorted in ascending order based on their
    original degree (degree before any modifications to the graph), but starting
    with the vertex with the smallest original degree.
    The purpose of this ordering is to prioritize the vertices with the
    lowest original degree at the end of the ordering.

    Args:
        graph (Graph): The input graph for which the smallest original degree last ordering will be computed.

    Returns:
        Tuple[List[int], Dict[str, Union[str, int, float]]]: A tuple containing a list of vertex indices representing
        the ordering of the vertices, and a dictionary of metadata.
    """

    start_time = time()

    # Initialize an empty list for the final ordering
    ordering = []

    # Create a list of vertex degrees using the degree function from the Graph class
    degrees = [graph.degree(i) for i in range(graph.V)]

    # Initialize a set of unprocessed vertices
    remaining_vertices = set(range(graph.V))

    # While there are unprocessed vertices
    while remaining_vertices:
        # Find the maximum degree among unprocessed vertices
        max_degree = max(degrees[i] for i in remaining_vertices)

        # Get the indices of the vertices with the maximum degree
        max_degree_vertices = [i for i in remaining_vertices if degrees[i] == max_degree]

        # Find the vertex with the smallest label among the max_degree_vertices
        min_vertex = min(max_degree_vertices)

        # Add the selected vertex to the end of the ordering
        ordering.append(min_vertex)

        # Remove the selected vertex from the remaining_vertices set
        remaining_vertices.remove(min_vertex)

    end_time = time()

    meta = {}
    meta['ordering_time'] = end_time - start_time

    return ordering, meta




def part2():
    """
    Part 2 of the CLI, reads a graph from a file, and using a selected ordering
    method will color the graph and output the the coloring to a file.
    """
    parser = ArgumentParser()
    parser.add_argument("-i",
                        "--input_file",
                        help="Input File name",
                        type=str,
                        required=True)
    parser.add_argument("-f",
                        "--output_file",
                        help="Output File name",
                        type=str,
                        default="coloring.txt",
                        required=False)
    parser.add_argument("-o",
                        "--ordering",
                        help="Ordering method to use for graph coloring.",
                        type=str,
                        choices=['smallest_last',
                                 'smallest_original_degree_last',
                                 'largest_last',
                                 'largest_original_degree_last',
                                 'incidence',
                                 'connected_sequential'],
                        required=True)

    args = parser.parse_args()

    orderings = {
        'smallest_last': smallest_last_vertex_ordering,
        'smallest_original_degree_last': smallest_original_degree_last_vertex_ordering,
        'largest_last': largest_last_vertex_ordering,
        'largest_original_degree_last': largest_original_degree_last_vertex_ordering,
        'incidence': incidence_ordering,
        'connected_sequential': connected_sequential_ordering
    }

    ordering = orderings[args.ordering]

    input_fname = args.input_file
    if not is_valid_filename(input_fname):
        raise ValueError("Invalid input filename.")

    output_fname = args.output_file
    if not is_valid_filename(output_fname):
        raise ValueError("Invalid output filename.")

    print('-' * SEPERATOR_LENGTH)
    print("Using the following arguments:")
    print(f'{"Input file:":<30} {input_fname} 📄')
    print(f'{"Output file:":<30} {output_fname} 📄')
    print(f'{"Ordering method:":<30} {args.ordering} 📈')
    print('-' * SEPERATOR_LENGTH)

    print(f'{"Reading graph from file..."} 📊')
    graph = read_graph_from_file(input_fname)
    print('Graph read from file🎉')
    print(f'{"Vertex count:":<30} {len(graph.vertices())} 📏')
    print(f'{"Edge count:":<30} {len(graph.edges())} 📏')
    print(f'{"Terminal clique size:":<30}{terminal_clique_size(graph)} 📏')
    average_original_degree = sum([graph.degree(v) for v in graph.vertices()]) / len(graph.vertices())
    print(f'{"Average original degree:":<30}{average_original_degree} 📏')
    print('-' * SEPERATOR_LENGTH)

    print(f'{"Ordering graph using:":<30} {args.ordering}... 🔢')
    order, meta = ordering(graph)

    if 'ordering_time' in meta:
        order_time = meta['ordering_time']
        ordering_time_str = str(datetime.timedelta(seconds=order_time))
        print(f'{"Ordering time:":<30} {ordering_time_str} ⏱️')
    else:
        print(f'{"Ordering time:":<30} {"N/A"} ⏱️')

    if 'deleted_degrees' in meta:
        deleted_degrees = meta['deleted_degrees']
        print(f'{"Vertex degree when deleted:":<30}')
        for vertex, degree in deleted_degrees.items():
            print(f'{vertex}: {degree} 📏')

    print('-' * SEPERATOR_LENGTH)

    print(f'{"Coloring graph..."} 🎨')
    coloring_start_time = time.time()
    coloring = greedy_coloring(graph, order)
    coloring_time = time.time() - coloring_start_time

    print(f'{"Coloring time:":<30} {str(datetime.timedelta(seconds=coloring_time))} ⏱️')
    colors_used = len(set(coloring.values()))
    print(f'{"Colors used:":<30} {colors_used} 📏')
    print('-' * SEPERATOR_LENGTH)

    # Now we need to write the coloring to a file
    # The format for this is such that each line follows the format:
    # VERTEX_NUMBER, COLOR_NUMBER

    print(f'{"Writing coloring to file..."} 📄')
    with open(output_fname, 'w') as f:
        for vertex, color in coloring.items():
            f.write(f'{vertex},{color}\n')
    print(f'{"Coloring written to file."} 🚀')
