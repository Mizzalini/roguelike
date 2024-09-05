from typing import Iterable, Any

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov

from entity import Entity
from game_map import GameMap
from input_handlers import EventHandler


class Engine:
    """
    Main game engine.

    Responsible for drawing the map and entities, and handling input.

    Attributes:
        event_handler (EventHandler): The event handler.
        game_map (GameMap): The game map.
        player (Entity): The player entity.
    """
    def __init__(self, event_handler: EventHandler,
                 game_map: GameMap, player: Entity):
        """
        Initialize the engine.

        Args:
            event_handler (EventHandler): The event handler.
            game_map (GameMap): The game map.
            player (Entity): The player entity.
        """
        self.event_handler = event_handler
        self.game_map = game_map
        self.player = player
        self.update_fov()

    def handle_enemy_turns(self) -> None:
        """
        Handle enemy turns.

        Loops through all entities on the map and handles their turns.
        """
        for entity in set(self.game_map.entities) - {self.player}:
            print(
                f'The {entity.name} wonders when it will get to take a real '
                f'turn.')

    def handle_events(self, events: Iterable[Any]) -> None:
        """
        Handle events.

        Args:
            events (Iterable): The events to handle.

        Returns:
            None

        Raises:
            SystemExit: If the player wants to exit the game.
        """
        for event in events:
            action = self.event_handler.dispatch(event)

            if action is None:
                continue

            action.perform(self, self.player)

            self.handle_enemy_turns()
            self.update_fov()

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

    def render(self, console: Console, context: Context) -> None:
        """
        Render the game.

        Only display entities that are in the FOV

        Args:
            console (Console): The console to render to.
            context (Context): The context to render to.

        Returns:
            None
        """
        self.game_map.render(console)

        context.present(console)
        console.clear()
