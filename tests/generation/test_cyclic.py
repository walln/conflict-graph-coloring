from algo.structures.graph import Graph
from algo.generation.cyclic import generate_cyclic_graph

def has_cycle(graph: Graph) -> bool:
    visited = [False] * graph.V
    stack = [False] * graph.V

    def is_cyclic_util(vertex):
        visited[vertex] = True
        stack[vertex] = True

        for neighbor in graph.neighbors(vertex):
            if not visited[neighbor]:
                if is_cyclic_util(neighbor):
                    return True
            elif stack[neighbor]:
                return True

        stack[vertex] = False
        return False

    for vertex in range(graph.V):
        if not visited[vertex]:
            if is_cyclic_util(vertex):
                return True

    return False

def test_generate_cyclic_graph():
    # Test a small graph with 3 vertices
    graph = generate_cyclic_graph(3)
    assert len(graph.vertices()) == 3
    assert len(graph.edges()) == 3
    assert has_cycle(graph)

    # Test a larger graph with 7 vertices
    graph = generate_cyclic_graph(7)
    assert len(graph.vertices()) == 7
    assert len(graph.edges()) == 7
    assert has_cycle(graph)

    # Test a graph with many vertices
    graph = generate_cyclic_graph(100)
    assert len(graph.vertices()) == 100
    assert len(graph.edges()) == 100
    assert has_cycle(graph)

    # Test a graph with only one vertex
    graph = generate_cyclic_graph(1)
    assert len(graph.vertices()) == 1
    assert len(graph.edges()) == 0

    # Test a graph with two vertices
    graph = generate_cyclic_graph(2)
    assert len(graph.vertices()) == 2
    assert len(graph.edges()) == 1
    assert has_cycle(graph)
