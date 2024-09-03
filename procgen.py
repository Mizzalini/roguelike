from __future__ import annotations

import random
from typing import Iterator, List, Tuple, TYPE_CHECKING

import tcod

from game_map import GameMap
import tile_types

if TYPE_CHECKING:
    from entity import Entity


class RectangularRoom:
    """
    A rectangular room in the dungeon.

    Attributes:
        x1 (int): The x coordinate of the top left corner of the room.
        y1 (int): The y coordinate of the top left corner of the room.
        x2 (int): The x coordinate of the bottom right corner of the room.
        y2 (int): The y coordinate of the bottom right corner of the room.
    """

    def __init__(self, x: int, y: int, width: int, height: int):
        """
        Initialize a new room.

        Takes the coordinates of the top left corner, and computes the bottom
        right corner.

        Args:
            x (int): The x coordinate of the room.
            y (int): The y coordinate of the room.
            width (int): The width of the room.
            height (int): The height of the room.
        """
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height

    @property
    def centre(self) -> Tuple[int, int]:
        """
        Get the centre of the room.

        Returns:
            Tuple[int, int]: The x, y coordinates of the centre of the room.
        """
        centre_x = int((self.x1 + self.x2) / 2)
        centre_y = int((self.y1 + self.y2) / 2)

        return centre_x, centre_y

    @property
    def inner(self) -> Tuple[slice, slice]:
        """
        Get the inner area of the room.

        Returns:
            Tuple[slice, slice]: The inner area of the room as a tuple of
            slices.
        """
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)

    def intersects(self, other: RectangularRoom) -> bool:
        """
        Check if this room intersects with another room.

        Args:
            other (RectangularRoom): The other room to check for intersection.

        Returns:
            bool: True if the rooms intersect, False otherwise.
        """
        return (
                self.x1 <= other.x2
                and self.x2 >= other.x1
                and self.y1 <= other.y2
                and self.y2 >= other.y1
        )


def tunnel_between(
        start: Tuple[int, int],
        end: Tuple[int, int]
) -> Iterator[Tuple[int, int]]:
    """
    Create a tunnel between two points.

    Uses Bresenham's line algorithm to create a tunnel between two points.

    Args:
        start (Tuple[int, int]): The x, y coordinates of the start point.
        end (Tuple[int, int]): The x, y coordinates of the end point.

    Yields:
        Tuple[int, int]: The x, y coordinates of the next point in the tunnel.
    """
    x1, y1 = start
    x2, y2 = end

    if random.random() < 0.5:
        corner_x, corner_y = x2, y1
    else:
        corner_x, corner_y = x1, y2

    # Generate the coordinates for the tunnel
    for x, y in tcod.los.bresenham((x1, y1),
                                   (corner_x, corner_y)).tolist():
        yield x, y

    for x, y in tcod.los.bresenham((corner_x, corner_y),
                                   (x2, y2)).tolist():
        yield x, y


def generate_dungeon(
        max_rooms: int,
        room_min_size: int,
        room_max_size: int,
        map_width: int,
        map_height: int,
        player: Entity
) -> GameMap:
    """
    Generate a new dungeon map.

    Args:
        max_rooms (int): The maximum number of rooms to generate.
        room_min_size (int): The minimum size of a room.
        room_max_size (int): The maximum size of a room.
        map_width (int): The width of the map.
        map_height (int): The height of the map.
        player (Entity): The player entity.

    Returns:
        GameMap: The generated dungeon map.
    """
    dungeon = GameMap(map_width, map_height)

    rooms: List[RectangularRoom] = []

    for r in range(max_rooms):
        room_width = random.randint(room_min_size, room_max_size)
        room_height = random.randint(room_min_size, room_max_size)

        x = random.randint(0, dungeon.width - room_width - 1)
        y = random.randint(0, dungeon.height - room_height - 1)

        new_room = RectangularRoom(x, y, room_width, room_height)

        # Run through the other rooms and see if they intersect with this one
        if any(new_room.intersects(other_room) for other_room in rooms):
            continue

        # Dig out this room
        dungeon.tiles[new_room.inner] = tile_types.floor

        if len(rooms) == 0:
            # The first room, where the player starts
            player.x, player.y = new_room.centre
        else:
            # Dig out a tunnel between this room and the previous one
            for x, y in tunnel_between(rooms[-1].centre, new_room.centre):
                dungeon.tiles[x, y] = tile_types.floor

        rooms.append(new_room)

    return dungeon
