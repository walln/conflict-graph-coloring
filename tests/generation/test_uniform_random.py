from algo.generation.uniform_random import generate_uniform_random_graph


def test_generate_random_graph_uniform():
    graph = generate_uniform_random_graph(5, 4)
    assert len(graph.vertices()) == 5
    assert len(graph.edges()) == 4

    graph = generate_uniform_random_graph(10, 20)
    assert len(graph.vertices()) == 10
    assert len(graph.edges()) == 20

    graph = generate_uniform_random_graph(7, 10)
    assert len(graph.vertices()) == 7
    assert len(graph.edges()) == 10

    graph = generate_uniform_random_graph(15, 30)
    assert len(graph.vertices()) == 15
    assert len(graph.edges()) == 30
