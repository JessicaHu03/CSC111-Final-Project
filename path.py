"""This file contains relevant construction of a path or set of paths given
a number of game runs with a fixed map.
"""

from __future__ import annotations
from typing import Any
import operator


class _Vertex:
    """A vertex in a graph.
    """
    pos: Tuple[int, int]
    neighbours: set[_Vertex]

    def __init__(self, pos: Tuple[int, int],
                 neighbours: set[_Vertex]) -> None:
        """Initialize a new vertex with the given item and neighbours."""
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
        print(self.item)

        for u in self.neighbours:
            if u not in visited:
                u.print_all_connected(visited)


class Graph:
    """A graph.
    """
    _vertices: dict[int, _Vertex]

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

        self._vertices[self.length()] = new_vertex

    def get_last_vertex(self) -> _Vertex:
        if len(self._vertices) != 0:
            return list(self._vertices.values())[-1]
        else:
            return (0, 0)


class Path:
    """A path that records player's path movements utilizing the Graph
    data structure"""
    _graph: Graph
    # _game_map: Game_Map

    # def __init__(self, game_map: Game_Map) -> None:
    def __init__(self) -> None:
        """Initialize the default path with the given graph and map"""
        self._graph = Graph()
        # self._game_map = game_map

    def current_pos(self) -> Tuple[int, int]:
        return self._graph.get_last_vertex().pos

    def next_pos(self, movement: str, step: int) -> Tuple[int, int]:
        """Returns the next position coordinate with the given movement and
        step size.

        Parameters
        ----------
        movement : str
            Indicates the desired movement, available from (left, right, up,
            down).
        step : int
            Step size for each individual movement.

        Returns
        -------
        Tuple[int, int]
            Coordinate of the next position

        """
        next_pos = self.current_pos()
        coord_change = {'left': (-step, 0),
                        'right': (step, 0),
                        'up': (0, step),
                        'down': (0, -step)}
        if movement in coord_change:
            next_pos = tuple(map(operator.add,
                                 self.current_pos,
                                 coord_change[movement]))
        else:
            raise ValueError

        return next_pos

    def update_path(self, movement: str) -> None:
        try:
            self._graph.add_vertex(self.next_pos(movement))
        except ValueError:
            pass
