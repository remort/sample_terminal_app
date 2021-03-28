import logging
import math
import operator
import typing as t

from dto import Coordinates, Point, Size, Tile
from storage import MapType

log = logging.getLogger(__name__)


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
                    ch=storage.heights_to_colors_map[col][0],
                    color=storage.heights_to_colors_map[col][1],
                    height=col,
                    loc=Point(x=x, y=y)
                )
            )
        _map.append(line)
    return _map


def path_between_two_dots(p1: Point, p2: Point) -> t.Generator[Point, None, Point]:
    """
    # Linear interpolation algorithm implementation. Finds path between two points in XY matrix.

    # "long", X-axis oriented paths tests:
    # Y axis increasing
    >>> [p for p in path_between_two_dots(Point(x=1,y=2), Point(x=11, y=7))]
    [Point(x=2, y=2), Point(x=3, y=3), Point(x=4, y=4), Point(x=5, y=4), Point(x=6, y=4), Point(x=7, y=5), Point(x=8, y=6), Point(x=9, y=6), Point(x=10, y=6)]

    >>> [p for p in path_between_two_dots(Point(x=10,y=2), Point(x=3, y=9))]
    [Point(x=9, y=3), Point(x=8, y=4), Point(x=7, y=5), Point(x=6, y=6), Point(x=5, y=7), Point(x=4, y=8)]

    # Y axis decreasing
    >>> [p for p in path_between_two_dots(Point(x=1,y=9), Point(x=11, y=1))]
    [Point(x=2, y=8), Point(x=3, y=7), Point(x=4, y=7), Point(x=5, y=6), Point(x=6, y=5), Point(x=7, y=4), Point(x=8, y=3), Point(x=9, y=3), Point(x=10, y=2)]

    >>> [p for p in path_between_two_dots(Point(x=10,y=8), Point(x=3, y=2))]
    [Point(x=9, y=7), Point(x=8, y=6), Point(x=7, y=5), Point(x=6, y=5), Point(x=5, y=4), Point(x=4, y=3)]

    # Y axis stalled (difference by Y is 0)
    >>> [p for p in path_between_two_dots(Point(x=1,y=9), Point(x=10, y=1))]
    [Point(x=2, y=8), Point(x=3, y=7), Point(x=4, y=6), Point(x=5, y=5), Point(x=6, y=5), Point(x=7, y=4), Point(x=8, y=3), Point(x=9, y=2)]

    >>> [p for p in path_between_two_dots(Point(x=9,y=8), Point(x=1, y=8))]
    [Point(x=8, y=8), Point(x=7, y=8), Point(x=6, y=8), Point(x=5, y=8), Point(x=4, y=8), Point(x=3, y=8), Point(x=2, y=8)]

    # "tall", Y-axis oriented paths tests:
    # X axis increasing
    >>> [p for p in path_between_two_dots(Point(x=3,y=2), Point(x=9, y=12))]
    [Point(x=4, y=3), Point(x=4, y=4), Point(x=5, y=5), Point(x=5, y=6), Point(x=6, y=7), Point(x=7, y=8), Point(x=7, y=9), Point(x=8, y=10), Point(x=8, y=11)]

    >>> [p for p in path_between_two_dots(Point(x=3,y=12), Point(x=9, y=3))]
    [Point(x=4, y=11), Point(x=4, y=10), Point(x=5, y=9), Point(x=6, y=8), Point(x=6, y=7), Point(x=7, y=6), Point(x=8, y=5), Point(x=8, y=4)]

    # X axis decreasing
    >>> [p for p in path_between_two_dots(Point(x=8,y=2), Point(x=1, y=12))]
    [Point(x=7, y=3), Point(x=7, y=4), Point(x=6, y=5), Point(x=5, y=6), Point(x=4, y=7), Point(x=4, y=8), Point(x=3, y=9), Point(x=2, y=10), Point(x=2, y=11)]

    >>> [p for p in path_between_two_dots(Point(x=9,y=4), Point(x=2, y=14))]
    [Point(x=8, y=5), Point(x=8, y=6), Point(x=7, y=7), Point(x=6, y=8), Point(x=6, y=9), Point(x=5, y=10), Point(x=4, y=11), Point(x=3, y=12), Point(x=3, y=13)]

    # X axis stalled (difference by X is 0)
    >>> [p for p in path_between_two_dots(Point(x=8,y=2), Point(x=8, y=12))]
    [Point(x=8, y=3), Point(x=8, y=4), Point(x=8, y=5), Point(x=8, y=6), Point(x=8, y=7), Point(x=8, y=8), Point(x=8, y=9), Point(x=8, y=10), Point(x=8, y=11)]

    >>> [p for p in path_between_two_dots(Point(x=6,y=13), Point(x=6, y=4))]
    [Point(x=6, y=12), Point(x=6, y=11), Point(x=6, y=10), Point(x=6, y=9), Point(x=6, y=8), Point(x=6, y=7), Point(x=6, y=6), Point(x=6, y=5)]
    """
    if p1 == p2:
        return p1

    y_diff = p2.y - p1.y
    x_diff = p2.x - p1.x

    move_op = operator.add
    if abs(y_diff) > abs(x_diff):
        move_over_x = False
        if y_diff < 0:
            move_op = operator.sub
        slope = x_diff / y_diff
    else:
        move_over_x = True
        if x_diff < 0:
            move_op = operator.sub
        slope = y_diff / x_diff

    steps = max(abs(x_diff), abs(y_diff))

    for step in range(1, steps):
        if move_over_x:
            x = move_op(p1.x, step)
            y = round(p1.y + slope * (x - p1.x))
        else:
            y = move_op(p1.y, step)
            x = round(p1.x + slope * (y - p1.y))

        yield Point(x=x, y=y)
