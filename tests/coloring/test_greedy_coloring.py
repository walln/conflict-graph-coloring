from algo.coloring.greedy import greedy_coloring
from algo.generation.complete import generate_complete_graph
from algo.generation.cyclic import generate_cyclic_graph
from algo.ordering.connected_sequential_ordering import connected_sequential_ordering
from algo.ordering.smallest_last import smallest_last_vertex_ordering
from algo.ordering.smallest_original_degree_last import smallest_original_degree_last_vertex_ordering
from algo.ordering.largest_last import largest_last_vertex_ordering
from algo.ordering.largest_original_degree_last import largest_original_degree_last_vertex_ordering
from algo.structures.graph import Graph

def is_valid_coloring(graph: Graph, colors: dict[int, int]) -> bool:
    """
    Check if a given coloring is valid for the given graph.

    :param graph: The graph object.
    :param colors: The coloring represented as a dictionary where keys are vertex indices and values are the colors.
    :return: True if the coloring is valid, False otherwise.
    """
    for u, v in graph.edges():
        if colors[u] == colors[v]:
            return False
    return True


def test_greedy_coloring_1():
    """
    A simple path with three vertices (0 - 1 - 2):
    0 -- 1 -- 2
    """
    graph = Graph(3)
    graph.add_edge(0, 1)
    graph.add_edge(1, 2)
    ordering = [0, 1, 2]
    colors = greedy_coloring(graph, ordering)
    assert colors == {0: 0, 1: 1, 2: 0}, f"Expected {{0: 0, 1: 1, 2: 0}}, but got {colors}"

def test_greedy_coloring_2():
    """
    A small cycle with four vertices (0 - 1 - 2 - 3 - 0):
    0 -- 1
    |    |
    3 -- 2

    """
    graph = Graph(4)
    graph.add_edge(0, 1)
    graph.add_edge(1, 2)
    graph.add_edge(2, 3)
    graph.add_edge(3, 0)
    ordering = [0, 1, 2, 3]
    colors = greedy_coloring(graph, ordering)
    assert colors == {0: 0, 1: 1, 2: 0, 3: 1}, f"Expected {{0: 0, 1: 1, 2: 0, 3: 1}}, but got {colors}"

def test_greedy_coloring_3():
    """
    A small tree with five vertices:
        0
       / \
      1   2
     / \
    3   4
    """
    graph = Graph(5)
    graph.add_edge(0, 1)
    graph.add_edge(0, 2)
    graph.add_edge(1, 3)
    graph.add_edge(1, 4)
    ordering = [0, 1, 2, 3, 4]
    colors = greedy_coloring(graph, ordering)
    assert colors == {0: 0, 1: 1, 2: 1, 3: 0, 4: 0}, f"Expected {{0: 0, 1: 1, 2: 1, 3: 0, 4: 0}}, but got {colors}"

def test_greedy_coloring_4():
    """
    A graph with two disconnected components:
    0 - 1 - 2      3 - 4
    |   |   |      |   |
    5 - 6 - 7      8 - 9
    """
    graph = Graph(10)
    graph.add_edge(0, 1)
    graph.add_edge(1, 2)
    graph.add_edge(0, 5)
    graph.add_edge(1, 6)
    graph.add_edge(2, 7)
    graph.add_edge(5, 6)
    graph.add_edge(6, 7)
    graph.add_edge(3, 4)
    graph.add_edge(3, 8)
    graph.add_edge(4, 9)
    graph.add_edge(8, 9)
    ordering = [0, 1, 2, 5, 6, 7, 3, 4, 8, 9]
    colors = greedy_coloring(graph, ordering)
    assert colors == {0: 0, 1: 1, 2: 0, 3: 0, 4: 1, 5: 1, 6: 0, 7: 1, 8: 1, 9: 0}, \
        f"Expected {{0: 0, 1: 1, 2: 0, 3: 0, 4: 1, 5: 1, 6: 0, 7: 1, 8: 1, 9: 0}}, but got {colors}"

def test_greedy_coloring_5():
    """
    A graph with a cycle and a path attached to it:
    0 - 1 - 2
    |       |
    3 - 4 - 5 - 6
            |
            7
    """
    graph = Graph(8)
    graph.add_edge(0, 1)
    graph.add_edge(1, 2)
    graph.add_edge(2, 5)
    graph.add_edge(5, 4)
    graph.add_edge(4, 3)
    graph.add_edge(3, 0)
    graph.add_edge(5, 6)
    graph.add_edge(5, 7)
    ordering = [0, 1, 2, 3, 4, 5, 6, 7]
    colors = greedy_coloring(graph, ordering)
    assert colors == {0: 0, 1: 1, 2: 0, 3: 1, 4: 0, 5: 1, 6: 0, 7: 0}, \
        f"Expected {{0: 0, 1: 1, 2: 0, 3: 1, 4: 0, 5: 1, 6: 0, 7: 0}}, but got {colors}"

