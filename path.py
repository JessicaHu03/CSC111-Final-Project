"""This file contains relevant construction of a path or set of paths given
a number of game runs with a fixed map.
"""

from __future__ import annotations
from typing import Tuple, List, Optional
import pandas as pd
import os


class _Vertex:
    """A vertex in a graph.
    """
    pos: Tuple[int, int]
    neighbours: set[_Vertex]

    def __init__(self, pos: Tuple[int, int],
                 neighbours: set[_Vertex]) -> None:
        """Initialize a new vertex with the given position and neighbours."""
        self.pos = pos
        self.neighbours = neighbours

    def check_connected(self, target_pos: Tuple[int, int],
                        visited: set[_Vertex]) -> bool:
        """Return whether this vertex is connected to a vertex corresponding to
        target_item, by a path that DOES NOT use any vertex in visited.

        Preconditions:
            - self not in visited
        """
        if self.pos == target_pos:
            return True
        else:
            visited.add(self)
            # (for loop version)
            for u in self.neighbours:
                if u not in visited:
                    if u.check_connected(target_pos, visited):
                        return True

            return False

    def print_all_connected(self, visited: set[_Vertex]) -> None:
        """
        TODO: This can be transformed into path visualization

        Preconditions:
            - self not in visited
        """
        visited.add(self)
        print(self.pos)

        for u in self.neighbours:
            if u not in visited:
                u.print_all_connected(visited)


class Graph:
    """A graph.
    """
    _vertices: dict[str, _Vertex]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self._vertices = dict()

    def length(self) -> int:
        """Returns the number of vertices"""
        return len(self._vertices)

    def add_vertex(self, pos: Tuple[int, int]) -> None:
        """Add a vertex with the given position to this graph.

        The new vertex is not adjacent to any other vertices.
        """
        new_vertex = _Vertex(pos, set())
        self._vertices[str(pos)] = new_vertex

    def add_edge(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> None:
        """Add an edge between the two vertices with the given items in this graph.

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.

        Preconditions:
            - item1 != item2
        """
        if str(pos1) in self._vertices and str(pos2) in self._vertices:
            # Add the edge between the two vertices
            v1 = self._vertices[str(pos1)]
            v2 = self._vertices[str(pos2)]

            v1.neighbours.add(v2)
            v2.neighbours.add(v1)
        else:
            raise ValueError

    def get_vertex(self, pos: Tuple[int, int]) -> _Vertex:
        """Return the vertex at the input position"""
        return self._vertices[str(pos)]

    def get_vertices(self) -> dict[str, _Vertex]:
        """Return _vertices"""
        return self._vertices


class Path:
    """A path that records player's path movements utilizing the Graph
    data structure"""
    id: int
    move_count: int
    initial_pos: Tuple[int, int]
    _map_id: int
    _graph: Graph
    _player_id: str
    _all_pos: List[Tuple[int, int]]

    def __init__(self, initial_pos: Tuple[int, int],
                 map_id: Optional[int] = 0,
                 player_id: Optional[str] = "Default") -> None:
        """Initialize the default path with the given graph and map"""
        self.initial_pos = initial_pos
        self.move_count = 0
        self._map_id = map_id
        self._player_id = player_id
        self._graph = Graph()
        self._all_pos = list()
        self.update_path(initial_pos)

    def get_graph(self) -> Graph:
        """Return the Graph"""
        return self._graph

    def all_pos(self) -> List[Tuple[int, int]]:
        """Return all the past positions of the player"""
        return self._all_pos

    def update_path(self, new_pos: Tuple[int, int]) -> None:
        """Add a new position (Vertex) to the path (_graph)

        This only happens for possible movements, after which is checked
        in advance
        """
        self.move_count += 1

        if new_pos not in self._graph.get_vertices():
            self._graph.add_vertex(new_pos)
            self._all_pos.append(new_pos)

        if len(self._graph.get_vertices()) > 1:
            self._graph.add_edge(self._all_pos[-2], new_pos)

    def write_path(self) -> None:
        """Saves relevant information for the current path to file"""
        # Returns number of existing paths from directory
        path_num = len([m for m in os.listdir('paths/')])
        self.id = path_num + 1

        # Retrieves specific object information, save to dataframe
        player_id = pd.DataFrame({'player_id': self._player_id}, index=[0])
        map_id = pd.DataFrame({'map_id': self._map_id}, index=[0])
        initial_pos = pd.DataFrame({'initial_pos': self.initial_pos})
        vertices = pd.DataFrame({'vertices': self._graph.get_vertices().keys()})
        neighbours = pd.DataFrame({'neighbours': [[n.pos for n in v.neighbours]
                                                  for v in self._graph.get_vertices().values()]})

        # Concatenate all information to a single dataframe. This may be bad practice, for that
        # the elements from one row aren't correlated, and there is a different number of observations
        # per variable. Using Pandas here is just for code cleanliness and computational simplicity.
        object_info = pd.concat([vertices, neighbours, initial_pos, player_id, map_id],
                                axis=1, ignore_index=False)

        # Sets new path name. This is given by 'path' + the path index.
        path_name = 'path{}.csv'.format(self.id)
        # Saves map file to directory
        object_info.to_csv(os.path.join(r'paths\\', path_name), index=False)

    def read_path(self, path_file: str) -> None:
        """Reads a path from file, retrieving all relevant information required
        to rebuild a path"""
        # Reading path file
        df = pd.read_csv(path_file, index_col=False)
        # Retrieve vertices and settings for path, indexing by column name
        player_id = df['player_id'][0]
        map_id = int(df['map_id'][0])
        initial_pos = df['initial_pos'][0]
        vertices = df['vertices'].tolist()
        neighbours = df['neighbours'].tolist()

        # Each value of the DataFrame is of type string, except for the player and map ids
        # Thus, by evaluating each returns the tuple objects.
        if vertices and neighbours:
            vertices = [eval(vertex) for vertex in vertices]
            neighbours = [eval(neighbour_set) for neighbour_set in neighbours]

        # Assign each neighbour set to their relevant vertex
        assert len(vertices) == len(neighbours)

        for i in range(len(vertices)):
            self._graph.add_vertex(vertices[i])

        for i in range(len(vertices)):
            for j in range(len(neighbours[i])):
                self._graph.add_edge(vertices[i], neighbours[i][j])

        self.initial_pos = initial_pos
        self._player_id = player_id
        self._map_id = map_id


