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

        # starting on second element we compare first-next vertices to determine
        # whether a non-zero edge exists from first to next
        while path_len > 1:

            next_vertex = path[path_ind]
            curr_vertex = path[path_ind-1]

            # check boundaries of proper vertices
            if next_vertex < 0 or next_vertex >= self.v_count or curr_vertex < 0 or curr_vertex >= self.v_count:
                return False

            # if no edge exists between first and next vertex
            if self.adj_matrix[curr_vertex][next_vertex] == 0:
                return False

            path_ind += 1
            path_len -= 1

        # if path successfully completed
        return True

    def dfs(self, v_start, v_end=None) -> []:
        """
        parameters:
            v_start(int): vertex to start the depth first search on
            v_end(int) OPTIONAL: optional vertex to end the search on

        returns:
            a list containing vertices visited and in the order they were visited

        functionality:
            Performs a depth first search on the graph and returns the connected component
            built from this search, with order being visit-sequence first to last
        """

        to_visit_stack = []
        visited_stack = []

        self.push(v_start, to_visit_stack)
        to_visit_stack_len = 1

        while to_visit_stack_len > 0:
            curr_vertex = to_visit_stack.pop()
            to_visit_stack_len -= 1
            # only process non-visited vertices
            if curr_vertex not in visited_stack:
                self.push(curr_vertex, visited_stack)

                if curr_vertex == v_end:
                    return visited_stack

                curr_vertex_neighbors = []
                col_ind = 0
                # find all vertices that curr_vertex is connected to
                while col_ind < self.v_count:
                    # process edge existence for each vertex
                    if self.adj_matrix[curr_vertex][col_ind] > 0:
                        self.push(col_ind, curr_vertex_neighbors)

                    col_ind += 1
                # now add all of these to the stack, sort them in descending order
                # descending order allows for correct processing of to_visit vertices
                # since the lowest values will be pushed last while the higher values
                # will be pushed first
                curr_vertex_neighbors = sorted(curr_vertex_neighbors, reverse=True)
                for neighbor in curr_vertex_neighbors:
                    self.push(neighbor, to_visit_stack)
                    to_visit_stack_len += 1

        return visited_stack

    def push(self, element, array):
        """
        Mainly to allow for more direct meaning when dealing with stack/queue
        """
        array.append(element)

    def enqueue(self, element, array):
        """
        Mainly to allow for more direct meaning when dealing with stack/queue
        """
        array.append(element)

    def dequeue(self, array):
        """
        Mainly to allow for more direct meaning when dealing with stack/queue
        """
        return array.pop(0)

    def bfs(self, v_start, v_end=None) -> []:
        """
        parameters:
            v_start(int): vertex to start the depth first search on
            v_end(int) OPTIONAL: optional vertex to end the search on

        returns:
            a list containing vertices visited and in the order they were visited

        functionality:
            Performs a breadth first search on the graph and returns the connected component
            built from this search, with order being visit-sequence first-to-last
        """
        to_visit_queue = []
        visited_stack = []

        self.enqueue(v_start, to_visit_queue)
        to_visit_queue_len = 1

        while to_visit_queue_len > 0:
            curr_vertex = self.dequeue(to_visit_queue)
            to_visit_queue_len -= 1

            # only process non-visited vertices
            if curr_vertex not in visited_stack:
                self.push(curr_vertex, visited_stack)

                if curr_vertex == v_end:
                    return visited_stack

                curr_vertex_neighbors = []
                col_ind = 0
                # find all vertices that curr_vertex is connected to
                while col_ind < self.v_count:
                    # process edge existence for each vertex
                    if self.adj_matrix[curr_vertex][col_ind] > 0:
                        self.enqueue(col_ind, curr_vertex_neighbors)

                    col_ind += 1
                # now add all of these to the stack, sort them in ascending order
                # ascending order is good as dequeue will process elements in the
                # order they were placed inside the to_visit_queue
                curr_vertex_neighbors = sorted(curr_vertex_neighbors)
                for neighbor in curr_vertex_neighbors:
                    self.enqueue(neighbor, to_visit_queue)
                    to_visit_queue_len += 1

        return visited_stack


    def has_cycle(self):
        """
        parameters:
            none

        returns:
            none

        functionality:
            This exploits the fact that whenever a vertex is a child of itself, a cycle exists. Using BFS,
            a dictionary keeps track of each nodes children, and then whenever a vertex is revisited, it checks
            to see if it is a child of itself.

            This is done for all unique connected components in the graph.
        """
        accounted_for = {}
        children = {}

        # DFS counter, only call DFS on NEW vertices
        for vertex in range(self.v_count):

            if vertex not in accounted_for:

                to_visit_queue = []
                visited_stack = []

                self.enqueue(vertex, to_visit_queue)
                to_visit_queue_len = 1

                root = vertex

                while to_visit_queue_len > 0:
                    curr_vertex = self.dequeue(to_visit_queue)

                    if root not in children:
                        children[root] = []
                    to_visit_queue_len -= 1

                    # only process non-visited vertices
                    if curr_vertex not in visited_stack:
                        self.push(curr_vertex, visited_stack)

                        curr_vertex_neighbors = []
                        col_ind = 0
                        # find all vertices that curr_vertex is connected to
                        while col_ind < self.v_count:
                            # process edge existence for each vertex
                            if self.adj_matrix[curr_vertex][col_ind] > 0:
                                self.enqueue(col_ind, curr_vertex_neighbors)

                            col_ind += 1
                        # now add all of these to the stack, sort them in ascending order
                        # ascending order is good as dequeue will process elements in the
                        # order they were placed inside the to_visit_queue
                        curr_vertex_neighbors = sorted(curr_vertex_neighbors)
                        for neighbor in curr_vertex_neighbors:
                            if neighbor not in children[root]:
                                children[root].append(neighbor)

                            self.enqueue(neighbor, to_visit_queue)
                            to_visit_queue_len += 1

                    # check to see if we've landed on a vertex that is a child of the parent
                    if curr_vertex in visited_stack and curr_vertex in children:
                        # if a vertex is a child of itself, then a cycle exists
                        if curr_vertex in children[curr_vertex]:
                            return True

        return False


    def dijkstra(self, src: int) -> []:
        """
        parameters:
            src(int): the starting vertex to check paths from

        returns:
            list containing distances from src to respective vertices

            each vertex is the same value as its index in the list

            ex: if src = vertex 3, and distance from src to vertex 0 = 2 then list[0] = 2, list[3] = 0

        functionality:

        """

        children = {}

        distances = {}

        to_visit_queue = []
        visited_stack = []

        self.enqueue(src, to_visit_queue)
        to_visit_queue_len = 1

        while to_visit_queue_len > 0:
            curr_vertex = self.dequeue(to_visit_queue)

            if src not in children:
                children[src] = []

            to_visit_queue_len -= 1

            # only process non-visited vertices
            if curr_vertex not in visited_stack:
                self.push(curr_vertex, visited_stack)

                curr_vertex_neighbors = []
                col_ind = 0
                # find all vertices that curr_vertex is connected to
                while col_ind < self.v_count:
                    # process edge existence for each vertex
                    if self.adj_matrix[curr_vertex][col_ind] > 0:
                        self.enqueue(col_ind, curr_vertex_neighbors)

                    col_ind += 1
                # now add all of these to the stack, sort them in ascending order
                # ascending order is good as dequeue will process elements in the
                # order they were placed inside the to_visit_queue
                curr_vertex_neighbors = sorted(curr_vertex_neighbors)
                for neighbor in curr_vertex_neighbors:
                    if neighbor not in children[src]:
                        children[src].append(neighbor)

                    # if a path from src to neighbor exists, and a path from neighbor to some other vertex exists,
                    # then a path from src to that other vertex exists, and we can do
                    # distance from src to other vertex = distance from src to neighbor + distance from neighbor to other vertex
                    if curr_vertex == src:
                        distances[(src, neighbor)] = self.adj_matrix[src][neighbor]

                    if curr_vertex != src and (curr_vertex, neighbor) not in distances:
                        distances[(curr_vertex, neighbor)] = self.adj_matrix[curr_vertex][neighbor]

                    if (src, neighbor) not in distances:
                        distances[(src, neighbor)] = distances[(src, curr_vertex)] + distances[(curr_vertex, neighbor)]

                    self.enqueue(neighbor, to_visit_queue)
                    to_visit_queue_len += 1

        calculated_distances = [None]*self.v_count

        path_ind = 0
        while path_ind < self.v_count:
            if path_ind == src:
                calculated_distances[path_ind] = 0

            elif (src, path_ind) not in distances:
                calculated_distances[path_ind] = float('inf')
            else:
                calculated_distances[path_ind] = distances[(src, path_ind)]
            path_ind += 1

        print(calculated_distances)
        print(self)




