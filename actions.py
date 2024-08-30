# Holds the different types of 'actions' that can be taken by the player

# The Action class is a base class that other actions will inherit from.
class Action:
    pass


# The EscapeAction class is a subclass of Action that represents the player wanting to exit the game.
class EscapeAction(Action):
    pass


# The MovementAction class is a subclass of Action that represents the player wanting to move in a direction.
class MovementAction(Action):
    def __init__(self, dx: int, dy: int):
        super().__init__()

        self.dx = dx
        self.dy = dy
