from __future__ import annotations

from typing import Optional, TYPE_CHECKING, override

import tcod.event

from actions import Action, BumpAction, EscapeAction, WaitAction

if TYPE_CHECKING:
    from engine import Engine


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

WAIT_KEYS = {
    tcod.event.KeySym.PERIOD,
    tcod.event.KeySym.KP_5,
    tcod.event.KeySym.CLEAR,
}


class EventHandler(tcod.event.EventDispatch[Action]):
    """
    The event handler base class.
    """
    def __init__(self, engine: Engine):
        """
        The constructor for the event handler.

        Args:
            engine (Engine): The game engine.
        """
        self.engine = engine

    def handle_events(self) -> None:
        """
        Handle the events.

        Raises:
            NotImplementedError: The method is not implemented
        """
        raise NotImplementedError()

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


class MainGameEventHandler(EventHandler):
    """
    The main game event handler.
    """
    @override
    def handle_events(self) -> None:
        """
        Handle the turn events.
        """
        for event in tcod.event.wait():
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

        return action


class GameOverEventHandler(EventHandler):
    """
    The game over event handler.
    """
    @override
    def handle_events(self) -> None:
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
