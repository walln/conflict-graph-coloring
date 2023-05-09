import random
import time
from typing import Dict
from algo.generation.complete import generate_complete_graph
from algo.generation.cyclic import generate_cyclic_graph
from algo.generation.power_law import generate_power_law_random_graph
from algo.generation.skewed_random import generate_skewed_random_graph
from algo.generation.uniform_random import generate_uniform_random_graph
from algo.ordering.smallest_last import smallest_last_vertex_ordering
from algo.ordering.smallest_original_degree_last import smallest_original_degree_last_vertex_ordering
from algo.ordering.largest_last import largest_last_vertex_ordering
from algo.ordering.largest_original_degree_last import largest_original_degree_last_vertex_ordering
from algo.ordering.incidence import incidence_ordering
from algo.ordering.connected_sequential_ordering import connected_sequential_ordering
from algo.coloring.greedy import greedy_coloring
from algo.structures.graph import terminal_clique_size2
import os
import matplotlib.pyplot as plt

from algo.structures.graph import Graph

SEPERATOR_LENGTH = 43


def edge_sizes(n):
    return int((n * (n - 1) / 2) / 4)


def test_orderings(graph: Graph):
    # Take a graph and run each ordering on it
    smallest_last_max_dd = 0
    colors_used = {}
    tq_size = 0

    deleted_degrees: Dict[int, int] = {}
    sl_order = []

    for method, func in orderings.items():
        print('-' * SEPERATOR_LENGTH)
        print(f'Running {method}... starting at {time.ctime()}')
        start = time.perf_counter()
        order, meta = func(graph)
        colors = greedy_coloring(graph, order)
        num_colors = max(colors.values()) + 1
        end = time.perf_counter()
        print(f'{method} completed at {time.ctime()}.')
        print(f'Elaspsed time: {(end - start):.6f} seconds.')

        colors_used[method] = num_colors

        if method == "smallest_last":
            deleted_degrees: Dict[int, int] = meta["deleted_degrees"]
            max_deleted_degree = max(deleted_degrees.values())
            smallest_last_max_dd = max_deleted_degree
            sl_order = order

            print("TQ")
            tq_size = terminal_clique_size2(graph)



    return (colors_used, smallest_last_max_dd, tq_size, deleted_degrees, sl_order)

orderings = {
    "smallest_last": smallest_last_vertex_ordering,
    "smallest_original_last": smallest_original_degree_last_vertex_ordering,
    "largest_last": largest_last_vertex_ordering,
    "largest_original_last": largest_original_degree_last_vertex_ordering,
    "incidence": incidence_ordering,
    "connected_sequential": connected_sequential_ordering,
}

generation_methods = {
        "complete": generate_complete_graph,
        "cyclic": generate_cyclic_graph,
        "power_law": generate_power_law_random_graph,
        "uniform_random": generate_uniform_random_graph,
        "skewed_random": generate_skewed_random_graph,
}

