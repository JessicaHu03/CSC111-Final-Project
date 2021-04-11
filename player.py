"""
This file contains the necessary class and methods for a player object
"""
import operator
from typing import Any, Tuple


class Player:
    """Player class, incorporates all current state of a player object.

    Attributes
    ----------
    id : string
        Represents the user id of the player.
        This can be used to identify different players on the interface.
    _position : Tuple[int, int, int]
        Current position of a player on the map.
        Represented by a tuple of integers consisting of the (x, y, z)
        coordinates.
    _vision_field : int
        This is the viewing distance (bright regions) of a player.
        Represented by an integer indicating the radius of vision
    _score : dict[str, int]
        Dictionary mapping different scoring types (number of keys, fragments,
        or opened treasure chests) to the corresponding value.
    """
    id: str
    _position: Tuple[int, int, int]
    _score: dict[str, int]
    _vision_field: int

    def __init__(self, id: str,
                 initial_pos: Tuple[int, int, int],
                 vision_field: int) -> None:
        """Initialize a new player with the given initial position and vision
        field radius.
        """
        self.id = id
        self._position = initial_pos
        self._vision_field = vision_field
        self._score = {
                       'key': 0,
                       'frag': 0,
                       'treasure': 0
                       }

    def get_pos(self) -> Tuple[int, int, int]:
        """Returns the current position of the player."""
        return self._position

    def update_pos(self, change: Tuple[int, int, int]) -> None:
        """Updates the position of the player with the given change in the
        coordinates"""
        self._position = tuple(map(operator.add, self._position, change))

    def get_score(self, type: str) -> int:
        """Returns the current score of the indicated type(keys, fragments...)
        """
        if type in self._score:
            return self._score[type]
        else:
            raise ValueError

    def update_score(self, type: str, change: int) -> None:
        """Updates the current score of the indicated type(keys, fragments...)
        with the given value of change"""
        if type in self._score:
            self._score[type] += change
        else:
            raise ValueError
