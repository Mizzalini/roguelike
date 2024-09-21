from __future__ import annotations

from typing import List, Tuple, TYPE_CHECKING

import numpy as np  # type: ignore
import tcod

from actions import Action, MeleeAction, MovementAction, WaitAction
from components.base_component import BaseComponent

if TYPE_CHECKING:
    from entity import Actor


class BaseAI(Action, BaseComponent):
    """
    Base class for AI components.
    """
    entity: Actor

    def perform(self) -> None:
        # No implementation as the engine will handle the AI's actions
        raise NotImplementedError()

    def get_path_to(self, dest_x: int, dest_y: int) -> List[Tuple[int, int]]:
        """
        Compute and return a path to the target position.

        If there is no valid path then return an empty list.

        Args:
            dest_x: Destination x-coordinate
            dest_y: Destination y-coordinate

        Returns:
            List of coordinates representing the path
        """
        cost = np.array(self.entity.game_map.tiles["walkable"], dtype=np.int8)

        for entity in self.engine.game_map.entities:
            if entity.blocks_movement and cost[entity.x, entity.y]:
                # Add to the cost of a blocked position
                # A lower number means more enemies will crowd behind each
                # other in hallways. a higher number means enemies will take
                # longer paths in order to surround the player
                cost[entity.x, entity.y] += 10

        # Create a graph from the cost array and pass that graph to the new
        # pathfinder
        graph = tcod.path.SimpleGraph(cost=cost, cardinal=2, diagonal=3)
        pathfinder = tcod.path.Pathfinder(graph)

        pathfinder.add_root((self.entity.x, self.entity.y))

        # Compute the path to the destination and remove the starting point
        path: List[List[int]] = (
            pathfinder.path_to((dest_x, dest_y))[1:].tolist())

        return [(index[0], index[1]) for index in path]


class HostileEnemy(BaseAI):
    """
    AI for a hostile enemy.

    Attributes:
        path: List of coordinates representing the path to the target
    """
    def __init__(self, entity: Actor):
        """
        Initialize the AI component.

        Args:
            entity: Actor entity
        """
        super().__init__(entity)
        self.path: List[Tuple[int, int]] = []

    def perform(self) -> None:
        """
        Perform the hostile enemy's action.

        If the entity is not in the player's vision, simply wait.
        If the player is right next to the entity (`distance <= 1`), attack
        the player.
        If the player can see the entity, but the entity is too far away to
        attack, then move towards the player.
        """
        target = self.engine.player
        dx = target.x - self.entity.x
        dy = target.y - self.entity.y
        distance = max(abs(dx), abs(dy))  # Chebyshev distance

        if self.engine.game_map.visible[self.entity.x, self.entity.y]:
            if distance <= 1:
                return MeleeAction(self.entity, dx, dy).perform()
            self.path = self.get_path_to(target.x, target.y)

        if self.path:
            dest_x, dest_y = self.path.pop(0)
            return MovementAction(
                self.entity, dest_x - self.entity.x, dest_y - self.entity.y
            ).perform()

        return WaitAction(self.entity).perform()
