from __future__ import annotations

from typing import Optional, TYPE_CHECKING, override

import tcod.event
from tcod import constants

from actions import Action, BumpAction, EscapeAction, WaitAction

if TYPE_CHECKING:
    from engine import Engine


# The keys for moving the player
MOVE_KEYS = {
    # Arrow keys
    tcod.event.KeySym.UP: (0, -1),
    tcod.event.KeySym.DOWN: (0, 1),
    tcod.event.KeySym.LEFT: (-1, 0),
    tcod.event.KeySym.RIGHT: (1, 0),
    # WASD keys
    tcod.event.KeySym.w: (0, -1),
    tcod.event.KeySym.s: (0, 1),
    tcod.event.KeySym.a: (-1, 0),
    tcod.event.KeySym.d: (1, 0),
}

# The keys for waiting
WAIT_KEYS = {
    tcod.event.KeySym.PERIOD,
    tcod.event.KeySym.KP_5,
    tcod.event.KeySym.CLEAR,
}

# The keys for message scrolling
CURSOR_Y_KEYS = {
    tcod.event.KeySym.UP: -1,
    tcod.event.KeySym.DOWN: 1,
    tcod.event.KeySym.PAGEUP: -10,
    tcod.event.KeySym.PAGEDOWN: 10,
}


class EventHandler(tcod.event.EventDispatch[Action]):
    """
    The event handler base class.

    Attributes:
        engine (Engine): The game engine.
    """
    def __init__(self, engine: Engine):
        """
        The constructor for the event handler.

        Args:
            engine (Engine): The game engine.
        """
        self.engine = engine

    def handle_events(self, context: tcod.context.Context) -> None:
        """
        Handles events.

        Iterates through events, and gives the event knowledge on the mouse
        position. That event is then dispatched, to be handled like normal.

        Args:
            context: The context of the game.
        """
        for event in tcod.event.wait():
            context.convert_event(event)
            self.dispatch(event)

    @override
    def ev_mousemotion(self, event: tcod.event.MouseMotion) -> None:
        if self.engine.game_map.in_bounds(event.tile.x, event.tile.y):
            self.engine.mouse_location = event.tile.x, event.tile.y

    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        """
        Handle the quit event.

        Args:
            event (tcod.event.Quit): The quit event.

        Returns:
            Optional[Action]: The action to be taken.

        Raises:
            SystemExit: The system exit
        """
        raise SystemExit()

    def on_render(self, console: tcod.Console) -> None:
        """
        Calls the `render` method from the `Engine` class using the given
        console.

        Args:
            console: The console to render to.
        """
        self.engine.render(console)


class MainGameEventHandler(EventHandler):
    """
    The main game event handler.
    """
    @override
    def handle_events(self, context: tcod.context.Context) -> None:
        """
        Handle the turn events.
        """
        for event in tcod.event.wait():
            context.convert_event(event)

            action = self.dispatch(event)

            if action is None:
                continue

            action.perform()

            self.engine.handle_enemy_turns()
            self.engine.update_fov()

    @override
    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        """
        Handle the quit event.

        Args:
            event (tcod.event.Quit): The quit event.

        Returns:
            Optional[Action]: The action to be taken.

        Raises:
            SystemExit: The system exit exception.
        """
        raise SystemExit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        """
        Handle the keydown event.

        Args:
            event (tcod.event.KeyDown): The keydown event.

        Returns:
            Optional[Action]: The action to be taken.
        """
        action: Optional[Action] = None

        key = event.sym

        player = self.engine.player

        if key in MOVE_KEYS:
            dx, dy = MOVE_KEYS[key]
            action = BumpAction(player, dx, dy)
        elif key in WAIT_KEYS:
            action = WaitAction(player)
        elif key == tcod.event.KeySym.ESCAPE:
            action = EscapeAction(player)
        elif key == tcod.event.KeySym.v:
            self.engine.event_handler = HistoryViewer(self.engine)

        return action


class GameOverEventHandler(EventHandler):
    """
    The game over event handler.
    """
    @override
    def handle_events(self, context: tcod.context.Context) -> None:
        """
        Handle the events.
        """
        for event in tcod.event.wait():
            action = self.dispatch(event)

            if action is None:
                continue

            action.perform()

    @override
    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        """
        Handle the keydown event.

        Args:
            event (tcod.event.KeyDown): The keydown event.

        Returns:
            Optional[Action]: The action to be taken.
        """
        action: Optional[Action] = None

        key = event.sym

        if key == tcod.event.KeySym.ESCAPE:
            action = EscapeAction(self.engine.player)

        return action


class HistoryViewer(EventHandler):
    """
    Prints the history on a larger window which can be navigated.

    Attributes:
        log_length (int): The length of the message log.
        cursor (int): The current position of the cursor.
    """
    def __init__(self, engine: Engine):
        """
        Initialises the history viewer.

        Args:
            engine (Engine): The game engine
        """
        super().__init__(engine)
        self.log_length = len(engine.message_log.messages)
        self.cursor = self.log_length - 1

    @override
    def on_render(self, console: tcod.Console) -> None:
        """
        Renders the message log.

        Args:
            console: The console to render to.
        """
        super().on_render(console)

        log_console = (
            tcod.console.Console(console.width - 6, console.height - 6))

        # Draw a frame with a custom banner title.
        log_console.draw_frame(0, 0, log_console.width, log_console.height)
        log_console.print_box(
            0, 0, log_console.width, 1, "┤Message history├",
            alignment=tcod.constants.CENTER
        )

        # Render the message log using the cursor parameter.
        self.engine.message_log.render_messages(
            log_console,
            1,
            1,
            log_console.width - 2,
            log_console.height - 2,
            self.engine.message_log.messages[: self.cursor + 1],
        )
        log_console.blit(console, 3, 3)

    @override
    def ev_keydown(self, event: tcod.event.KeyDown) -> None:
        """
        Handle the keydown event.

        Overrides the default keydown event to allow for scrolling through the
        message log.
        """
        # Fancy conditional movement to make it feel right.
        if event.sym in CURSOR_Y_KEYS:
            adjust = CURSOR_Y_KEYS[event.sym]
            if adjust < 0 and self.cursor == 0:
                # Only move from the top to the bottom when you're on the edge.
                self.cursor = self.log_length - 1
            elif adjust > 0 and self.cursor == self.log_length - 1:
                # Same with bottom to top movement.
                self.cursor = 0
            else:
                # Otherwise move while staying clamped to the bounds of the
                # history log.
                self.cursor = max(0, min(self.cursor + adjust,
                                         self.log_length - 1))
        elif event.sym == tcod.event.KeySym.HOME:
            self.cursor = 0  # Move directly to the top message.
        elif event.sym == tcod.event.KeySym.END:
            # Move directly to the last message.
            self.cursor = self.log_length - 1
        else:
            # Any other key moves back to the main game state.
            self.engine.event_handler = MainGameEventHandler(self.engine)
