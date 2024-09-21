from typing import List, Reversible, Tuple
import textwrap

import tcod

import colour


class Message:
    """
    A message to be displayed in the message log.

    Attributes:
        plain_text (str): The plain text of the message.
        fg (Tuple[int, int, int]): The text colour.
        count (int): The number of times this message has been added.
    """
    def __init__(self, text: str, fg: Tuple[int, int, int]):
        """
        Initialise a message.

        Args:
            text (str): The message text.
            fg (Tuple[int, int, int]): The text colour.
        """
        self.plain_text = text
        self.fg = fg
        self.count = 1

    @property
    def full_text(self) -> str:
        """
        The full text of this message, including the count if necessary.

        Returns:
            str: The full text of this message.
        """
        if self.count > 1:
            return f"{self.plain_text} (x{self.count})"
        return self.plain_text


class MessageLog:
    """
    A message log to store messages.

    Attributes:
        messages (List[Message]): The messages in this log.
    """
    def __init__(self) -> None:
        """
        Initialise the message log.
        """
        self.messages: List[Message] = []

    def add_message(
            self,
            text: str,
            fg: Tuple[int, int, int] = colour.white,
            *,
            stack: bool = True,
    ) -> None:
        """
        Add a message to this log.

        If `stack` is True, then the message can stack with a previous message
        of the same text

        Args:
            text (str): The message text.
            fg (Tuple[int, int, int], optional): The text colour.
            Defaults to white.
            stack (bool, optional): Whether to stack this message with identical
             messages. Defaults to True.
        """
        if stack and self.messages and text == self.messages[-1].plain_text:
            self.messages[-1].count += 1
        else:
            self.messages.append(Message(text, fg))

    def render(
            self,
            console: tcod.console.Console,
            x: int,
            y: int,
            width: int,
            height: int
    ) -> None:
        """
        Render this log over the given area.

        Args:
            console (tcod.Console): The console to render to.
            x (int): The x position to start rendering at.
            y (int): The y position to start rendering at.
            width (int): The width of the area to render to.
            height (int): The height of the area to render to.
        """
        self.render_messages(console, x, y, width, height, self.messages)

    @staticmethod
    def render_messages(
            console: tcod.console.Console,
            x: int,
            y: int,
            width: int,
            height: int,
            messages: Reversible[Message],
    ) -> None:
        """
        Render the messages provided.

        The `messages` are rendered starting at the last message and working
        backwards.

        Args:
            console (tcod.Console): The console to render to.
            x (int): The x position to start rendering at.
            y (int): The y position to start rendering at.
            width (int): The width of the area to render to.
            height (int): The height of the area to render to.
            messages (Reversible[Message]): The messages to render.
        """
        y_offset = height - 1

        for message in reversed(messages):
            for line in reversed(textwrap.wrap(message.full_text, width)):
                console.print(x=x, y=y + y_offset, string=line, fg=message.fg)
                y_offset -= 1
                if y_offset < 0:
                    return  # No more space to print messages
