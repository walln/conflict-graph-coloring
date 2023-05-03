from algo.structures.graph import Graph
from typing import Dict, List, Tuple, Union
from time import time


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
