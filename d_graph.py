# Course: CS261 - Data Structures
# Author:
# Assignment:
# Description:

class DirectedGraph:
    """
    Class to implement directed weighted graph
    - duplicate edges not allowed
    - loops not allowed
    - only positive edge weights
    - vertex names are integers
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency matrix
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.v_count = 0
        self.adj_matrix = []

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            v_count = 0
            for u, v, _ in start_edges:
                v_count = max(v_count, u, v)
            for _ in range(v_count + 1):
                self.add_vertex()
            for u, v, weight in start_edges:
                self.add_edge(u, v, weight)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if self.v_count == 0:
            return 'EMPTY GRAPH\n'
        out = '   |'
        out += ' '.join(['{:2}'.format(i) for i in range(self.v_count)]) + '\n'
        out += '-' * (self.v_count * 3 + 3) + '\n'
        for i in range(self.v_count):
            row = self.adj_matrix[i]
            out += '{:2} |'.format(i)
            out += ' '.join(['{:2}'.format(w) for w in row]) + '\n'
        out = f"GRAPH ({self.v_count} vertices):\n{out}"
        return out

    # ------------------------------------------------------------------ #

    def add_vertex(self) -> int:
        """
        parameters:
            None

        returns:
            int

        functionality:
            Adds vertex to tree and returns new number of vertices
        """

        new_vertex = []

        # initialize new vertex with as many zeroes equal to current v_count
        for column in range(self.v_count):
            new_vertex.append(0)

        # append to matrix
        self.adj_matrix.append(new_vertex)

        # now account for newly added vertex and append one more column to each
        for vertex_row in self.adj_matrix:
            vertex_row.append(0)

        self.v_count += 1

        return self.v_count

    def add_edge(self, src: int, dst: int, weight=1) -> None:
        """
        parameters:
            src(int): source vertex
            dst(int): destination vertex
            weight(int): weight of each edge

        returns:
            none

        functionality:
            Adds edge from source to destination vertex with specified weight or 1

            This method adds a new edge to the graph, connecting two vertices with provided indices. If either
            (or both) vertex indices do not exist in the graph, or if the weight is not a positive integer,
            or if src and dst refer to the same vertex, the method does nothing. If an edge already
            exists in the graph, the method will update its weight.
        """

        if src == dst:
            return

        if src >= self.v_count or src < 0 or dst >= self.v_count or dst < 0:
            return

        if weight <= 0:
            return

        self.adj_matrix[src][dst] = weight


    def remove_edge(self, src: int, dst: int) -> None:
        """
        parameters:
            src(int): source vertex
            dst(int): destination vertex

        returns:
            none

        functionality:
            Removes specified edge if it exists
        """
        if src == dst:
            return

        if src >= self.v_count or src < 0 or dst >= self.v_count or dst < 0:
            return

        self.adj_matrix[src][dst] = 0


    def get_vertices(self) -> []:
        """
        parameters:
            none

        returns:
            list of vertices in no particular order

        functionality:
            returns a list of vertices in the graph
        """

        return [x for x in range(self.v_count)]


    def get_edges(self) -> []:
        """
        parameters:
            none

        returns:
            list of all edges in the graph

        functionality:
            returns a list of all edges in the graph
        """
        edges = []

        for row_vertex in range(self.v_count):
            for col_vertex in range(self.v_count):
                # if weight is more than 0
                if self.adj_matrix[row_vertex][col_vertex] > 0:
                    edges.append((row_vertex, col_vertex, self.adj_matrix[row_vertex][col_vertex]))

        return edges

    def is_valid_path(self, path: []) -> bool:
        """
        parameters:
            path(Python built-in list): specified path

        returns:
            boolean value describing whether or not the specified path exists in the graph

        functionality:
            uses the specified path to verify with the adj_matrix and returns True/False
            based on whether or not the algo successfully iterated through the path
        """

        path_len = len(path)
        path_ind = 1

        if path_len == 1:
            if path[0] >= self.v_count or path[0] < 0:
                return False

        while path_len > 1:
            next_vertex = path[path_ind]
            curr_vertex = path[path_ind-1]

            if next_vertex < 0 or next_vertex >= self.v_count or curr_vertex < 0 or curr_vertex >= self.v_count:
                return False

            if self.adj_matrix[curr_vertex][next_vertex] == 0:
                return False

            path_len -= 1

        return True

    def dfs(self, v_start, v_end=None) -> []:
        """
        parameters:


        returns:


        functionality:

        """
        pass

    def bfs(self, v_start, v_end=None) -> []:
        """
        parameters:


        returns:


        functionality:

        """
        pass

    def has_cycle(self):
        """
        parameters:


        returns:


        functionality:

        """
        pass

    def dijkstra(self, src: int) -> []:
        """
        parameters:


        returns:


        functionality:

        """
        pass


if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = DirectedGraph()
    print(g)
    for _ in range(5):
        g.add_vertex()
    print(g)

    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    for src, dst, weight in edges:
        g.add_edge(src, dst, weight)
    print(g)


    print("\nPDF - method get_edges() example 1")
    print("----------------------------------")
    g = DirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    print(g.get_edges(), g.get_vertices(), sep='\n')


    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    test_cases = [[0, 1, 4, 3], [1, 3, 2, 1], [0, 4], [4, 0], [], [2]]
    for path in test_cases:
        print(path, g.is_valid_path(path))


    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for start in range(5):
        print(f'{start} DFS:{g.dfs(start)} BFS:{g.bfs(start)}')


    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)

    edges_to_remove = [(3, 1), (4, 0), (3, 2)]
    for src, dst in edges_to_remove:
        g.remove_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')

    edges_to_add = [(4, 3), (2, 3), (1, 3), (4, 0)]
    for src, dst in edges_to_add:
        g.add_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')
    print('\n', g)


    print("\nPDF - dijkstra() example 1")
    print("--------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
    g.remove_edge(4, 3)
    print('\n', g)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
