from algo.structures.graph import Graph
from typing import List, Tuple, Dict, Union
from time import time



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
