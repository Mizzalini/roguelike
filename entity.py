from __future__ import annotations

import copy
from typing import Tuple, TypeVar, TYPE_CHECKING

if TYPE_CHECKING:
    from game_map import GameMap

T = TypeVar("T", bound="Entity")


class Entity:
    """
    A generic object to represent players, enemies, items, etc.

    Attributes:
        x: The x-coordinate of the entity.
        y: The y-coordinate of the entity.
        char: The character representing the entity.
        color: The color of the entity, represented as an RGB tuple.
        name: The name of the entity.
        blocks_movement: Whether the entity blocks movement.
    """

    def __init__(
            self,
            x: int = 0,
            y: int = 0,
            char: str = "?",
            color: Tuple[int, int, int] = (255, 255, 255),
            name: str = "<Unnamed>",
            blocks_movement: bool = False,
    ):
        """
        Initialize the entity.

        Args:
            x: The x-coordinate of the entity.
            y: The y-coordinate of the entity.
            char: The character representing the entity.
            color: The color of the entity, represented as an RGB tuple.
            name: The name of the entity.
            blocks_movement: Whether the entity blocks movement.
        """
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks_movement = blocks_movement

    def spawn(self: T, gamemap: GameMap, x: int, y: int) -> T:
        """
        Spawn a copy of this entity at a given location.

        Args:
            gamemap: The game map to spawn the entity on.
            x: The x-coordinate to spawn the entity at.
            y: The y-coordinate to spawn the entity at.

        Returns:
            Entity: The newly spawned entity.
        """
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        gamemap.entities.add(clone)

        return clone

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
