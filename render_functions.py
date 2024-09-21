from __future__ import annotations

from typing import TYPE_CHECKING

import colour

if TYPE_CHECKING:
    from tcod import Console
    from engine import Engine
    from game_map import GameMap


def get_names_at_location(x: int, y: int, game_map: GameMap) -> str:
    """
    Returns a capitalised string of entity names at the specified coordinates.

    Only returns the names of enemies who are currently visible to the player.

    Args:
        x (int): The x-coordinate to be checked.
        y (int): The y-coordinate to be checked.
        game_map (GameMap): The game map.
    """
    if not game_map.in_bounds(x, y) or not game_map.visible[x, y]:
        return ""

    names = ", ".join(
        entity.name for entity in game_map.entities if entity.x == x and
        entity.y == y
    )

    return names.capitalize()


def render_bar(
        console: Console,
        current_value: int,
        maximum_value: int,
        total_width: int
) -> None:
    """
    Render a bar that represents a value between 0 and maximum_value.

    Args:
        console (Console): The console to render the bar to.
        current_value (int): The current value of the bar.
        maximum_value (int): The maximum value of the bar.
        total_width (int): The total width of the bar.
    """
    bar_width = int(float(current_value) / maximum_value * total_width)

    # Render the background first
    console.draw_rect(
        x=0, y=44, width=total_width, height=1, ch=1, bg=colour.bar_empty
    )

    # Render the filled bar on top
    if bar_width > 0:
        console.draw_rect(
            x=0, y=44, width=bar_width, height=1, ch=1, bg=colour.bar_filled
        )

    console.print(
        x=1, y=44, string=f'HP: {current_value}/{maximum_value}',
        fg=colour.bar_text
    )


def render_names_at_mouse_location(
        console: Console,
        x: int,
        y: int,
        engine: Engine
) -> None:
    """
    Render the names of entities at the player's mouse location.

    Args:
        console (Console): The console to render the names to.
        x (int): The x-coordinate to render the names to.
        y (int): The y-coordinate to render the names to.
        engine (Engine): The game engine.
    """
    mouse_x, mouse_y = engine.mouse_location

    names_at_mouse_location = get_names_at_location(
        x=mouse_x, y=mouse_y, game_map=engine.game_map
    )

    console.print(x=x, y=y, string=names_at_mouse_location)
