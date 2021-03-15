import math

from dto import Coordinates, Point, Size, Tile
from storage import MapType


def make_coordinates_by_size(size: Size) -> Coordinates:
    """Makes only coordinates object with starting point at 0,0."""

    return Coordinates(
        tl=Point(x=0, y=0),
        tr=Point(x=size.w - 1, y=0),
        br=Point(x=size.w - 1, y=size.h - 1),
        bl=Point(x=0, y=size.h - 1),
    )


def make_map_coordinates_by_pad_dimensions(map_pad_h: int, map_pad_w: int) -> Coordinates:
    """Makes only coordinates object with starting point at 0,0."""

    return Coordinates(
        tl=Point(x=0, y=0),
        tr=Point(x=map_pad_w - 1, y=0),
        br=Point(x=map_pad_w - 1, y=map_pad_h - 1),
        bl=Point(x=0, y=map_pad_h - 1),
    )


def get_map_scale_by_screen_size(screen_height: int, screen_width: int) -> int:
    power_of_2 = math.log2(max(screen_height, screen_width))
    return int(power_of_2) + 1


def generate_map_from_surface(storage) -> MapType:
    _map = list()
    for y, row in enumerate(storage.surface):
        line = list()
        for x, col in enumerate(row):
            line.append(
                Tile(
                    x=x,
                    y=y,
                    ch=storage.heights_to_colors_map[col][0],
                    color=storage.heights_to_colors_map[col][1],
                    height=col,
                )
            )
        _map.append(line)
    return _map
