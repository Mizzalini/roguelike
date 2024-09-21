from __future__ import annotations

import copy
from typing import Optional, Tuple, Type, TypeVar, TYPE_CHECKING

from render_order import RenderOrder

if TYPE_CHECKING:
    from components.ai import BaseAI
    from components.fighter import Fighter
    from game_map import GameMap

T = TypeVar("T", bound="Entity")


class Entity:
    """
    A generic object to represent players, enemies, items, etc.

    Attributes:
        game_map: The game map the entity is currently
        x: The x-coordinate of the entity.
        y: The y-coordinate of the entity.
        char: The character representing the entity.
        color: The color of the entity, represented as an RGB tuple.
        name: The name of the entity.
        blocks_movement: Whether the entity blocks movement.
    """

    game_map: GameMap

    def __init__(
            self,
            game_map: Optional[GameMap] = None,
            x: int = 0,
            y: int = 0,
            char: str = "?",
            color: Tuple[int, int, int] = (255, 255, 255),
            name: str = "<Unnamed>",
            blocks_movement: bool = False,
            render_order: RenderOrder = RenderOrder.CORPSE
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
        self.render_order = render_order
        if game_map:
            # If game_map isn't provided now then it will be set later.
            self.game_map = game_map
            game_map.entities.add(self)

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
        clone.game_map = gamemap
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

    def place(self, x: int, y: int, game_map: Optional[GameMap] = None) -> None:
        """
        Place the entity at a given location.

        Args:
            x: The x-coordinate to place the entity at.
            y: The y-coordinate to place the entity at.
            game_map: The game map to place the entity on.
        """
        self.x = x
        self.y = y
        if game_map:
            if hasattr(self, "game_map"):  # Possibly uninitialized.
                self.game_map.entities.remove(self)
            self.game_map = game_map
            game_map.entities.add(self)


class Actor(Entity):
    """
    An actor is an entity that can perform actions.

    Attributes:
        ai: The AI controlling the actor.
        fighter: The fighter component of the actor.
    """
    def __init__(
            self,
            *,
            x: int = 0,
            y: int = 0,
            char: str = "?",
            color: Tuple[int, int, int] = (255, 255, 255),
            name: str = "<Unnamed>",
            ai_cls: Type[BaseAI],
            fighter: Fighter,
    ):
        """
        Initialize the actor.

        Args:
            x: The x-coordinate of the actor.
            y: The y-coordinate of the actor.
            char: The character representing the actor.
            color: The color of the actor, represented as an RGB tuple.
            name: The name of the actor.
            ai_cls: The AI class to control the actor.
            fighter: The fighter component of the actor.
        """
        super().__init__(
            x=x,
            y=y,
            char=char,
            color=color,
            name=name,
            blocks_movement=True,
            render_order=RenderOrder.ACTOR
        )

        self.ai: Optional[BaseAI] = ai_cls(self)

        self.fighter = fighter
        self.fighter.entity = self

    @property
    def is_alive(self) -> bool:
        """
        Return whether the actor is alive.
        """
        return bool(self.fighter.hp > 0)