def test_greedy_coloring_6():
    """
    A complete bipartite graph:
    0 - 4
    |   |
    1 - 5
    |   |
    2 - 6
    |   |
    3 - 7
    """
    graph = Graph(8)
    graph.add_edge(0, 4)
    graph.add_edge(0, 5)
    graph.add_edge(0, 6)
    graph.add_edge(0, 7)
    graph.add_edge(1, 4)
    graph.add_edge(1, 5)
    graph.add_edge(1, 6)
    graph.add_edge(1, 7)
    graph.add_edge(2, 4)
    graph.add_edge(2, 5)
    graph.add_edge(2, 6)
    graph.add_edge(2, 7)
    graph.add_edge(3, 4)
    graph.add_edge(3, 5)
    graph.add_edge(3, 6)
    graph.add_edge(3, 7)
    ordering = [0, 4, 1, 5, 2, 6, 3, 7]
    colors = greedy_coloring(graph, ordering)
    assert colors == {0: 0, 1: 0, 2: 0, 3: 0, 4: 1, 5: 1, 6: 1, 7: 1}, \
        f"Expected {{0: 0, 1: 0, 2: 0, 3: 0, 4: 1, 5: 1, 6: 1, 7: 1}}, but got {colors}"

def test_greedy_coloring_7():
    """
    A cycle with 4 vertices
    0 -- 1
    |    |
    3 -- 2
    """
    graph = Graph(4)
    graph.add_edge(0, 1)
    graph.add_edge(1, 2)
    graph.add_edge(2, 3)
    graph.add_edge(3, 0)
    ordering, _ = smallest_last_vertex_ordering(graph)
    colors = greedy_coloring(graph, ordering)
    assert max(colors.values()) <= 1, f"Expected 2 colors, but got {max(colors.values()) + 1}"


def test_greedy_coloring_8():
    """
    A simple path with 3 vertices
    0 -- 1 -- 2
    """
    graph = Graph(3)
    graph.add_edge(0, 1)
    graph.add_edge(1, 2)
    ordering, _ = smallest_last_vertex_ordering(graph)
    colors = greedy_coloring(graph, ordering)
    assert max(colors.values()) <= 1, f"Expected 2 colors, but got {max(colors.values()) + 1}"

def test_greedy_coloring_9():
    """
    A cycle with 4 vertices
    0 -- 1
    |    |
    3 -- 2
    """
    graph = Graph(4)
    graph.add_edge(0, 1)
    graph.add_edge(1, 2)
    graph.add_edge(2, 3)
    graph.add_edge(3, 0)
    ordering, _ = smallest_original_degree_last_vertex_ordering(graph)
    colors2_1 = greedy_coloring(graph, ordering)
    assert max(colors2_1.values()) <= 1, f"Expected 2 colors, but got {max(colors2_1.values()) + 1}"

def test_greedy_coloring_10():
    """
    A simple path with 3 vertices
    0 -- 1 -- 2

    """
    graph = Graph(3)
    graph.add_edge(0, 1)
    graph.add_edge(1, 2)
    ordering, _ = smallest_original_degree_last_vertex_ordering(graph)
    colors = greedy_coloring(graph, ordering)
    assert max(colors.values()) <= 1, f"Expected 2 colors, but got {max(colors.values()) + 1}"

def test_greedy_coloring_11():
    """
    A graph with two disjoint cycles
    0 -- 1 -- 2
         |
    3 -- 4 -- 5
    """
    graph = Graph(6)
    graph.add_edge(0, 1)
    graph.add_edge(1, 2)
    graph.add_edge(1, 4)
    graph.add_edge(3, 4)
    graph.add_edge(4, 5)
    ordering, _ = smallest_last_vertex_ordering(graph)
    colors = greedy_coloring(graph, ordering)
    assert max(colors.values()) <= 2, f"Expected 3 colors, but got {max(colors.values()) + 1}"

