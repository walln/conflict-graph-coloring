from argparse import ArgumentParser
import datetime
import time

from algo.structures.graph import Graph, terminal_clique_size
from algo.generation.complete import generate_complete_graph
from algo.generation.cyclic import generate_cyclic_graph
from algo.generation.power_law import generate_power_law_graph
from algo.generation.skewed_random import generate_skewed_graph
from algo.generation.uniform_random import generate_uniform_random_graph

from algo.ordering.incidence import incidence_ordering
from algo.ordering.connected_sequential_ordering import connected_sequential_ordering
from algo.ordering.largest_last import largest_last_vertex_ordering
from algo.ordering.largest_original_degree_last import largest_original_degree_last_vertex_ordering
from algo.ordering.smallest_last import smallest_last_vertex_ordering
from algo.ordering.smallest_original_degree_last import smallest_original_degree_last_vertex_ordering

from algo.coloring.greedy import greedy_coloring

from algo.serialization.graph import write_graph_to_file, read_graph_from_file

import os

SEPERATOR_LENGTH = 43

def is_valid_filename(filename):
    """
    Check whether the given filename is valid and writable.

    Args:
        filename (str): The filename to validate.

    Returns:
        bool: True if the filename is valid and writable, False otherwise.
    """
    if not isinstance(filename, str) or not filename:
        return False

    if not all(c.isprintable() and c not in ['/', '\\', ':', '*', '?', '<', '>', '|'] for c in filename):
        return False

    if os.path.isdir(filename):
        return False

    if os.path.isfile(filename) and not os.access(filename, os.W_OK):
        return False

    if not os.access(os.path.dirname(os.path.abspath(filename)), os.W_OK):
        return False

    return True



def complete_edge_count(V: int):
    return int(V * (V - 1) / 2)

def cli_p1():
    """
    Part 1 of the CLI, generates a graph and outputs it to a file.
    Using the selected output file, number of edges, number of vertices,
    and graph generation method, a graph is generated and output to the
    selected file.
    """
    parser = ArgumentParser()
    parser.add_argument("-o",
                        "--output_file",
                        help="Output File name",
                        type=str,
                        required=True)
    parser.add_argument("-v",
                        "--vertices",
                        help="How many vertices to add to the graph.",
                        type=int,
                        required=True)
    parser.add_argument("-e",
                        "--edges",
                        help="How many edges to add to the graph.",
                        type=int,
                        required=True)
    parser.add_argument("-g",
                        "--generator",
                        help="Graph generation method.",
                        type=str,
                        choices=['complete', 'power_law', 'uniform_random', 'skewed_random', 'cyclic'],
                        required=True)

    args = parser.parse_args()

    methods = {
        "complete": generate_complete_graph,
        "power_law": generate_power_law_graph,
        "uniform_random": generate_uniform_random_graph,
        "skewed_random" : generate_skewed_graph,
        "cyclic": generate_cyclic_graph
    }

    V: int = args.vertices
    E: int = args.edges

    if args.generator not in methods:
        raise ValueError("Invalid graph generation method.")

    output_fname = args.output_file
    if not is_valid_filename(output_fname):
        raise ValueError("Invalid output filename.")

    method = methods[args.generator]

    if V > 10_000:
        raise ValueError("Input vertex amount exceeds maximum of 10,000.")
    if E > 2_000_000:
        raise ValueError("Input edge amount exceeds maximum of 2,000,000.")
    if args.generator == "complete" and E != complete_edge_count(V):
        raise ValueError(f'For a complete graph with {V} edges {complete_edge_count(V)} edges must exist.')

    print('-' * SEPERATOR_LENGTH)
    print("Using the following arguments:")
    print(f'{"Output file:":<30} {output_fname} 📄')
    print(f'{"Vertices:":<30} {V} 📏')
    print(f'{"Edges:":<30} {E} 📏')
    print(f'{"Graph generation method:":<30} {args.generator} 📈')
    print('-' * SEPERATOR_LENGTH)

    print(f'{"Generating graph..."} 📊')

    graph: Graph = method(V, E) if args.generator != "complete" else method(V)
    print('Graph generated 🎉')

    write_graph_to_file(graph, output_fname)
    print(f'Graph written to {output_fname} 🚀')


