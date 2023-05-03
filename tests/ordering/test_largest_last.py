from algo.structures.graph import Graph
from algo.ordering.largest_last import largest_last_vertex_ordering

def test_largest_last_vertex_ordering_1():
    graph = Graph(5)
    graph.add_edge(0, 1)
    graph.add_edge(1, 2)
    graph.add_edge(2, 3)
    graph.add_edge(3, 4)
    graph.add_edge(4, 0)

    ordering, _ = largest_last_vertex_ordering(graph)

    assert ordering == [4, 3, 2, 1, 0]

def test_largest_last_vertex_ordering_2():
    graph = Graph(4)
    graph.add_edge(0, 1)
    graph.add_edge(1, 2)
    graph.add_edge(2, 3)
    graph.add_edge(3, 0)

    ordering, _ = largest_last_vertex_ordering(graph)

    assert ordering == [3, 2, 1, 0]

def test_largest_last_vertex_ordering_3():
    graph = Graph(6)
    graph.add_edge(0, 1)
    graph.add_edge(0, 2)
    graph.add_edge(1, 3)
    graph.add_edge(2, 4)
    graph.add_edge(3, 5)
    graph.add_edge(4, 5)

    ordering, _ = largest_last_vertex_ordering(graph)

    assert ordering == [5, 4, 3, 2, 1, 0]
