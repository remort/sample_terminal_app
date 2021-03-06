import typing as t
from dto import Coordinates, Point, Size, Tile


class RuntimeStorage:
    def __init__(self):
        self.scene_size: t.Optional[Size] = None
        self.map_size: t.Optional[int] = None

        self.scene_coords: t.Optional[Coordinates] = None
        self.map_coords: t.Optional[Coordinates] = None

        self.screen_pad_coords: t.Optional[Coordinates] = None

        self.surface: t.List[t.List[int]] = []
        self.map: t.Optional[t.List[t.List[Tile]]] = None

        self.bar_height: int = 1

        self.actor_screen_center_offset: t.Optional[Point] = None
        self.actor_location: t.Optional[Point] = None

        self.screen_is_most_top: bool = False
        self.screen_is_most_bottom: bool = False
        self.screen_is_most_right: bool = False
        self.screen_is_most_left: bool = False

        self.messages: t.List[str] = []
