from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import tcod.event

from actions import Action, BumpAction, EscapeAction

if TYPE_CHECKING:
    from engine import Engine


class EventHandler(tcod.event.EventDispatch[Action]):
    """
    An event handler for the game.
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
        Handle the turn events.
        """
        for event in tcod.event.wait():
            action = self.dispatch(event)

            if action is None:
                continue

            action.perform()

            self.engine.handle_enemy_turns()
            self.engine.update_fov()

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

        if key == tcod.event.KeySym.UP or key == tcod.event.KeySym.w:
            action = BumpAction(player, dx=0, dy=-1)
        if key == tcod.event.KeySym.DOWN or key == tcod.event.KeySym.s:
            action = BumpAction(player, dx=0, dy=1)
        if key == tcod.event.KeySym.LEFT or key == tcod.event.KeySym.a:
            action = BumpAction(player, dx=-1, dy=0)
        if key == tcod.event.KeySym.RIGHT or key == tcod.event.KeySym.d:
            action = BumpAction(player, dx=1, dy=0)

        elif key == tcod.event.KeySym.ESCAPE:
            action = EscapeAction(player)

        return action
