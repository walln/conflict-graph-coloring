from algo.structures.graph import Graph
from algo.ordering.largest_original_degree_last import largest_original_degree_last_vertex_ordering

def test_largest_original_degree_last_vertex_ordering_1():
    graph = Graph(5)
    graph.add_edge(0, 1)
    graph.add_edge(1, 2)
    graph.add_edge(2, 3)
    graph.add_edge(3, 4)
    graph.add_edge(4, 0)

    ordering, _ = largest_original_degree_last_vertex_ordering(graph)

    assert ordering == [0, 1, 2, 3, 4]

def test_largest_original_degree_last_vertex_ordering_2():
    graph = Graph(5)
    graph.add_edge(0, 1)
    graph.add_edge(0, 2)
    graph.add_edge(1, 3)
    graph.add_edge(1, 4)

    ordering, _ = largest_original_degree_last_vertex_ordering(graph)

    assert ordering == [2, 3, 4, 0, 1]

def test_largest_original_degree_last_vertex_ordering_3():
    graph = Graph(6)
    graph.add_edge(0, 1)
    graph.add_edge(0, 2)
    graph.add_edge(1, 3)
    graph.add_edge(2, 4)
    graph.add_edge(3, 5)
    graph.add_edge(4, 5)

    ordering, _ = largest_original_degree_last_vertex_ordering(graph)

    assert ordering == [0, 1, 2, 3, 4, 5]
