# Course: 
# Author: 
# Assignment: 
# Description:


class UndirectedGraph:
    """
    Class to implement undirected graph
    - duplicate edges not allowed
    - loops not allowed
    - no edge weights
    - vertex names are strings
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.adj_list = dict()

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            for u, v in start_edges:
                self.add_edge(u, v)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = [f'{v}: {self.adj_list[v]}' for v in self.adj_list]
        out = '\n  '.join(out)
        if len(out) < 70:
            out = out.replace('\n  ', ', ')
            return f'GRAPH: {{{out}}}'
        return f'GRAPH: {{\n  {out}}}'

    # ------------------------------------------------------------------ #

    def add_vertex(self, v: str) -> None:
        """
        parameters:
            v(str): vertex to be added to the graph

        returns:
            none

        functionality:
            adds specified vertex to graph if not existing there already
        """
        if v not in self.adj_list:
            self.adj_list[v] = []


    def add_edge(self, u: str, v: str) -> None:
        """
        parameters:
            u(str): vertex 1
            v(str): vertex 2

        returns:
            none

        functionality:
            ensures that by the end of execution, both vertices exist, and are connected by an edge unless
            vertices are the same
        """
        if u == v:
            return

        if u not in self.adj_list:
            self.add_vertex(u)

        if v not in self.adj_list:
            self.add_vertex(v)

        # add u to adjacent neighbors of v
        if u not in self.adj_list[v]:
            self.adj_list[v].append(u)

        # add v to adjacent neighbors of u
        if v not in self.adj_list[u]:
            self.adj_list[u].append(v)


    def remove_edge(self, v: str, u: str) -> None:
        """
        parameters:
            v(str): vertex 1
            u(str): vertex 2

        returns:
            none

        functionality:
            removes connection (edge) between specified vertices if edge exists
        """

        if v in self.adj_list and u in self.adj_list:
            if u in self.adj_list[v]:
                # if it exists in one, it exists in the other
                self.adj_list[v].remove(u)
                self.adj_list[u].remove(v)

    def remove_vertex(self, v: str) -> None:
        """
        parameters:
            v(str): vertex to remove

        returns:
            none

        functionality:
            removes vertex and all edges connected to it from the graph
        """

        if v in self.adj_list:
            neighbors = self.adj_list[v]

        else:
            return

        for neighbor in neighbors:
            # remove v from each of v's neighbor's neighbor-list
            self.adj_list[neighbor].remove(v)

    def get_vertices(self) -> []:
        """
        parameters:
            none

        returns:
            list of all vertices within the graph

        functionality:
            gathers all vertices from graph in no particular order
        """

        return list(self.adj_list.keys())

    def get_edges(self) -> []:
        """
        parameters:
            none

        returns:
            list of all edges in the graph

        functionality:
            returns a list of all edges in the graph in no particular order
        """
        edges = []

        added = {}

        for vertex in self.adj_list:

            for neighbor in self.adj_list[vertex]:
                # make sure we don't include duplicate edges since (A, C) = (C, A) in an undirected graph
                if (vertex, neighbor) not in added and (neighbor, vertex) not in added:
                    edges.append((vertex, neighbor))
                    added[(vertex, neighbor)] = True

        return edges
        

    def is_valid_path(self, path: []) -> bool:
        """
        parameters:
            path(python list): a sequence of vertices

        returns:
            boolean value describing whether or not sequence given is a path

        functionality:
            Determines whether specified sequence is a path in the graph

            An empty path is valid
        """
        path_size = len(path)

        if path_size == 0:
            return True

        is_path = True
        path_ind = 0
        while is_path and path_ind < path_size:
            curr_vertex = path[path_ind]
            # if vertex not in graph, not a possible path!
            if curr_vertex not in self.adj_list:
                return False
            if path_ind + 1 < path_size:
                next_vertex = path[path_ind+1]
            # at this point if we are on the last vertex then we have found a path here from vertex 1
            else:
                return True
            curr_vertex_neighbors = self.adj_list[curr_vertex]
            # check to see if the next vertex in the path is a neighbor of the current one, return once
            # this is not the case, else keep checking
            if next_vertex not in curr_vertex_neighbors:
                return False

            path_ind += 1


    def dfs(self, v_start, v_end=None) -> []:
        """
        parameters:
            v_start(str): starting vertex
            v_end(str): optional ending vertex
            return_cyclic(bool): parameter given if we want the cyclic nature of the graph instead
                of a list of travelled-to vertices

        returns:
            list containing all visited vertices from the depth-first-search

        functionality:
            performs a DFS on the graph starting at the specified index and returns a list
            of all visited vertices
        """

        to_visit_stack = []
        visited_stack = []

        if v_start not in self.adj_list:
            return visited_stack

        to_visit_stack.append(v_start)
        to_visit_stack_len = 1

        # while we still need to visit vertices continue the traversal
        while to_visit_stack_len > 0:
            curr_vertex = to_visit_stack.pop()
            to_visit_stack_len -= 1
            # only process non-visited vertices
            if curr_vertex not in visited_stack:
                visited_stack.append(curr_vertex)
                # if an end is specified, this is where it comes to play
                if curr_vertex == v_end:
                    return visited_stack
                # sort in reverse order so that the stack has the lowest values on top
                curr_vertex_neighbors = sorted(self.adj_list[curr_vertex], reverse=True)
                # descends from highest to lowest, appending lowest values top top of stack
                for neighbor in curr_vertex_neighbors:
                    to_visit_stack.append(neighbor)
                    to_visit_stack_len += 1

        return visited_stack

    def bfs(self, v_start, v_end=None) -> []:
        """
        parameters:
            v_start(str): starting vertex of BFS
            v_end(str) OPTIONAL: ending vertex of BFS

        returns:
            list of all vertices visited

        functionality:
            returns in the order visited all vertices travelled to from start to end if end is reached
        """
        to_visit_queue = []
        visited_stack = []

        if v_start not in self.adj_list:
            return visited_stack

        to_visit_queue.append(v_start)
        to_visit_queue_len = 1

        while to_visit_queue_len > 0:
            # dequeue
            curr_vertex = to_visit_queue.pop(0)
            to_visit_queue_len -= 1

            if curr_vertex not in visited_stack:
                visited_stack.append(curr_vertex)
                # if an end is specified, this is where it comes to play
                if curr_vertex == v_end:
                    return visited_stack
                # sort in regular ascending order so that lower values are dequeued first
                curr_vertex_neighbors = sorted(self.adj_list[curr_vertex])
                # descends from highest to lowest, appending lowest values top top of stack
                for neighbor in curr_vertex_neighbors:
                    to_visit_queue.append(neighbor)
                    to_visit_queue_len += 1

        return visited_stack

    def count_connected_components(self)->int:
        """
        parameters:
            none

        returns:
            number of connected components in the graph

        functionality:
            finds and counts all connected components in the graph

            all vertices travelled to via a DFS/BFS produces a connected component, I use
            this property to count all unique DFS connected components
        """

        # the idea here is that with DFS, is returns a list of all visited vertices
        # therefore, it contains a connected component

        # so any accounted for vertex, or a vertex found from a DFS, will not need to be
        # checked to find a potential connected component
        component_count = 0
        accounted_for = {}
        for vertex in self.adj_list:
            # increment components each time an unaccounted for vertex is used as a DFS start
            if vertex not in accounted_for:
                component = self.dfs(vertex)
                component_count += 1

                for link in component:
                    accounted_for[link] = True

        return component_count

    def has_cycle(self)->bool:
        """
        parameters:
            none

        returns:
            boolean value indicating whether or not graph contains a cycle

        functionality:
            determines whether or not graph is acyclic

            for a cycle to exist in a graph, it must have at least as many edges as it does vertices
            if I keep track of unique edges within each connected component, I can determine whether
            or not this statement is True or False
        """
        accounted_for = {}

        # loop through each unique connected component (subgraph)
        for vertex in self.adj_list:
            # initialize edge count, to_visit and visited stack for each connected component
            edge_count = 0
            to_visit_stack = []
            visited_stack = []
            edges = {}

            to_visit_stack.append(vertex)
            to_visit_stack_len = 1

            # increment components each time an unaccounted for vertex is used as a DFS start
            if vertex not in accounted_for:

                # while we still need to visit vertices continue the traversal
                while to_visit_stack_len > 0:
                    curr_vertex = to_visit_stack.pop()
                    to_visit_stack_len -= 1
                    # only process non-visited vertices
                    if curr_vertex not in visited_stack:
                        visited_stack.append(curr_vertex)
                        # sort in reverse order so that the stack has the lowest values on top
                        curr_vertex_neighbors = sorted(self.adj_list[curr_vertex], reverse=True)
                        # descends from highest to lowest, appending lowest values top top of stack
                        for neighbor in curr_vertex_neighbors:
                            # account for unique edges
                            if (curr_vertex, neighbor) not in edges and (neighbor, curr_vertex) not in edges:
                                edge_count += 1
                                edges[(curr_vertex, neighbor)] = True
                            to_visit_stack.append(neighbor)
                            to_visit_stack_len += 1

                for link in visited_stack:
                    accounted_for[link] = True

            # this is the minimum size subgraph needed for a cycle to exist
            if (edge_count >= 3) and edge_count >= len(visited_stack):
                return True

        return False

if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = UndirectedGraph()
    print(g)

    for v in 'ABCDE':
        g.add_vertex(v)
    print(g)

    g.add_vertex('A')
    print(g)

    for u, v in ['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE', ('B', 'C')]:
        g.add_edge(u, v)
    print(g)


    print("\nPDF - method remove_edge() / remove_vertex example 1")
    print("----------------------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    g.remove_vertex('DOES NOT EXIST')
    g.remove_edge('A', 'B')
    g.remove_edge('X', 'B')
    print(g)
    g.remove_vertex('D')
    print(g)


    print("\nPDF - method get_vertices() / get_edges() example 1")
    print("---------------------------------------------------")
    g = UndirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE'])
    print(g.get_edges(), g.get_vertices(), sep='\n')


    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    test_cases = ['ABC', 'ADE', 'ECABDCBE', 'ACDECB', '', 'D', 'Z']
    for path in test_cases:
        print(list(path), g.is_valid_path(list(path)))


    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = 'ABCDEGH'
    for case in test_cases:
        print(f'{case} DFS:{g.dfs(case)} BFS:{g.bfs(case)}')
    print('-----')
    for i in range(1, len(test_cases)):
        v1, v2 = test_cases[i], test_cases[-1 - i]
        print(f'{v1}-{v2} DFS:{g.dfs(v1, v2)} BFS:{g.bfs(v1, v2)}')


    print("\nPDF - method count_connected_components() example 1")
    print("---------------------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print(g.count_connected_components(), end=' ')
    print()


    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG',
        'add FG', 'remove GE')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print('{:<10}'.format(case), g.has_cycle())
