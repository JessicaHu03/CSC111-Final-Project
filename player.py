"""
This file contains the necessary class and methods for a player object
"""
from typing import Tuple


class Player:
    """Player class, incorporates all current state of a player object.

    Attributes
    ----------
    user_id : string
        Represents the user id of the player.
        This can be used to identify different players on the interface.
    backpack : dict
        Keep track of current number of treasure and fragments the player has found.
    _position : Tuple[int, int, int]
        Current position of a player on the map.
        Represented by a tuple of integers consisting of the (x, y)
        coordinates.
    _vision_field : int
        This is the viewing distance (bright regions) of a player.
        Represented by an integer indicating the radius of vision
    """
    user_id: str
    backpack: dict
    initial_pos: Tuple[int, int]
    _position: Tuple[int, int]
    _vision_field: int

    def __init__(self, user_id: str,
                 initial_pos: Tuple[int, int],
                 vision_field: int) -> None:
        """Initialize a new player with the given initial position and vision
        field radius.
        """
        self.user_id = user_id
        self.initial_pos = initial_pos
        self._position = initial_pos
        self._vision_field = vision_field
        self.backpack = {'treasures': 0, 'fragments': 0}

    def reset(self, omit_treasures: bool) -> None:
        self._position = self.initial_pos
        if not omit_treasures:
            self.backpack['treasures'] = 0
        self.backpack['fragments'] = 0

    def get_pos(self) -> Tuple[int, int]:
        """Returns the current position of the player."""
        return self._position

    def update_pos(self, new_pos: Tuple[int, int]) -> None:
        """Updates the position of the player with the given change in the
        coordinates"""
        self._position = new_pos

    def update_backpack(self, object_type: str, change: int) -> None:
        """Updates the current backpack of the indicated type(keys, fragments...)
        with the given value of change"""
        self.backpack[object_type] += change

    def set_vision_radius(self, radius: int) -> None:
        """Updates the vision field radius (this is for testing purposes or for
        certain additional feature)"""
        self._vision_field = radius