def test_greedy_coloring_12():
    """
    A tree-like graph
         3
         |
    0 -- 1 -- 2
         |
         4
    """
    graph = Graph(5)
    graph.add_edge(0, 1)
    graph.add_edge(1, 2)
    graph.add_edge(1, 3)
    graph.add_edge(1, 4)
    ordering, _ = smallest_original_degree_last_vertex_ordering(graph)
    colors = greedy_coloring(graph, ordering)
    assert max(colors.values()) <= 1, f"Expected 2 colors, but got {max(colors.values()) + 1}"

def test_greedy_coloring_13():
    """
    A central hub with multiple branches
         4
         |
    3 -- 0 -- 1 -- 5
         |
         2
    """
    graph = Graph(6)
    graph.add_edge(0, 1)
    graph.add_edge(0, 2)
    graph.add_edge(0, 3)
    graph.add_edge(0, 4)
    graph.add_edge(1, 5)
    ordering, _ = smallest_last_vertex_ordering(graph)
    colors = greedy_coloring(graph, ordering)
    assert max(colors.values()) <= 2, f"Expected 3 colors, but got {max(colors.values()) + 1}"

def test_greedy_coloring_14():
    """
    A graph with a cycle and a few branches
         5
         |
    0 -- 1 -- 2
    |    |    |
    4 -- 3    6
    """
    graph = Graph(7)
    graph.add_edge(0, 1)
    graph.add_edge(1, 2)
    graph.add_edge(1, 3)
    graph.add_edge(1, 5)
    graph.add_edge(2, 6)
    graph.add_edge(3, 4)
    graph.add_edge(4, 0)
    ordering, _ = smallest_original_degree_last_vertex_ordering(graph)
    colors = greedy_coloring(graph, ordering)
    assert max(colors.values()) <= 2, f"Expected 3 colors, but got {max(colors.values()) + 1}"

def test_greedy_coloring_15():
    """
    A graph with two connected cycles
    0 -- 1 -- 2
    |    |    |
    5 -- 4 -- 3
    """
    graph = Graph(6)
    graph.add_edge(0, 1)
    graph.add_edge(1, 2)
    graph.add_edge(2, 3)
    graph.add_edge(3, 4)
    graph.add_edge(4, 5)
    graph.add_edge(5, 0)
    graph.add_edge(1, 4)
    ordering, _ = largest_last_vertex_ordering(graph)
    colors = greedy_coloring(graph, ordering)
    assert max(colors.values()) <= 2, f"Expected 3 colors, but got {max(colors.values()) + 1}"


def test_greedy_coloring_16():
    """
    A graph with a cycle and an extended branch
         6
         |
    0 -- 1 -- 2
    |    |
    3 -- 4 -- 5
    """
    graph = Graph(7)
    graph.add_edge(0, 1)
    graph.add_edge(1, 2)
    graph.add_edge(1, 4)
    graph.add_edge(1, 6)
    graph.add_edge(0, 3)
    graph.add_edge(3, 4)
    graph.add_edge(4, 5)
    ordering, _ = largest_last_vertex_ordering(graph)
    colors = greedy_coloring(graph, ordering)
    assert max(colors.values()) <= 2, f"Expected 3 colors, but got {max(colors.values()) + 1}"

def test_greedy_coloring_17():
    """
    A graph with a star topology
         4
         |
    2 -- 0 -- 1
         |
         3
    """
    graph = Graph(5)
    graph.add_edge(0, 1)
    graph.add_edge(0, 2)
    graph.add_edge(0, 3)
    graph.add_edge(0, 4)
    ordering, _ = largest_last_vertex_ordering(graph)
    colors = greedy_coloring(graph, ordering)
    assert max(colors.values()) <= 1, f"Expected 2 colors, but got {max(colors.values()) + 1}"


def test_greedy_coloring_18():
    """
    A graph with two disconnected components
    0 -- 1 -- 2      3 -- 4
    |    |    |      |    |
    7 -- 6 -- 5      9 -- 8
    """
    graph = Graph(10)
    graph.add_edge(0, 1)
    graph.add_edge(1, 2)
    graph.add_edge(1, 6)
    graph.add_edge(2, 5)
    graph.add_edge(5, 6)
    graph.add_edge(6, 7)
    graph.add_edge(0, 7)
    graph.add_edge(3, 4)
    graph.add_edge(4, 8)
    graph.add_edge(3, 9)
    graph.add_edge(8, 9)
    ordering, _ = largest_last_vertex_ordering(graph)
    colors = greedy_coloring(graph, ordering)
    assert max(colors.values()) <= 1, f"Expected 2 colors, but got {max(colors.values()) + 1}"

