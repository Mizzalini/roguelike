from __future__ import annotations

from typing import TYPE_CHECKING, override

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity


class Action:
    """
    An action that can be performed.
    """
    def perform(self, engine: Engine, entity: Entity) -> None:
        """
        Perform this action with the objects needed to determine its scope.

        Args:
            engine: The scope this action is being performed in.
            entity: The object performing the action.

        Returns:
            None
        """
        raise NotImplementedError()


class EscapeAction(Action):
    """
    An action to exit the game.
    """
    @override
    def perform(self, engine: Engine, entity: Entity) -> None:
        """
        Perform the escape action.
        """
        raise SystemExit()


class MovementAction(Action):
    """
    An action to move in a direction.

    Attributes:
        dx: The amount to move in the x-direction.
        dy: The amount to move in the y-direction.
    """
    def __init__(self, dx: int, dy: int):
        """
        Initialize the movement action.

        Args:
            dx: The amount to move in the x-direction.
            dy: The amount to move in the y-direction.
        """
        super().__init__()

        self.dx = dx
        self.dy = dy

    @override
    def perform(self, engine: Engine, entity: Entity) -> None:
        """
        Perform the movement action.
        """
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy

        if not engine.game_map.in_bounds(dest_x, dest_y):
            return  # Destination is out of bounds.
        if not engine.game_map.tiles["walkable"][dest_x, dest_y]:
            return  # Destination is blocked by a tile.

        entity.move(self.dx, self.dy)
