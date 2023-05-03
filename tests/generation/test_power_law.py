from algo.generation.power_law import generate_power_law_graph

def helper_test_generate_power_law_graph(num_vertices: int, num_edges_per_vertex: int):
    graph = generate_power_law_graph(num_vertices, num_edges_per_vertex)

    # Verify the number of vertices
    assert graph.V == num_vertices, f"Expected {num_vertices} vertices, but got {graph.V} vertices"

    # Verify the number of edges
    max_num_edges = num_vertices * (num_vertices - 1) // 2
    num_edges = len(graph.edges())
    assert 0 < num_edges <= max_num_edges, \
        f"Expected the number of edges to be between 1 and {max_num_edges}, but got {num_edges} edges"

def test_generate_power_law_graph_1():
    helper_test_generate_power_law_graph(5, 2)

def test_generate_power_law_graph_2():
    helper_test_generate_power_law_graph(6, 3)

def test_generate_power_law_graph_3():
    helper_test_generate_power_law_graph(7, 2)

def test_generate_large_power_law_graph():
    helper_test_generate_power_law_graph(200, 4)
