from algo.structures.graph import Graph
from algo.ordering.smallest_original_degree_last import smallest_original_degree_last_vertex_ordering

def test_smallest_original_degree_last_vertex_ordering_1():
    graph = Graph(6)
    graph.add_edge(0, 1)
    graph.add_edge(0, 2)
    graph.add_edge(1, 3)
    graph.add_edge(1, 4)
    graph.add_edge(2, 3)
    graph.add_edge(4, 5)

    ordering, _ = smallest_original_degree_last_vertex_ordering(graph)

    assert ordering == [1, 0, 2, 3, 4, 5], "Test case failed"

def test_smallest_original_degree_last_vertex_ordering_2():
    graph = Graph(8)
    graph.add_edge(0, 1)
    graph.add_edge(1, 2)
    graph.add_edge(2, 3)
    graph.add_edge(3, 4)
    graph.add_edge(4, 5)
    graph.add_edge(5, 6)
    graph.add_edge(6, 7)

    ordering, _ = smallest_original_degree_last_vertex_ordering(graph)

    assert ordering == [1, 2, 3, 4, 5, 6, 0, 7]

def test_smallest_original_degree_last_vertex_ordering_3():
    graph = Graph(7)
    graph.add_edge(0, 1)
    graph.add_edge(0, 2)
    graph.add_edge(1, 3)
    graph.add_edge(1, 4)
    graph.add_edge(2, 5)
    graph.add_edge(2, 6)

    ordering, _ = smallest_original_degree_last_vertex_ordering(graph)

    assert ordering == [1, 2, 0, 3, 4, 5, 6]

def test_sold_ordering_4():
    graph = Graph(5)
    graph.add_edge(0, 1)
    graph.add_edge(0, 2)
    graph.add_edge(1, 3)
    graph.add_edge(1, 4)

    ordering, _ = smallest_original_degree_last_vertex_ordering(graph)

    assert ordering == [1, 0, 2, 3, 4]
