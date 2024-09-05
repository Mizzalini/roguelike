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


class ActionWithDirection(Action):
    """
    An action that requires a direction.
    """
    def __init__(self, dx: int, dy: int):
        """
        Initialize the action with a direction.

        Args:
            dx: The x-direction of the action.
            dy: The y-direction of the action.
        """
        super().__init__()

        self.dx = dx
        self.dy = dy

    @override
    def perform(self, engine: Engine, entity: Entity) -> None:
        raise NotImplementedError()


class MeleeAction(ActionWithDirection):
    """
    An action to perform a melee attack.
    """
    @override
    def perform(self, engine: Engine, entity: Entity) -> None:
        """
        Perform the melee action.
        """
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy

        target = engine.game_map.get_blocking_entity_at_location(dest_x, dest_y)
        if not target:
            return  # No entity to attack.

        print(
            f"You kick the {target.name} in the shins, much to its annoyance!"
        )


class MovementAction(ActionWithDirection):
    """
    An action to move in a direction.

    Attributes:
        dx: The amount to move in the x-direction.
        dy: The amount to move in the y-direction.
    """
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
        if engine.game_map.get_blocking_entity_at_location(dest_x, dest_y):
            return  # Destination is blocked by an entity.

        entity.move(self.dx, self.dy)


class BumpAction(ActionWithDirection):
    """
    Decides whether the action should be a melee attack or movement.
    """
    @override
    def perform(self, engine: Engine, entity: Entity) -> None:
        """
        Determine whether to perform a melee attack or movement.
        """
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy

        if engine.game_map.get_blocking_entity_at_location(dest_x, dest_y):
            return MeleeAction(self.dx, self.dy).perform(engine, entity)
        else:
            return MovementAction(self.dx, self.dy).perform(engine, entity)
