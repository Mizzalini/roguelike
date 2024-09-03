from typing import Set, Iterable, Any

from tcod.context import Context
from tcod.console import Console

from actions import EscapeAction, MovementAction
from entity import Entity
from input_handlers import EventHandler


class Engine:
    """
    Main game engine.

    Responsible for drawing the map and entities, and handling input.

    Attributes:
        entities (Set[Entity]): The game entities.
        event_handler (EventHandler): The event handler.
        player (Entity): The player entity.
    """
    def __init__(self, entities: Set[Entity], event_handler: EventHandler, player: Entity):
        """
        Initialize the engine.

        Args:
            entities (Set[Entity]): The game entities.
            event_handler (EventHandler): The event handler.
            player (Entity): The player entity.
        """
        self.entities = entities
        self.event_handler = event_handler
        self.player = player

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

            if isinstance(action, MovementAction):
                self.player.move(dx=action.dx, dy=action.dy)

            elif isinstance(action, EscapeAction):
                raise SystemExit()

    def render(self, console: Console, context: Context) -> None:
        """
        Render the game.

        Args:
            console (Console): The console to render to.
            context (Context): The context to render to.

        Returns:
            None
        """
        for entity in self.entities:
            console.print(entity.x, entity.y, entity.char, fg=entity.color)

        context.present(console)
        console.clear()