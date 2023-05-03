class Node:
    def __init__(self, value):
        self.vertex = value
        self.next = None

    def __iter__(self):
        curr = self
        while curr:
            yield curr
            curr = curr.next

class Graph:
    def __init__(self, num_verticies: int) -> None:
        self.V = num_verticies
        self.adj_list = [None] * self.V

    def vertices(self) -> list[int]:
        return list(range(self.V))

    def edges(self) -> list[int]:
        """
        Returns a list of all edges in the graph as tuples (u, v), where u and v are connected vertices.
        """
        edges = []

        # Iterate through all vertices in the graph
        for u in range(self.V):
            # Iterate through the adjacency list of vertex u
            temp = self.adj_list[u]
            while temp:
                v = temp.vertex

                # Since the graph is undirected, add each edge only once by checking if u < v
                if u < v:
                    edges.append((u, v))

                temp = temp.next

        return edges

    def add_edge(self, s, d):
        node = Node(d)
        node.next = self.adj_list[s]
        self.adj_list[s] = node

        node = Node(s)
        node.next = self.adj_list[d]
        self.adj_list[d] = node

    def print_graph(self):
        for i in range(self.V):
            print("Vertex " + str(i) + ":", end="")
            temp = self.adj_list[i]
            while temp:
                print(" -> {}".format(temp.vertex), end="")
                temp = temp.next
            print(" \n")

    def degree(self, vertex):
        """
        Returns the degree of the given vertex
        """
        degree = 0
        temp = self.adj_list[vertex]
        while temp:
            degree += 1
            temp = temp.next
        return degree


    def neighbors(self, vertex):
        """
        Returns a list of neighbors of the given vertex
        """
        neighbors = []
        temp = self.adj_list[vertex]
        while temp:
            neighbors.append(temp.vertex)
            temp = temp.next
        return neighbors

    def dfs(self, start, visited):
        """
        Depth-First Search algorithm starting from the given vertex.
        """
        visited[start] = True
        yield start

        for neighbor in self.neighbors(start):
            if not visited[neighbor]:
                yield from self.dfs(neighbor, visited)

    def connected_components(self):
        """
        Returns a list of connected components, where each component is a list of vertices.
        """
        visited = [False] * self.V
        components = []

        for vertex in range(self.V):
            if not visited[vertex]:
                component = list(self.dfs(vertex, visited))
                components.append(component)

        return components


def bron_kerbosch(graph: Graph, r=None, p=None, x=None):
    if r is None:
        r = set()
    if p is None:
        p = set(range(graph.V))
    if x is None:
        x = set()

    if not p and not x:
        return [r]

    cliques = []
    for v in list(p):
        neighbors = set(neighbor.vertex for neighbor in graph.adj_list[v])
        new_r = r | {v}
        new_p = p & neighbors
        new_x = x & neighbors

        cliques += bron_kerbosch(graph, new_r, new_p, new_x)

        p.remove(v)
        x.add(v)

    return cliques

def terminal_clique_size(graph: Graph):
    all_cliques = bron_kerbosch(graph)
    terminal_clique = max(all_cliques, key=len)
    return len(terminal_clique)
