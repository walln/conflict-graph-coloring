from algo.structures.graph import Graph
from algo.ordering.incidence import incidence_ordering

def test_incidence_ordering_1():
    graph = Graph(7)
    graph.add_edge(0, 1)
    graph.add_edge(0, 2)
    graph.add_edge(1, 3)
    graph.add_edge(2, 4)
    graph.add_edge(2, 5)
    graph.add_edge(4, 6)

    ordering, _ = incidence_ordering(graph)


    assert ordering == [6, 3, 5, 1, 4, 2, 0]

def test_incidence_ordering_2():
    graph = Graph(6)
    graph.add_edge(0, 1)
    graph.add_edge(1, 2)
    graph.add_edge(1, 3)
    graph.add_edge(3, 4)
    graph.add_edge(3, 5)

    ordering, _ = incidence_ordering(graph)

    assert ordering == [5, 4, 2, 0, 3, 1]

def test_incidence_ordering_3():
    graph = Graph(7)
    graph.add_edge(0, 1)
    graph.add_edge(0, 2)
    graph.add_edge(1, 3)
    graph.add_edge(1, 4)
    graph.add_edge(2, 5)
    graph.add_edge(2, 6)

    ordering, _ = incidence_ordering(graph)

    assert ordering == [6, 5, 4, 3, 2, 1, 0]
