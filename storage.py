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
from dto import Coordinates, Point, Size, Tile

MapType = t.List[t.List[Tile]]


class RuntimeStorage:
    def __init__(self):
        # A power of two which defines map size.
        self.map_scale: t.Optional[int] = None
        # Size computed from scale.
        self.map_size: t.Optional[int] = None

        self.map_pad_h: int = 0
        self.map_pad_w: int = 0
        self.map_pad_coords: t.Optional[Coordinates] = None

        # 2-dim. array of random generated heights. Maps to self.map later.
        self.surface: t.List[t.List[int]] = []
        # 2-dim. array of map Tiles: [y,[x]] resulting from self.surface.
        self.map: t.Optional[MapType] = None
        # Status bar ncurses pad height.
        self.bar_height: int = 1
        self.status_bar_width: int = 0

        # Height and Width of main scene ncurses pad.
        self.scene_size: t.Optional[Size] = None
        # Main scene ncurses pad coordinates starting from 0,0 point. Actor position computes inside this coords.
        self.scene_pad_coords: t.Optional[Coordinates] = None
        # Current main scene ncurses pad position in larger map coordinates.
        self.scene_on_map_coords: t.Optional[Coordinates] = None

        # Point stores Actor point offset
        self.actor_screen_center_offset: Size = Size(w=0, h=0)

        # Actor point location on map coordinates.
        self.actor_location: t.Optional[Point] = None

        # Current tile height.
        self.curr_height: t.Optional[int] = None

        # Unveils map, do not discover map on move, makes move speed high.
        self.debug: bool = False

        # Flags designates if actor reached the border of the map.
        self.screen_is_most_top: bool = False
        self.screen_is_most_bottom: bool = False
        self.screen_is_most_right: bool = False
        self.screen_is_most_left: bool = False

        # Map tile is drawn as 2 terminal symbols horizontally: XX, instead of standard one symbol per tile: X.
        self.square_tiles: bool = False

        # For square tiles mode only when horizontal move takes two symbols.
        # When screen in odd, we move left, reach map border: move screen half step,
        # then start moving actor on screen on the rest half of the step.
        self.short_scroll: bool = False

        # Move key pressed, screen edge is even, border just reached - do not move actor second time on screen.
        # If map border is reached and we move but map doesn't move anymore - move actor on screen then.
        self.scene_moved: bool = False

        self.messages: t.List[str] = []
        self.move_keys = (KEY_UP, KEY_DOWN, KEY_RIGHT, KEY_LEFT)
        self.key_up = KEY_UP
        self.key_down = KEY_DOWN
        self.key_left = KEY_LEFT
        self.key_right = KEY_RIGHT

        self.heights_to_colors_map: t.Dict[int, t.Tuple[str, int]] = {
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

        self.heights_to_wait_time_map: t.Dict[int, float] = {
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
