import os
import random
import time
from typing import Dict, List

import matplotlib.pyplot as plt
import numpy as np

from algo.generation.complete import generate_complete_graph
from algo.generation.cyclic import generate_cyclic_graph
from algo.generation.power_law import generate_power_law_random_graph
from algo.generation.skewed_random import generate_skewed_random_graph
from algo.generation.uniform_random import generate_uniform_random_graph


def test_method(method_name, generator_function, sizes):
    times = []
    conflicts_by_size: List[List[int]] = []

    for size in sizes:
        print(f'Generating a {method_name} graph of size {size}... starting at {time.ctime()}')
        random.seed(42)

        if method_name not in ["complete", "cyclic"]:
            start_time = time.perf_counter()
            graph = generator_function(size[0], size[1])
            end_time = time.perf_counter()
        else:
            start_time = time.perf_counter()
            graph = generator_function(size[0])
            end_time = time.perf_counter()

        run_time = end_time - start_time
        times.append(run_time)

        conflicts = [graph.degree(vertex) for vertex in graph.vertices()]
        conflicts_by_size.append(conflicts)
        # Log data
        print(f'Graph generated in {(run_time):.6f} seconds.')
        print(f'Number of conflicts: {sum(conflicts)}')


    return (times, conflicts_by_size)

def edge_sizes(n):
    return int((n * (n - 1) / 2) / 4)


def test():
    vertex_sizes = [10, 25, 50, 75, 100, 200, 300, 400, 500, 750, 1000, 1500, 2000, 3000, 5000]
    sizes = [(vertex_size, edge_sizes(vertex_size)) for vertex_size in vertex_sizes]

    methods = {
        "complete": generate_complete_graph,
        "cyclic": generate_cyclic_graph,
        "power_law": generate_power_law_random_graph,
        "uniform_random": generate_uniform_random_graph,
        "skewed_random": generate_skewed_random_graph,
    }

    conflicts_per_method: Dict[str, List[List[int]]] = {}

    for method_name, generator_function in methods.items():
        times, conflicts = test_method(method_name, generator_function, sizes)
        conflicts_per_method[method_name] = conflicts

        # Make a result folder for each method or clear the existing one
        folder_path = "generation_tests" + "/" + method_name

        if not os.path.exists(folder_path):
            os.mkdir(folder_path)

        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                os.rmdir(file_path)

        # Plot the times for each method
        fig, ax = plt.subplots()

        # Plot the data as a line plot
        ax.plot([x for x, y in sizes], times)

        # Set the axis labels and title
        ax.set_xlabel('Graph Size')
        ax.set_ylabel('Generation Time (s)')
        ax.set_title('Generation Time vs. Graph Size')

        # Display the plot
        # plt.show()

        fig.savefig(folder_path + "/times.png")

        # Save a table of the runtime data
        with open(folder_path + "/times.txt", "w") as f:
            f.write('Graph Size\tGeneration Time (s)\n')
            for i in range(len(sizes)):
                f.write(f'{sizes[i][0]}\t{times[i]}\n')

    for size_index, (num_vertices, num_edges) in enumerate(sizes):
        plt.figure()
        plt.title(f"Graph conflicts per vertex (n={num_vertices})")
        plt.xlabel("Vertex")
        plt.ylabel("Number of conflicts")
        plt.xticks(range(num_vertices))

        bottom = np.zeros(num_vertices)

        for method, conflicts_per_size in conflicts_per_method.items():
            conflicts = conflicts_per_size[size_index]
            plt.bar(range(num_vertices), conflicts, bottom=bottom, label=method.capitalize())
            bottom += conflicts

        plt.gca().xaxis.set_tick_params(labelbottom=False)


        plt.legend(loc='upper right', bbox_to_anchor=(1.5, 1))
        plt.subplots_adjust(right=0.7)
        plt.savefig(f"generation_tests/conflicts_{num_vertices}.png")


test()
