import typing as t
from curses import KEY_DOWN, KEY_LEFT, KEY_RIGHT, KEY_UP

from colors import (
    COLOR_MAP_H1,
    COLOR_MAP_H2,
    COLOR_MAP_H3,
    COLOR_MAP_H4,
    COLOR_MAP_H5,
    COLOR_MAP_H6,
    COLOR_MAP_H7,
    COLOR_MAP_H8,
    COLOR_MAP_H9,
)

BAR_HEIGHT: int = 1

MOVE_KEYS = (KEY_UP, KEY_DOWN, KEY_RIGHT, KEY_LEFT)
KEY_UP = KEY_UP
KEY_DOWN = KEY_DOWN
KEY_LEFT = KEY_LEFT
KEY_RIGHT = KEY_RIGHT
KEY_SAVE = 115  # 's'

HEIGHTS_TO_COLORS_MAP: t.Dict[int, t.Tuple[str, int]] = {
    0: ('0', COLOR_MAP_H1),
    1: ('1', COLOR_MAP_H2),
    2: ('2', COLOR_MAP_H3),
    3: ('3', COLOR_MAP_H4),
    4: ('4', COLOR_MAP_H5),
    5: ('5', COLOR_MAP_H6),
    6: ('6', COLOR_MAP_H7),
    7: ('7', COLOR_MAP_H8),
    8: ('8', COLOR_MAP_H9),
}

HEIGHTS_TO_WAIT_TIME_MAP: t.Dict[int, float] = {
    0: 1.0,
    1: 0.05,
    2: 0.1,
    3: 0.2,
    4: 0.3,
    5: 0.5,
    6: 0.7,
    7: 0.9,
    8: 1.1,
}