def test():
    vertex_sizes = [10, 25, 50, 75, 100, 150]
    sizes = [(vertex_size, edge_sizes(vertex_size)) for vertex_size in vertex_sizes]

    times = []

    data = {}

    clique_sizes = {}
    max_dd_size = []

    dds = {}
    sl_orders = {}


    for (vertex_size, edge_size) in sizes:

        for method, generator in generation_methods.items():
            print('-' * SEPERATOR_LENGTH)
            print(f'Generating a {method} graph of size {vertex_size}... starting at {time.ctime()}')
            random.seed(42)
            start_time = time.perf_counter()
            if method not in ["complete", "cyclic"]:
                start_time = time.perf_counter()
                graph = generator(vertex_size, edge_size)
                end_time = time.perf_counter()
            else:
                start_time = time.perf_counter()
                graph = generator(vertex_size)
                end_time = time.perf_counter()
                end_time = time.perf_counter()
            run_time = end_time - start_time
            times.append(run_time)
            print(f'Graph generated in {(run_time):.6f} seconds.')

            colors_used, smallest_last_max_dd, tq_size, sl_deleted_degrees, sl_order = test_orderings(graph)

            if vertex_size not in dds:
                dds[vertex_size] = {}

            if vertex_size not in sl_orders:
                sl_orders[vertex_size] = {}

            if vertex_size not in clique_sizes:
                clique_sizes[vertex_size] = {}

            dds[vertex_size][method] = sl_deleted_degrees
            sl_orders[vertex_size][method] = sl_order
            clique_sizes[vertex_size][method] = tq_size

            print('-' * SEPERATOR_LENGTH)
            print('-' * SEPERATOR_LENGTH)

            for key, value in colors_used.items():
                print(f'{key} used : {value} colors')

            print('-' * SEPERATOR_LENGTH)

            print('Smallest Last Specific Data:')
            print(f'Smallest last max deleted degree: {smallest_last_max_dd}')
            max_dd_size.append(smallest_last_max_dd)
            print(f'Terminal clique size: {tq_size}')
            print('')

            data[vertex_size] = {} if vertex_size not in data else data[vertex_size]
            data[vertex_size][method] = {}

            for ordering_method in orderings.keys():
                data[vertex_size][method][ordering_method] = colors_used[ordering_method]

            # Make a result folder for each method or clear the existing one
            folder_path = "ordering_tests" + "/" + method

            if not os.path.exists(folder_path):
                os.mkdir(folder_path)

            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    os.rmdir(file_path)



    # Now we plot the deleted degrees

    for size in vertex_sizes:

        for method in generation_methods.keys():
            x_coords = list(range(0, len(sl_orders[size][method])))

            y_coords = list(reversed([dds[size][method][vertex] for vertex in sl_orders[size][method]]))
            plt.plot(x_coords, y_coords, label=method)

        # Set the x-axis label and title
        plt.xlabel('Order of Vertex Deletion')
        plt.ylabel('Vertex Degree at Deletion')
        plt.title(f'Vertex Degrees over Time n={size}')

        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

        # Display the plot
        plt.show()


    # COMPARE COLORING

    # List of ordering methods to compare
    ordering_methods = ["smallest_last",
                        "smallest_original_last",
                        "largest_last",
                        "largest_original_last",
                        "incidence",
                        "connected_sequential"]

    # List of graph types to compare
    graph_types = ["complete", "cyclic", "power_law", "uniform_random", "skewed_random"]

    # List of data sizes to compare
    data_sizes = vertex_sizes



    # Create a subplot for each graph type
    fig, axs = plt.subplots(nrows=int(len(graph_types) / 2)+1, ncols=2, figsize=(12, 16))

    # Iterate over each graph type
    for i, graph_type in enumerate(graph_types):
        row_idx = i // 2
        col_idx = i % 2

        # Create a subplot for the current graph type
        ax = axs[row_idx, col_idx]


        # Iterate over each data size
        for data_size in data_sizes:
            # Initialize a list to store the performance data for each ordering method
            performance_data = []

            # Iterate over each ordering method
            for ordering_method in ordering_methods:
                # Get the performance data for the current ordering method, graph type, and data size
                colors_used = data[data_size][graph_type][ordering_method]
                # Calculate the performance metric (e.g. number of colors used)

                # Add the performance metric to the list
                performance_data.append(colors_used)

            # Plot the performance data for the current data size
            ax.plot(ordering_methods, performance_data, label=f"n={data_size}")

        # Set the title and axis labels for the current subplot
        ax.set_title(f"Graph Type: {graph_type}")
        ax.set_xlabel("Ordering Method")
        ax.set_ylabel("Performance Metric")
        ax.set_ylim(bottom=0)

        # Add a legend to the current subplot
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    # Adjust the spacing between subplots
    fig.tight_layout()

    # Show the plots
    plt.show()

    print("TQ SIZES:", clique_sizes)











test()
