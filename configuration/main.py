import logging
import typing as t

from dto import Coordinates, MapType, Point, Size


log = logging.getLogger(__name__)


class Configuration:
    def __init__(self, storage_handler):
        self.storage_handler = storage_handler

        # A power of two which defines map size.
        self.map_scale: t.Optional[int] = None
        # Size computed from scale.
        self.map_size: t.Optional[int] = None

        self.map_pad_h: int = 0
        self.map_pad_w: int = 0

        # 2-dim. array of random generated heights. Maps to self.map later.
        self.surface: t.List[t.List[int]] = []
        # 2-dimensional array of map Tiles: [y,[x]] resulting from self.surface.
        self.map: t.Optional[MapType] = None
        self.status_bar_width: int = 0

        # Height and Width of main scene ncurses pad.
        self.scene_size: t.Optional[Size] = None
        # Main scene ncurses pad coordinates starting from 0,0 point. Actor position computes inside this coords.
        self.scene_pad_coords: t.Optional[Coordinates] = None
        # Current main scene ncurses pad position relative to larger map coordinates.
        self.scene_on_map_coords: t.Optional[Coordinates] = None

        # Point stores Actor point offset
        self.actor_scene_center_offset: Size = Size(w=0, h=0)

        # Actor point location on map coordinates.
        self.actor_on_map_pos: t.Optional[Point] = None

        # Unveils map, do not discover map on move, makes move speed high.
        self.debug: bool = False

        # Map tile is drawn as 2 terminal symbols horizontally: XX, instead of standard one symbol per tile: X.
        self.square_tiles: bool = False

        # Flags designates if actor reached the border of the map.
        self.scene_is_most_top: bool = False
        self.scene_is_most_bottom: bool = False
        self.scene_is_most_right: bool = False
        self.scene_is_most_left: bool = False

        # For square tiles mode only when horizontal move takes two symbols.
        # When screen in odd, we move left, reach map border: move screen half step,
        # then start moving actor on screen on the rest half of the step.
        self.short_scroll: bool = False

        # Move key pressed, screen edge is even, border just reached - do not move actor second time on screen.
        # If map border is reached and we move but map doesn't move anymore - move actor on screen then.
        self.scene_moved: bool = False

        self.messages: t.List[str] = []

    def load(self, file_name: str):
        self.storage_handler.load(self, file_name)

    def save(self):
        self.storage_handler.save(self)