def test_greedy_coloring_19():
    """
    A graph with a cycle and a few branches
         5
         |
    0 -- 1 -- 2
    |    |    |
    4 -- 3    6
    """
    graph = Graph(7)
    graph.add_edge(0, 1)
    graph.add_edge(1, 2)
    graph.add_edge(1, 3)
    graph.add_edge(1, 5)
    graph.add_edge(2, 6)
    graph.add_edge(3, 4)
    graph.add_edge(4, 0)
    ordering, _ = largest_original_degree_last_vertex_ordering(graph)
    colors = greedy_coloring(graph, ordering)
    assert max(colors.values()) <= 2, f"Expected 3 colors, but got {max(colors.values()) + 1}"

def test_greedy_coloring_20():
    """
    A tree-like graph
         3
         |
    0 -- 1 -- 2
         |
         4
    """
    graph = Graph(5)
    graph.add_edge(0, 1)
    graph.add_edge(1, 2)
    graph.add_edge(1, 3)
    graph.add_edge(1, 4)
    ordering, _ = largest_original_degree_last_vertex_ordering(graph)
    colors = greedy_coloring(graph, ordering)
    assert max(colors.values()) <= 1, f"Expected 2 colors, but got {max(colors.values()) + 1}"

def test_connected_sequential_ordering_greedy_coloring_1():
    """
    A graph with two separate cycles
    Component 1: 0 - 1 - 2 - 0
    Component 2: 3 - 4 - 5 - 3
    """
    graph = Graph(6)
    graph.add_edge(0, 1)
    graph.add_edge(1, 2)
    graph.add_edge(2, 0)
    graph.add_edge(3, 4)
    graph.add_edge(4, 5)
    graph.add_edge(5, 3)
    ordering, _ = connected_sequential_ordering(graph)
    colors = greedy_coloring(graph, ordering)
    max_colors = max(colors.values()) + 1
    assert max_colors <= 3, f"Expected at most 3 colors, but got {max_colors}"

def test_connected_sequential_ordering_greedy_coloring_2():
    graph = Graph(8)
    graph.add_edge(0, 1)
    graph.add_edge(0, 3)
    graph.add_edge(1, 2)
    graph.add_edge(1, 4)
    graph.add_edge(2, 5)
    graph.add_edge(3, 4)
    graph.add_edge(3, 6)

    ordering, _ = connected_sequential_ordering(graph)
    colors = greedy_coloring(graph, ordering)

    # Check that the colors of connected vertices are different
    for u, v in graph.edges():
        assert colors[u] != colors[v], f"Vertices {u} and {v} have the same color"

    # Check that the isolated vertex 7 has a color assigned
    assert 7 in colors, "Isolated vertex 7 has no color assigned"

def test_greedy_coloring_complete_graph_1():
    """
    Test greedy coloring on a complete graph with 5 vertices.
    """
    graph = generate_complete_graph(5)
    ordering = graph.vertices()
    colors = greedy_coloring(graph, ordering)
    assert max(colors.values()) == 4, f"Expected 5 colors, but got {max(colors.values()) + 1}"


def test_greedy_coloring_complete_graph_2():
    """
    Test greedy coloring on a complete graph with 6 vertices.
    """
    graph = generate_complete_graph(6)
    ordering = graph.vertices()
    colors = greedy_coloring(graph, ordering)
    assert max(colors.values()) == 5, f"Expected 6 colors, but got {max(colors.values()) + 1}"


def test_greedy_coloring_cyclic_graph_1():
    """
    Test the greedy coloring algorithm on a cyclic graph with 3 vertices.
    """
    graph = generate_cyclic_graph(3)
    ordering = graph.vertices()
    colors = greedy_coloring(graph, ordering)

    assert is_valid_coloring(graph, colors)


def test_greedy_coloring_cyclic_graph_2():
    """
    Test the greedy coloring algorithm on a cyclic graph with 6 vertices.
    """
    graph = generate_cyclic_graph(6)
    ordering = graph.vertices()
    colors = greedy_coloring(graph, ordering)

    assert is_valid_coloring(graph, colors)

def test_greedy_coloring_cyclic_graph_3():
    """
    Test the greedy coloring algorithm on a cyclic graph with 12 verticess.
    """
    graph = generate_cyclic_graph(12)
    ordering = graph.vertices()
    colors = greedy_coloring(graph, ordering)

    assert is_valid_coloring(graph, colors)