if __name__ == '__main__':

    # print("\nPDF - method add_vertex() / add_edge example 1")
    # print("----------------------------------------------")
    # g = DirectedGraph()
    # print(g)
    # for _ in range(5):
    #     g.add_vertex()
    # print(g)
    #
    # edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
    #          (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    # for src, dst, weight in edges:
    #     g.add_edge(src, dst, weight)
    # print(g)
    #
    #
    # print("\nPDF - method get_edges() example 1")
    # print("----------------------------------")
    # g = DirectedGraph()
    # print(g.get_edges(), g.get_vertices(), sep='\n')
    # edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
    #          (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    # g = DirectedGraph(edges)
    # print(g.get_edges(), g.get_vertices(), sep='\n')
    #
    #
    # print("\nPDF - method is_valid_path() example 1")
    # print("--------------------------------------")
    # edges = [(0, 4, 2), (1, 0, 10), (1, 2, 10), (2, 6, 6),
    #          (2, 9, 7), (3, 2, 6), (3, 10, 4), (4, 7, 4),
    #          (5, 1, 4), (5, 9, 5), (6, 3, 1), (7, 8, 1),
    #          (8, 5, 7), (9, 0, 2), (10, 9, 3)]
    # g = DirectedGraph(edges)
    # test_cases = [[0, 4, 7, 8, 5, 1, 2, 9, 10], [1, 3, 2, 1], [0, 4], [4, 0], [], [2]]
    # for path in test_cases:
    #     print(path, g.is_valid_path(path))
    #
    #
    # print("\nPDF - method dfs() and bfs() example 1")
    # print("--------------------------------------")
    # edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
    #          (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    # g = DirectedGraph(edges)
    # for start in range(5):
    #     print(f'{start} DFS:{g.dfs(start)} BFS:{g.bfs(start)}')
    #
    #
    # print("\nPDF - method has_cycle() example 1")
    # print("----------------------------------")
    # edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
    #          (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    # g = DirectedGraph(edges)
    #
    # edges_to_remove = [(3, 1), (4, 0), (3, 2)]
    # for src, dst in edges_to_remove:
    #     g.remove_edge(src, dst)
    #     print(g.get_edges(), g.has_cycle(), sep='\n')
    #
    # edges_to_add = [(4, 3), (2, 3), (1, 3), (4, 0)]
    # for src, dst in edges_to_add:
    #     g.add_edge(src, dst)
    #     print(g.get_edges(), g.has_cycle(), sep='\n')
    # print('\n', g)
    #
    #
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