def cli_p2():
    """
    Part 2 of the CLI, reads a graph from a file, and using a selected ordering
    method will color the graph and output the the coloring to a file.
    """
    parser = ArgumentParser()
    parser.add_argument("-i",
                        "--input_file",
                        help="Input File name",
                        type=str,
                        required=True)
    parser.add_argument("-f",
                        "--output_file",
                        help="Output File name",
                        type=str,
                        default="coloring.txt",
                        required=False)
    parser.add_argument("-o",
                        "--ordering",
                        help="Ordering method to use for graph coloring.",
                        type=str,
                        choices=['smallest_last',
                                 'smallest_original_degree_last',
                                 'largest_last',
                                 'largest_original_degree_last',
                                 'incidence',
                                 'connected_sequential'],
                        required=True)

    args = parser.parse_args()

    orderings = {
        'smallest_last': smallest_last_vertex_ordering,
        'smallest_original_degree_last': smallest_original_degree_last_vertex_ordering,
        'largest_last': largest_last_vertex_ordering,
        'largest_original_degree_last': largest_original_degree_last_vertex_ordering,
        'incidence': incidence_ordering,
        'connected_sequential': connected_sequential_ordering
    }

    ordering = orderings[args.ordering]

    input_fname = args.input_file
    if not is_valid_filename(input_fname):
        raise ValueError("Invalid input filename.")

    output_fname = args.output_file
    if not is_valid_filename(output_fname):
        raise ValueError("Invalid output filename.")

    print('-' * SEPERATOR_LENGTH)
    print("Using the following arguments:")
    print(f'{"Input file:":<30} {input_fname} 📄')
    print(f'{"Output file:":<30} {output_fname} 📄')
    print(f'{"Ordering method:":<30} {args.ordering} 📈')
    print('-' * SEPERATOR_LENGTH)

    print(f'{"Reading graph from file..."} 📊')
    graph = read_graph_from_file(input_fname)
    print('Graph read from file🎉')
    print(f'{"Vertex count:":<30} {len(graph.vertices())} 📏')
    print(f'{"Edge count:":<30} {len(graph.edges())} 📏')
    print(f'{"Terminal clique size:":<30}{terminal_clique_size(graph)} 📏')
    average_original_degree = sum([graph.degree(v) for v in graph.vertices()]) / len(graph.vertices())
    print(f'{"Average original degree:":<30}{average_original_degree} 📏')
    print('-' * SEPERATOR_LENGTH)

    print(f'{"Ordering graph using:":<30} {args.ordering}... 🔢')
    order, meta = ordering(graph)

    if 'ordering_time' in meta:
        order_time = meta['ordering_time']
        ordering_time_str = str(datetime.timedelta(seconds=order_time))
        print(f'{"Ordering time:":<30} {ordering_time_str} ⏱️')
    else:
        print(f'{"Ordering time:":<30} {"N/A"} ⏱️')

    if 'deleted_degrees' in meta:
        deleted_degrees = meta['deleted_degrees']
        print(f'{"Vertex degree when deleted:":<30}')
        for vertex, degree in deleted_degrees.items():
            print(f'{vertex}: {degree} 📏')

    print('-' * SEPERATOR_LENGTH)

    print(f'{"Coloring graph..."} 🎨')
    coloring_start_time = time.time()
    coloring = greedy_coloring(graph, order)
    coloring_time = time.time() - coloring_start_time

    print(f'{"Coloring time:":<30} {str(datetime.timedelta(seconds=coloring_time))} ⏱️')
    colors_used = len(set(coloring.values()))
    print(f'{"Colors used:":<30} {colors_used} 📏')
    print('-' * SEPERATOR_LENGTH)

    # Now we need to write the coloring to a file
    # The format for this is such that each line follows the format:
    # VERTEX_NUMBER, COLOR_NUMBER

    print(f'{"Writing coloring to file..."} 📄')
    with open(output_fname, 'w') as f:
        for vertex, color in coloring.items():
            f.write(f'{vertex},{color}\n')
    print(f'{"Coloring written to file."} 🚀')

    # TODO:
    # Graph results (needs above ^)
    # Maybe add more ordering methods
    # Cleanup repo
    # Write paper

if __name__ == "__main__":
    cli_p1()
