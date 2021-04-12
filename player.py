"""
This file contains the necessary class and methods for a player object
"""
import operator
from typing import Tuple


class Player:
    """Player class, incorporates all current state of a player object.

    Attributes
    ----------
    user_id : string
        Represents the user id of the player.
        This can be used to identify different players on the interface.
    score : int
        Keep track of current number of treasure the player has found.
    _position : Tuple[int, int, int]
        Current position of a player on the map.
        Represented by a tuple of integers consisting of the (x, y)
        coordinates.
    _vision_field : int
        This is the viewing distance (bright regions) of a player.
        Represented by an integer indicating the radius of vision
    """
    user_id: str
    score: int
    _position: Tuple[int, int]
    _vision_field: int

    def __init__(self, user_id: str,
                 initial_pos: Tuple[int, int],
                 vision_field: int) -> None:
        """Initialize a new player with the given initial position and vision
        field radius.
        """
        self.user_id = user_id
        self._position = initial_pos
        self._vision_field = vision_field
        self.score = 0

    def get_pos(self) -> Tuple[int, int]:
        """Returns the current position of the player."""
        return self._position

    def update_pos(self, new_pos: Tuple[int, int]) -> None:
        """Updates the position of the player with the given change in the
        coordinates"""
        self._position = new_pos

    def update_score(self, change: int) -> None:
        """Updates the current score of the indicated type(keys, fragments...)
        with the given value of change"""
        self.score += change

    def set_vision_radius(self, radius: int) -> None:
        """Updates the vision field radius (this is for testing purposes or for
        certain additional feature)"""
        self._vision_field = radius
