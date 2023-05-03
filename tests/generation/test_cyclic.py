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

def cylic_test_helper(num_vertices, num_edges):
        graph = generate_cyclic_graph(num_vertices, num_edges)

        # Verify the number of vertices
        assert graph.V == num_vertices, f"Expected {num_vertices} vertices, but got {graph.V} vertices"

        # Verify the number of edges
        assert len(graph.edges()) == num_edges, f"Expected {num_edges} edges, but got {len(graph.edges())} edges"

        # Verify that the graph contains at least one cycle
        assert has_cycle(graph), "The graph does not contain a cycle"


def test_cyclic_1():
    cylic_test_helper(5, 7)

def test_cyclic_2():
    cylic_test_helper(4, 5)

def test_cyclic_3():
    cylic_test_helper(6, 10)

def test_cyclic_4():
    cylic_test_helper(7, 12)

def test_cyclic_large():
    cylic_test_helper(300, 400)
