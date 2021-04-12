"""
This file contains the necessary class and methods for a player object
"""
import operator
from typing import Tuple


class Player:
    """Player class, incorporates all current state of a player object.

    Attributes
    ----------
    id : string
        Represents the user id of the player.
        This can be used to identify different players on the interface.
    _position : Tuple[int, int, int]
        Current position of a player on the map.
        Represented by a tuple of integers consisting of the (x, y)
        coordinates.
    _vision_field : int
        This is the viewing distance (bright regions) of a player.
        Represented by an integer indicating the radius of vision
    _score : dict[str, int]
        Dictionary mapping different scoring types (number of keys, fragments,
        or opened treasure chests) to the corresponding value.
    """
    id: str
    _position: Tuple[int, int]
    _score: dict[str, int]
    _vision_field: int

    def __init__(self, id: str,
                 initial_pos: Tuple[int, int],
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

    def get_pos(self) -> Tuple[int, int]:
        """Returns the current position of the player."""
        return self._position

    def update_pos(self, change: Tuple[int, int]) -> None:
        """Updates the position of the player with the given change in the
        coordinates"""
        new_pos = tuple(map(operator.add, self._position, change))

        # The to-integer operation here is for aligning with position type "Tuple[int, int]"
        self._position = (int(new_pos[0]), int(new_pos[1]))

    def get_score(self, score_type: str) -> int:
        """Returns the current score of the indicated type(keys, fragments...)
        """
        if score_type in self._score:
            return self._score[score_type]
        else:
            raise ValueError

    def update_score(self, score_type: str, change: int) -> None:
        """Updates the current score of the indicated type(keys, fragments...)
        with the given value of change"""
        if score_type in self._score:
            self._score[score_type] += change
        else:
            raise ValueError

    def set_vision_radius(self, radius: int) -> None:
        """Updates the vision field radius (this is for testing purposes or for
        certain additional feature)"""
        self._vision_field = radius
