from typing import Tuple


class Entity:
    """
    A generic object to represent players, enemies, items, etc.

    Attributes:
        x: The x-coordinate of the entity.
        y: The y-coordinate of the entity.
        char: The character representing the entity.
        color: The color of the entity, represented as an RGB tuple.
    """

    def __init__(self, x: int, y: int, char: str, color: Tuple[int, int, int]):
        """
        Initialize the entity.

        Args:
            x: The x-coordinate of the entity.
            y: The y-coordinate of the entity.
            char: The character representing the entity.
            color: The color of the entity, represented as an RGB tuple.
        """
        self.x = x
        self.y = y
        self.char = char
        self.color = color

    def move(self, dx: int, dy: int) -> None:
        """
        Move the entity by a given amount.

        Args:
            dx: The amount to move in the x-direction.
            dy: The amount to move in the y-direction.

        Returns:
            None

        Raises:
            None
        """
        self.x += dx
        self.y += dy
