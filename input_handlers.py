from typing import Optional

import tcod.event

from actions import Action, BumpAction, EscapeAction


class EventHandler(tcod.event.EventDispatch[Action]):
    """
    An event handler for the game.
    """
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

        if key == tcod.event.KeySym.UP or key == tcod.event.KeySym.w:
            action = BumpAction(dx=0, dy=-1)
        if key == tcod.event.KeySym.DOWN or key == tcod.event.KeySym.s:
            action = BumpAction(dx=0, dy=1)
        if key == tcod.event.KeySym.LEFT or key == tcod.event.KeySym.a:
            action = BumpAction(dx=-1, dy=0)
        if key == tcod.event.KeySym.RIGHT or key == tcod.event.KeySym.d:
            action = BumpAction(dx=1, dy=0)

        elif key == tcod.event.KeySym.ESCAPE:
            action = EscapeAction()

        return action
