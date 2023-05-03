from algo.structures.graph import Graph
from typing import Dict, List, Tuple, Union
from time import time

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
        for node in graph.adj_list[min_vertex]:
            neighbor = node.vertex
            if neighbor in remaining_vertices:
                degrees[neighbor] -= 1

    end_time = time()

    meta = {'deleted_degrees': deleted_degrees}
    meta['ordering_time'] = end_time - start_time
    return ordering, meta
