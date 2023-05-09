import pytest
from algo.generation.complete import generate_complete_graph
from algo.structures.graph import Graph
from algo.serialization.graph import write_graph_to_file, read_graph_from_file

def test_write_and_read_graph(tmp_path):
    # Create a sample graph
    graph = Graph(4)
    graph.add_edge(0, 1)
    graph.add_edge(0, 2)
    graph.add_edge(1, 2)
    graph.add_edge(3, 0)

    # Write the graph to a temporary file
    temp_file = tmp_path / "test_graph.txt"
    write_graph_to_file(graph, str(temp_file))

    # Read the graph from the temporary file
    graph_from_file = read_graph_from_file(str(temp_file))

    # Compare the original graph and the graph read from the file
    assert graph.V == graph_from_file.V
    for vertex in graph.vertices():
        assert set(graph.neighbors(vertex)) == set(graph_from_file.neighbors(vertex))

def test_write_and_read_empty_graph_raises_error(tmp_path):
    # Create an empty graph
    empty_graph = Graph(0)

    # Write the empty graph to a temporary file
    temp_file = tmp_path / "empty_graph.txt"

    # Test that writing an empty graph raises a ValueError
    with pytest.raises(ValueError, match="Cannot write an empty graph to a file"):
        write_graph_to_file(empty_graph, str(temp_file))

def test_write_and_read_disconnected_graph(tmp_path):
    graph = Graph(5)
    graph.add_edge(0, 1)
    graph.add_edge(2, 3)

    temp_file = tmp_path / "disconnected_graph.txt"
    write_graph_to_file(graph, str(temp_file))

    graph_from_file = read_graph_from_file(str(temp_file))

    assert graph.V == graph_from_file.V
    for vertex in graph.vertices():
        assert set(graph.neighbors(vertex)) == set(graph_from_file.neighbors(vertex))


def test_write_and_read_complete_graph(tmp_path):
    graph = generate_complete_graph(4)

    temp_file = tmp_path / "complete_graph.txt"
    write_graph_to_file(graph, str(temp_file))

    graph_from_file = read_graph_from_file(str(temp_file))

    assert graph.V == graph_from_file.V
    for vertex in graph.vertices():
        assert set(graph.neighbors(vertex)) == set(graph_from_file.neighbors(vertex))


def test_write_and_read_line_graph(tmp_path):
    graph = Graph(5)
    graph.add_edge(0, 1)
    graph.add_edge(1, 2)
    graph.add_edge(2, 3)
    graph.add_edge(3, 4)

    temp_file = tmp_path / "line_graph.txt"
    write_graph_to_file(graph, str(temp_file))

    graph_from_file = read_graph_from_file(str(temp_file))

    assert graph.V == graph_from_file.V
    for vertex in graph.vertices():
        assert set(graph.neighbors(vertex)) == set(graph_from_file.neighbors(vertex))

def test_write_and_read_self_loop_graph(tmp_path):
    graph = Graph(3)
    graph.add_edge(0, 1)
    graph.add_edge(1,1)

    temp_file = tmp_path / "self_loop_graph.txt"
    write_graph_to_file(graph, str(temp_file))

    # Test that reading a graph with a self-loop raises a ValueError
    with pytest.raises(ValueError, match=r"Self-loops are not allowed: \(1, 1\)"):
        read_graph_from_file(str(temp_file))



def test_write_and_read_parallel_edges_graph(tmp_path):
    graph = Graph(3)
    graph.add_edge(0, 1)
    graph.add_edge(1, 2)
    graph.add_edge(1, 2)  # Parallel edge

    temp_file = tmp_path / "parallel_edges_graph.txt"
    write_graph_to_file(graph, str(temp_file))

    graph_from_file = read_graph_from_file(str(temp_file))

    assert graph.V == graph_from_file.V
    for vertex in graph.vertices():
        assert set(graph.neighbors(vertex)) == set(graph_from_file.neighbors(vertex))


def test_write_and_read_large_graph(tmp_path):
    graph = generate_complete_graph(1000)

    temp_file = tmp_path / "large_graph.txt"
    write_graph_to_file(graph, str(temp_file))

    graph_from_file = read_graph_from_file(str(temp_file))

    assert graph.V == graph_from_file.V
    for vertex in graph.vertices():
        assert set(graph.neighbors(vertex)) == set(graph_from_file.neighbors(vertex))
