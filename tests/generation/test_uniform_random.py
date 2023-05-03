from algo.generation.uniform_random import generate_uniform_random_graph

def helper_function(num_vertices, num_edges):
    graph = generate_uniform_random_graph(num_vertices, num_edges)

    # Verify the number of vertices
    assert graph.V == num_vertices, f"Expected {num_vertices} vertices, but got {graph.V} vertices"

    # Verify the number of edges
    assert len(graph.edges()) == num_edges, f"Expected {num_edges} edges, but got {len(graph.edges())} edges"

def test_uniform_random_generation_1():
    helper_function(5,5)

def test_uniform_random_generation_2():
    helper_function(6,8)

def test_uniform_random_generation_3():
    helper_function(7,14)

def test_uniform_random_generation_large():
    helper_function(200, 3000)
