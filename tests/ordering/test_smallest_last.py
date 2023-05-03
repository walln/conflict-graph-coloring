from algo.structures.graph import Graph
from algo.ordering.smallest_last import smallest_last_vertex_ordering

def test_smallest_last_vertex_ordering_1():
    g = Graph(6)
    g.add_edge(0, 1)
    g.add_edge(0, 2)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 4)
    g.add_edge(3, 5)

    ordering, _ = smallest_last_vertex_ordering(g)
    assert ordering == [4, 5, 3, 0, 1, 2]

def test_smallest_last_vertex_ordering_2():
    g = Graph(7)
    g.add_edge(0, 1)
    g.add_edge(0, 2)
    g.add_edge(1, 3)
    g.add_edge(2, 3)
    g.add_edge(3, 4)
    g.add_edge(3, 5)
    g.add_edge(3, 6)

    ordering, _ = smallest_last_vertex_ordering(g)
    assert ordering == [4, 5, 6, 0, 1, 2, 3]

def test_smallest_last_vertex_ordering_3():
    graph = Graph(12)
    graph.add_edge(0, 1)
    graph.add_edge(1, 2)
    graph.add_edge(2, 3)
    graph.add_edge(3, 0)

    graph.add_edge(4, 5)
    graph.add_edge(5, 6)
    graph.add_edge(6, 7)
    graph.add_edge(7, 4)

    graph.add_edge(8, 9)
    graph.add_edge(9, 10)
    graph.add_edge(10, 11)
    graph.add_edge(11, 8)

    ordering, _ = smallest_last_vertex_ordering(graph)

    assert ordering == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

def test_smallest_last_vertex_ordering_degrees_1():
    graph = Graph(5)
    graph.add_edge(0, 1)
    graph.add_edge(1, 2)
    graph.add_edge(2, 3)
    graph.add_edge(3, 4)

    ordering, meta = smallest_last_vertex_ordering(graph)
    deleted_degrees = meta['deleted_degrees']

    assert ordering == [0, 1, 2, 3, 4]
    assert deleted_degrees == {0: 1, 1: 1, 2: 1, 3: 1, 4:0}

def test_smallest_last_vertex_ordering_degrees_2():
    graph = Graph(6)
    graph.add_edge(0, 1)
    graph.add_edge(1, 2)
    graph.add_edge(2, 3)
    graph.add_edge(3, 4)
    graph.add_edge(4, 5)

    ordering, meta = smallest_last_vertex_ordering(graph)
    deleted_degrees = meta['deleted_degrees']

    assert ordering == [0, 1, 2, 3, 4, 5]
    assert deleted_degrees == {0: 1, 1: 1, 2: 1, 3: 1, 4: 1, 5: 0}
