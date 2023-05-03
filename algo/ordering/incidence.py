from algo.structures.graph import Graph
from typing import List, Tuple, Dict, Union
from time import time


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
