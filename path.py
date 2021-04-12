"""This file contains relevant construction of a path or set of paths given
a number of game runs with a fixed map.
"""

from __future__ import annotations
from typing import Any


class _Vertex:
    """A vertex in a graph.
    """
    pos: Tuple[int, int, int]
    neighbours: set[_Vertex]

    def __init__(self, pos: Tuple[int, ...],
                 neighbours: set[_Vertex]) -> None:
        """Initialize a new vertex with the given item and neighbours."""
        self.pos = pos
        self.neighbours = neighbours

    def check_connected(self, target_pos: Tuple[int, ...],
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
        self._vertices = {0, set()}

    def get_last_vertex(self) -> dict[int, _Vertex]:
        return self._vertices[-1]


class Path:
    """A path that records player's path movements in the form of a Graph
    data structure"""
    _graph: Graph
    _last_vertex: _graph.get_last_vertex()
    _map: Map

    def __init__(self, map: Map) -> None:
        """Initialize the default path with the given graph and map"""
        self._graph = Graph()
        self._map = map

    def update_path(self, movement: str) -> None
        next_vertex = _self._graph.get_
