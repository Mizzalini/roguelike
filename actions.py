from __future__ import annotations

from typing import Optional, Tuple, TYPE_CHECKING, override

if TYPE_CHECKING:
    from engine import Engine
    from entity import Actor, Entity


class Action:
    """
    An action that can be performed.

    Attributes:
        entity: The entity performing the action.
    """
    def __init__(self, entity: Actor) -> None:
        """
        Initialize the action with the entity performing it.

        Args:
            entity: The entity performing the action.
        """
        super().__init__()
        self.entity = entity

    @property
    def engine(self) -> Engine:
        """
        Return the engine this action belongs to
        """
        return self.entity.game_map.engine

    def perform(self) -> None:
        """
        Perform this action with the objects needed to determine its scope.

        self.engine is the scope this action is being performed in.
        self.entity is the object performing the action.

        This method must be overridden by Action subclasses.
        """
        raise NotImplementedError()


class EscapeAction(Action):
    """
    An action to exit the game.
    """
    @override
    def perform(self) -> None:
        """
        Perform the escape action.
        """
        raise SystemExit()


class WaitAction(Action):
    """
    An action to wait for a turn.
    """
    @override
    def perform(self) -> None:
        """
        Perform the wait action.
        """
        pass


class ActionWithDirection(Action):
    """
    An action that requires a direction.
    """
    def __init__(self, entity: Actor, dx: int, dy: int):
        """
        Initialize the action with the entity performing it and the direction.

        Args:
            entity: The entity performing the action.
            dx: The amount to move in the x-direction.
            dy: The amount to move in the y-direction.
        """
        super().__init__(entity)
        self.dx = dx
        self.dy = dy

    @property
    def dest_xy(self) -> Tuple[int, int]:
        """
        Return the destination x, y coordinates.
        """
        return self.entity.x + self.dx, self.entity.y + self.dy

    @property
    def blocking_entity(self) -> Optional[Entity]:
        """
        Return the blocking entity at the destination.
        """
        return self.engine.game_map.get_blocking_entity_at_location(
            *self.dest_xy)

    @property
    def target_actor(self) -> Optional[Actor]:
        """
        Return the actor at the destination.
        """
        return self.engine.game_map.get_actor_at_location(*self.dest_xy)

    @override
    def perform(self) -> None:
        raise NotImplementedError()


class MeleeAction(ActionWithDirection):
    """
    An action to perform a melee attack.
    """
    @override
    def perform(self) -> None:
        """
        Perform the melee action.
        """
        target = self.target_actor
        if not target:
            return  # No entity to attack.

        damage = self.entity.fighter.power - target.fighter.defense

        attack_desc = f"{self.entity.name.capitalize()} attacks {target.name}"
        if damage > 0:
            target.fighter.hp -= damage
            print(f"{attack_desc} for {damage} hit points.")
        else:
            print(f"{attack_desc} but does no damage.")


class MovementAction(ActionWithDirection):
    """
    An action to move in a direction.

    Attributes:
        dx: The amount to move in the x-direction.
        dy: The amount to move in the y-direction.
    """
    @override
    def perform(self) -> None:
        """
        Perform the movement action.
        """
        dest_x, dest_y = self.dest_xy

        if not self.engine.game_map.in_bounds(dest_x, dest_y):
            return  # Destination is out of bounds.
        if not self.engine.game_map.tiles["walkable"][dest_x, dest_y]:
            return  # Destination is blocked by a tile.
        if self.engine.game_map.get_blocking_entity_at_location(dest_x, dest_y):
            return  # Destination is blocked by an entity.

        self.entity.move(self.dx, self.dy)


class BumpAction(ActionWithDirection):
    """
    Decides whether the action should be a melee attack or movement.
    """
    @override
    def perform(self) -> None:
        """
        Determine whether to perform a melee attack or movement.
        """
        if self.target_actor:
            return MeleeAction(self.entity, self.dx, self.dy).perform()
        else:
            return MovementAction(self.entity, self.dx, self.dy).perform()
