class Action:
    """
    A generic action to represent an action taken by the player.
    """
    pass


class EscapeAction(Action):
    """
    An action to exit the game.
    """
    pass


class MovementAction(Action):
    """
    An action to move in a direction.

    Attributes:
        dx: The amount to move in the x-direction.
        dy: The amount to move in the y-direction.
    """
    def __init__(self, dx: int, dy: int):
        """
        Initialize the movement action.

        Args:
            dx: The amount to move in the x-direction.
            dy: The amount to move in the y-direction.
        """
        super().__init__()

        self.dx = dx
        self.dy = dy
