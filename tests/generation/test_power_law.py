from algo.generation.power_law import generate_power_law_random_graph


def test_generate_power_law_random_graph():
    # Test graph with 5 vertices and 3 edges
    graph = generate_power_law_random_graph(5, 3)
    assert len(graph.vertices()) == 5
    assert len(graph.edges()) == 3

    # Test graph with 10 vertices and 15 edges
    graph = generate_power_law_random_graph(10, 15)
    assert len(graph.vertices()) == 10
    assert len(graph.edges()) == 15


    # Test graph with 20 vertices and 100 edges
    graph = generate_power_law_random_graph(20, 100)
    assert len(graph.vertices()) == 20
    assert len(graph.edges()) == 100
