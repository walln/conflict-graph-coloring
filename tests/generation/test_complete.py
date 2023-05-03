from algo.generation.complete import generate_complete_graph

def test_complete_1():
    graph = generate_complete_graph(3)
    edges = graph.edges()

    expected_edges = {(0, 1), (0, 2), (1, 2)}
    assert set(edges) == expected_edges, f"Expected {expected_edges}, but got {set(edges)}"

def test_complete_2():
    graph = generate_complete_graph(4)
    edges = graph.edges()

    expected_edges = {(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)}
    assert set(edges) == expected_edges, f"Expected {expected_edges}, but got {set(edges)}"

def test_large_complete():
    num_vertices = 1000

    graph = generate_complete_graph(num_vertices)
    edges = graph.edges()

    expected_num_edges = num_vertices * (num_vertices - 1) // 2
    assert len(edges) == expected_num_edges, f"Expected {expected_num_edges} edges, but got {len(edges)} edges"
