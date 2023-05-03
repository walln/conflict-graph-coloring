from algo.structures.graph import Graph

def test_init_graph():
    g = Graph(5)
    assert g.V == 5
    assert g.adj_list == [None, None, None, None, None]

def test_vertices():
    g = Graph(5)
    g.add_edge(0, 1)
    g.add_edge(0, 2)
    g.add_edge(1, 3)
    g.add_edge(1, 4)

    assert g.vertices() == [0,1,2,3,4]

    graph = Graph(4)
    graph.add_edge(0, 1)
    graph.add_edge(1, 2)
    graph.add_edge(2, 3)
    graph.add_edge(3, 0)

    assert graph.vertices() == [0,1,2,3]

def test_edges():
    graph = Graph(4)
    graph.add_edge(0, 1)
    graph.add_edge(0, 2)
    graph.add_edge(1, 3)

    # Get the list of edges in the graph
    edges = graph.edges()

    # Verify the output using assertions
    expected_edges = {(0, 1), (0, 2), (1, 3)}
    assert set(edges) == expected_edges, f"Expected {expected_edges}, but got {set(edges)}"

    # Manually construct a graph with 5 vertices and 5 edges
    graph = Graph(5)
    graph.add_edge(0, 1)
    graph.add_edge(1, 2)
    graph.add_edge(2, 3)
    graph.add_edge(3, 4)
    graph.add_edge(4, 0)

    # Get the list of edges in the graph
    edges = graph.edges()

    # Verify the output using assertions
    expected_edges = {(0, 1), (0, 4), (1, 2), (2, 3), (3, 4)}
    assert set(edges) == expected_edges, f"Expected {expected_edges}, but got {set(edges)}"


def test_add_edge():
    g = Graph(4)
    g.add_edge(0, 1)
    assert g.adj_list[0].vertex == 1
    assert g.adj_list[1].vertex == 0

def test_add_multiple_edges():
    g = Graph(5)
    g.add_edge(0, 1)
    g.add_edge(0, 2)
    g.add_edge(1, 3)
    g.add_edge(1, 4)

    assert g.adj_list[0].vertex == 2
    assert g.adj_list[0].next.vertex == 1

    assert g.adj_list[1].vertex == 4
    assert g.adj_list[1].next.vertex == 3
    assert g.adj_list[1].next.next.vertex == 0

    assert g.adj_list[2].vertex == 0
    assert g.adj_list[3].vertex == 1
    assert g.adj_list[4].vertex == 1

def test_print_graph():
    g = Graph(5)
    g.add_edge(0, 1)
    g.add_edge(0, 2)
    g.add_edge(1, 3)
    g.add_edge(1, 4)

    import io
    import sys

    output = io.StringIO()
    sys.stdout = output
    g.print_graph()
    sys.stdout = sys.__stdout__

    expected_output = ["Vertex 0: -> 2 -> 1",
                       "Vertex 1: -> 4 -> 3 -> 0",
                       "Vertex 2: -> 0",
                       "Vertex 3: -> 1",
                       "Vertex 4: -> 1"]

    actual_output = [line for line in output.getvalue().splitlines() if line.strip()]

    assert len(expected_output) == len(actual_output)

    for expected_line, actual_line in zip(expected_output, actual_output):
        assert expected_line.strip() == actual_line.strip()

def test_degree():
    graph = Graph(4)
    graph.add_edge(0, 1)
    graph.add_edge(1, 2)
    graph.add_edge(2, 3)
    graph.add_edge(3, 0)
    assert graph.degree(1) == 2

    graph = Graph(5)
    graph.add_edge(0, 1)
    graph.add_edge(1, 2)
    graph.add_edge(2, 3)
    graph.add_edge(3, 4)
    assert graph.degree(3) == 2

def test_neighbors():
    graph = Graph(4)
    graph.add_edge(0, 1)
    graph.add_edge(1, 2)
    graph.add_edge(2, 3)
    graph.add_edge(3, 0)
    assert graph.neighbors(1) == [2, 0]

    graph = Graph(5)
    graph.add_edge(0, 1)
    graph.add_edge(1, 2)
    graph.add_edge(2, 3)
    graph.add_edge(3, 4)
    assert graph.neighbors(2) == [3, 1]

def test_connected_components_empty_graph():
    graph = Graph(0)
    assert graph.connected_components() == []

def test_connected_components_single_component():
    graph = Graph(5)
    graph.add_edge(0, 1)
    graph.add_edge(1, 2)
    graph.add_edge(1, 3)
    graph.add_edge(2, 4)
    expected_components = [[0, 1, 2, 3, 4]]
    result_components = graph.connected_components()
    # Sort the vertices within the connected components for comparison
    result_components = [sorted(component) for component in result_components]
    assert result_components == expected_components


def test_connected_components_multiple_components():
    graph = Graph(6)
    graph.add_edge(0, 1)
    graph.add_edge(1, 2)
    graph.add_edge(3, 4)
    expected_components = [[0, 1, 2], [3, 4], [5]]
    assert graph.connected_components() == expected_components
