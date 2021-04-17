"""
This file contains the necessary class and methods for a player object
"""
import pandas as pd


class Player:
    """Player class, incorporates all current state of a player object.

    Attributes
    ----------
    user_id : string
        Represents the user id of the player.
        This can be used to identify different players on the interface.
    backpack : dict
        Keep track of current number of treasure and fragments the player has found.
    _vision_field : int
        This is the viewing distance (bright regions) of a player.
        Represented by an integer indicating the radius of vision
    """
    player_id: str
    backpack: dict
    games_played: int
    treasure_count: int
    _vision_field: int

    def __init__(self, player_id: str) -> None:
        """Initialize a new player with the given initial position and vision
        field radius.
        """
        self.player_id = player_id
        self.backpack = {'treasures': 0, 'fragments': 0}
        self.games_played = 0
        self.treasure_count = 0
        self._vision_field = 20

    def reset(self) -> None:
        self.backpack['treasures'] = 0
        self.backpack['fragments'] = 0

    def get_vision_radius(self) -> int:
        return self._vision_field

    def set_vision_radius(self, radius: int) -> None:
        """Updates the vision field radius (this is for testing purposes or for
        certain additional feature)"""
        self._vision_field = radius

    def update_backpack(self, object_type: str, change: int) -> None:
        """Updates the current backpack of the indicated type(keys, fragments...)
        with the given value of change"""
        self.backpack[object_type] += change

    def update_data(self, difficulty: int) -> None:
        """Updates player data saved in player_stat.csv"""
        self.games_played += 1
        self.treasure_count += difficulty

        df = pd.read_csv('player_stat.csv', index_col='player_id')
        try:
            df_player = df.loc[self.player_id]
        except KeyError:
            df.loc[self.player_id] = [self.games_played, self._vision_field, self.treasure_count]
        else:
            df_player.loc['games_played'] = self.games_played
            df_player.loc['treasure_count'] = self.treasure_count
            df.loc[self.player_id] = df_player

        df.to_csv('player_stat.csv')
