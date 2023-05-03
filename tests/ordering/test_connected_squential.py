from algo.structures.graph import Graph
from algo.ordering.connected_sequential_ordering import connected_sequential_ordering

def test_connected_sequential_ordering_1():
    """
    A graph with a cycle and a few branches
         5
         |
    0 -- 1 -- 2
    |    |    |
    4 -- 3    6
    """
    graph = Graph(7)
    graph.add_edge(0, 1)
    graph.add_edge(1, 2)
    graph.add_edge(1, 3)
    graph.add_edge(1, 5)
    graph.add_edge(2, 6)
    graph.add_edge(3, 4)
    graph.add_edge(4, 0)
    ordering, _ = connected_sequential_ordering(graph)
    assert ordering[:5] == [1, 0, 2, 3, 4] or ordering[:5] == [1, 2, 0, 3, 4], f"Unexpected ordering: {ordering}"

def test_connected_sequential_ordering_2():
    """
    A tree-like graph
         3
         |
    0 -- 1 -- 2
         |
         4
    """
    graph = Graph(5)
    graph.add_edge(0, 1)
    graph.add_edge(1, 2)
    graph.add_edge(1, 3)
    graph.add_edge(1, 4)
    ordering, _ = connected_sequential_ordering(graph)
    assert ordering == [1, 0, 2, 3, 4], f"Unexpected ordering: {ordering}"


def test_connected_sequential_ordering_3():
    """
    A graph with multiple connected components
    Component 1: 0 - 1 - 2
    Component 2: 3 - 4 - 5
    """
    graph = Graph(6)
    graph.add_edge(0, 1)
    graph.add_edge(1, 2)
    graph.add_edge(3, 4)
    graph.add_edge(4, 5)
    ordering, _ = connected_sequential_ordering(graph)

    # Check if the starting vertices for each component are correct
    assert ordering[0] == 1 and ordering[3] == 4, f"Unexpected ordering: {ordering}"

def test_connected_sequential_ordering_4():
    """
    A graph with two separate cycles
    Component 1: 0 - 1 - 2 - 0
    Component 2: 3 - 4 - 5 - 3
    """
    graph = Graph(6)
    graph.add_edge(0, 1)
    graph.add_edge(1, 2)
    graph.add_edge(2, 0)
    graph.add_edge(3, 4)
    graph.add_edge(4, 5)
    graph.add_edge(5, 3)
    ordering, _ = connected_sequential_ordering(graph)

    # Check if the starting vertices for each component are correct
    assert ordering[0] in [0, 1, 2] and ordering[3] in [3, 4, 5], f"Unexpected ordering: {ordering}"

def test_connected_sequential_ordering_5():
    """
    A graph with a star-like structure
         5
         |
    0 -- 1 -- 2
         |
         4
    """
    graph = Graph(6)
    graph.add_edge(0, 1)
    graph.add_edge(1, 2)
    graph.add_edge(1, 4)
    graph.add_edge(1, 5)
    ordering, _ = connected_sequential_ordering(graph)

    # Check if the starting vertex is correct
    assert ordering[0] == 1, f"Unexpected ordering: {ordering}"

def test_connected_sequential_ordering_6():
    """
    A graph with a mix of components
    Component 1: 0 - 1 - 2 - 3
    Component 2: 4 - 5 - 6 - 4
    Component 3: 7 (isolated vertex)
    """
    graph = Graph(8)
    graph.add_edge(0, 1)
    graph.add_edge(1, 2)
    graph.add_edge(2, 3)
    graph.add_edge(4, 5)
    graph.add_edge(5, 6)
    graph.add_edge(6, 4)
    ordering, _ = connected_sequential_ordering(graph)

    # Check if the starting vertices for each component are correct
    assert ordering[0] == 1 and ordering[4] in [4, 5, 6] and ordering[7] == 7, f"Unexpected ordering: {ordering}"
