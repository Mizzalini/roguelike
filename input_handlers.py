# This file contains the EventHandler class, which is responsible for handling input events and converting them into
# actions.

from typing import Optional

import tcod.event

from actions import Action, EscapeAction, MovementAction


# The EventHandler class is a subclass of tcod.event.EventDispatch that is responsible for handling input events and
# converting them into actions.
class EventHandler(tcod.event.EventDispatch[Action]):
    # The ev_quit method is called when the player tries to close the game window.
    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()

    # The ev_keydown method is called when the player presses a key.
    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None

        key = event.sym

        if key == tcod.event.KeySym.UP or key == tcod.event.KeySym.w:
            action = MovementAction(dx=0, dy=-1)
        if key == tcod.event.KeySym.DOWN or key == tcod.event.KeySym.s:
            action = MovementAction(dx=0, dy=1)
        if key == tcod.event.KeySym.LEFT or key == tcod.event.KeySym.a:
            action = MovementAction(dx=-1, dy=0)
        if key == tcod.event.KeySym.RIGHT or key == tcod.event.KeySym.d:
            action = MovementAction(dx=1, dy=0)

        elif key == tcod.event.KeySym.ESCAPE:
            action = EscapeAction()

        return action