from __future__ import annotations

from typing import TYPE_CHECKING

from tcod.console import Console
from tcod.map import compute_fov

from input_handlers import MainGameEventHandler
from message_log import MessageLog
from render_functions import render_bar, render_names_at_mouse_location

if TYPE_CHECKING:
    from entity import Actor
    from game_map import GameMap
    from input_handlers import EventHandler


class Engine:
    """
    Main game engine.

    Responsible for drawing the map and entities, and handling input.

    Attributes:
        event_handler (EventHandler): The event handler.
        message_log (MessageLog): The message log.
        mouse_location (Tuple[int, int]): The current mouse location.
        player (Actor): The player entity.
    """
    game_map: GameMap

    def __init__(self, player: Actor):
        """
        Initialize the engine.

        Args:
            player (Actor): The player entity.
        """
        self.event_handler: EventHandler = MainGameEventHandler(self)
        self.message_log = MessageLog()
        self.mouse_location = (0,0)
        self.player = player

    def handle_enemy_turns(self) -> None:
        """
        Handle enemy turns.

        Loops through all entities on the map and handles their turns.
        """
        for entity in set(self.game_map.actors) - {self.player}:
            if entity.ai:
                entity.ai.perform()

    def update_fov(self) -> None:
        """
        Update the FOV.
        """
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=6
        )
        # If a tile is visible it should be added to explored
        self.game_map.explored |= self.game_map.visible

    def render(self, console: Console) -> None:
        """
        Render the game.

        Only displays entities that are in the FOV

        Args:
            console (Console): The console to render to.

        Returns:
            None
        """
        self.game_map.render(console)

        self.message_log.render(console=console, x=21, y=44, width=40, height=5)

        render_bar(
            console=console,
            current_value=self.player.fighter.hp,
            maximum_value=self.player.fighter.max_hp,
            total_width=20
        )

        render_names_at_mouse_location(console=console, x=0, y=43, engine=self)
