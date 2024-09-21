from __future__ import annotations

from typing import Iterable, Iterator, Optional, TYPE_CHECKING

import numpy as np  # type: ignore
from tcod.console import Console

from entity import Actor
import tile_types

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity


class GameMap:
    """
    Class to represent the game map

    Attributes:
        engine (Engine): The game engine.
        width (int): The width of the game map.
        height (int): The height of the game map.
        entities (set[Entity]): The entities on the game map.
        tiles (np.ndarray): The tiles of the game map.
        visible (np.ndarray): The visible tiles of the game map.
        explored (np.ndarray): The explored tiles of the game map.
    """

    def __init__(self, engine: Engine, width: int, height: int,
                 entities: Iterable[Entity] = ()):
        """
        Initialize the game map

        Args:
            engine (Engine): The game engine.
            width (int): The width of the game map.
            height (int): The height of the game map.
            entities (Iterable[Entity], optional): The entities on the game map.
        """
        self.engine = engine
        self.width, self.height = width, height
        self.entities = set(entities)
        self.tiles = np.full((width, height),
                             fill_value=tile_types.wall,
                             order="F")

        self.visible = np.full((width, height),
                               fill_value=False, order="F")
        self.explored = np.full((width, height),
                                fill_value=False, order="F")

    @property
    def actors(self) -> Iterator[Actor]:
        """
        Get the actors on the game map.

        Returns:
            Iterator[Actor]: The actors on the game map.
        """
        yield from (
            entity
            for entity in self.entities
            if isinstance(entity, Actor) and entity.is_alive
        )

    def get_blocking_entity_at_location(
            self,
            location_x: int,
            location_y: int,
    ) -> Optional[Entity]:
        """
        Get the blocking entity at a location.

        Args:
            location_x (int): The x-coordinate of the location.
            location_y (int): The y-coordinate of the location.

        Returns:
            Optional[Entity]: The blocking entity at the location.
        """
        for entity in self.entities:
            if (entity.blocks_movement
                    and entity.x == location_x
                    and entity.y == location_y):
                return entity

        return None

    def get_actor_at_location(self, x: int, y: int) -> Optional[Actor]:
        """
        Get the actor at a location.

        Args:
            x (int): The x-coordinate of the location.
            y (int): The y-coordinate of the location.

        Returns:
            Optional[Actor]: The actor at the location.
        """
        for actor in self.actors:
            if actor.x == x and actor.y == y:
                return actor

        return None

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
        Renders the game

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

        entities_sorted_for_rendering = sorted(
            self.entities, key=lambda x: x.render_order.value
        )

        # Draw all entities in the game map
        for entity in entities_sorted_for_rendering:
            if self.visible[entity.x, entity.y]:
                console.print(
                    x=entity.x, y=entity.y, string=entity.char, fg=entity.color
                )
