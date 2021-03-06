import math

from dto import Coordinates, Point, Size


def make_coordinates_by_size(size: Size) -> Coordinates:
    """Makes only coordinates object with starting point at 0,0."""

    return Coordinates(
        tl=Point(x=0, y=0),
        tr=Point(x=size.w - 1, y=0),
        br=Point(x=size.w - 1, y=size.h - 1),
        bl=Point(x=0, y=size.h - 1),
    )


def make_map_coordinates_by_map_size(size: int) -> Coordinates:
    """Makes only coordinates object with starting point at 0,0."""

    return Coordinates(
        tl=Point(x=0, y=0),
        tr=Point(x=size - 1, y=0),
        br=Point(x=size - 1, y=size - 1),
        bl=Point(x=0, y=size - 1),
    )


def get_map_scale_by_screen_size(screen_height, screen_width) -> int:
    power_of_2 = math.log2(max(screen_height, screen_width))
    return int(power_of_2) + 1
