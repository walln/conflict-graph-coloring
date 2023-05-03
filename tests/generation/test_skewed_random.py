from algo.generation.skewed_random import generate_skewed_graph

def helper_test_generate_skewed_graph(num_vertices: int, num_edges: int):
    graph = generate_skewed_graph(num_vertices, num_edges)

    # Verify the number of vertices
    assert graph.V == num_vertices, f"Expected {num_vertices} vertices, but got {graph.V} vertices"

    # Verify the number of edges
    assert len(graph.edges()) == num_edges, f"Expected {num_edges} edges, but got {len(graph.edges())} edges"

def test_skewed_generation_1():
    helper_test_generate_skewed_graph(5, 5)

def test_skewed_generation_2():
    helper_test_generate_skewed_graph(6, 8)

def test_skewed_generation_3():
    helper_test_generate_skewed_graph(7, 14)

def test_skewed_generation_large():
    helper_test_generate_skewed_graph(200, 1000)
