from typing import List, Tuple, Dict, Union
from algo.structures.graph import Graph
from time import time


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
