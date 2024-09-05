import numpy as np  # type: ignore
from tcod.console import Console

import tile_types


class GameMap:
    """
    Class to represent the game map

    Attributes:
        width (int): The width of the game map
        height (int): The height of the game map
        tiles (np.ndarray): The tiles of the game map
        visible (np.ndarray): The visible tiles of the game map
        explored (np.ndarray): The explored tiles of the game map
    """
    def __init__(self, width: int, height: int):
        """
        Initialize the game map

        Args:
            width (int): The width of the game map
            height (int): The height of the game map
        """
        self.width, self.height = width, height
        self.tiles = np.full((width, height),
                             fill_value=tile_types.wall,
                             order="F")

        self.visible = np.full((width, height), fill_value=False, order="F")
        self.explored = np.full((width, height), fill_value=False, order="F")

    def in_bounds(self, x: int, y: int) -> bool:
        """
        Check if a set of coordinates is in bounds of the game map

        Args:
            x (int): The x coordinate
            y (int): The y coordinate

        Returns:
            bool: True if the coordinates are in bounds, False otherwise
        """
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console: Console) -> None:
        """
        Render the game map

        If a tile is in the 'visible' array, then draw it with the 'light'
        colours. If it isn't, but it's in the 'explored' array, then draw it
        with the 'dark' colours. Otherwise, the default is 'SHROUD'

        Args:
            console (Console): The console to render to
        """
        console.rgb[0: self.width, 0: self.height] = np.select(
            condlist=[self.visible, self.explored],
            choicelist=[self.tiles["light"], self.tiles["dark"]],
            default=tile_types.SHROUD
        )
