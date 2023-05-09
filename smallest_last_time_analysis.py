import time
from algo.generation.uniform_random import generate_uniform_random_graph
from algo.ordering.smallest_last import smallest_last_vertex_ordering
import os
import matplotlib.pyplot as plt


def edge_sizes(n):
    return int((n * (n - 1) / 2) / 4)

def test():
    vertex_sizes = [10, 25, 50, 75, 100, 200, 300, 400, 500, 750, 1000, 1500, 2000, 3000, 5000]
    sizes = [(vertex_size, edge_sizes(vertex_size)) for vertex_size in vertex_sizes]

    times = []


    for V, E in sizes:
        graph = generate_uniform_random_graph(V, E)
        print(f'Ordering graph of size {V} with {E} edges...')
        start_time = time.perf_counter()
        order, meta = smallest_last_vertex_ordering(graph)
        end_time = time.perf_counter()
        run_time = end_time - start_time

        print(f'Graph ordered in {(run_time):.6f} seconds.')

        times.append(run_time)

        folder_path = "generation_tests" + "/" + "smallest_last_ordering"

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
    ax.set_ylabel('Ordering Time (s)')
    ax.set_title('Ordering Time vs. Graph Size')


    fig.savefig(folder_path + "/times.png")

    with open(folder_path + "/times.txt", "w") as f:
        f.write('Graph Size\Ordering Time (s)\n')
        for i in range(len(sizes)):
            f.write(f'{sizes[i][0]}\t{times[i]}\n')

test()
