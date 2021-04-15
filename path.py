"""This file contains relevant construction of a path or set of paths given
a number of game runs with a fixed map.
"""

from __future__ import annotations
from typing import Tuple
import operator
from map import GameMap
from player import Player


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
    _vertices: dict[Tuple[int, int], _Vertex]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self._vertices = dict()
        self.add_vertex((0, 0))

    def length(self) -> int:
        """Returns the number of vertices"""
        return len(self._vertices)

    def add_vertex(self, pos: Tuple[int, int]) -> None:
        """Add a vertex with the given position to this graph.

        The new vertex is not adjacent to any other vertices.
        """
        new_vertex = _Vertex(pos, set())
        self._vertices[pos] = new_vertex

    def add_edge(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> None:
        """Add an edge between the two vertices with the given items in this graph.

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.

        Preconditions:
            - item1 != item2
        """
        if pos1 in self._vertices and pos2 in self._vertices:
            # Add the edge between the two vertices
            v1 = self._vertices[pos1]
            v2 = self._vertices[pos2]

            v1.neighbours.add(v2)
            v2.neighbours.add(v1)
        else:
            raise ValueError

    def get_vertex(self, pos: Tuple[int, int]) -> _Vertex:
        """Return the vertex at the input position"""
        return self._vertices[pos]

    def get_vertices(self) -> dict[Tuple[int, int], _Vertex]:
        """Return _vertices"""
        return self._vertices


class Path:
    """A path that records player's path movements utilizing the Graph
    data structure"""
    _graph: Graph
    _player: Player
    move_count: int
    _game_map: GameMap

    def __init__(self, game_map: GameMap,
                 graph: Graph, player: Player) -> None:
        """Initialize the default path with the given graph and map"""
        self.move_count = 0
        self._graph = graph
        self._player = player
        self._game_map = game_map

    def get_graph(self) -> Graph:
        """Return the Graph"""
        return self._graph

    def current_pos(self) -> Tuple[int, int]:
        """Return current position in the path"""
        return self._player.get_pos()

    def next_pos(self, movement: str, h_step: int, v_step) -> Tuple[int, int]:
        """Returns the next position coordinate with the given movement and
        step size.
        """
        coord_change = {'left': (-h_step, 0),
                        'right': (h_step, 0),
                        'up': (0, v_step),
                        'down': (0, -v_step)}
        if movement in coord_change:
            next_pos = tuple(map(operator.add,
                                 self.current_pos(),
                                 coord_change[movement]))
        else:
            next_pos = self.current_pos()
            print('Invalid Movement')

        return next_pos

    def update_path(self, new_pos: Tuple[int, int]) -> None:
        """Add a new position (Vertex) to the path (_graph)

        This only happens for possible movements, after which is checked
        in advance
        """
        self.move_count += 1
        if new_pos not in self._graph.get_vertices():
            self._graph.add_vertex(new_pos)

        self._graph.add_edge(self.current_pos(), new_pos)
