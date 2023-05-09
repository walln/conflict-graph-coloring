from algo.structures.graph import Graph
from typing import List, Tuple, Dict, Union
from time import time


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
