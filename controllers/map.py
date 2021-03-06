import curses

from controllers.base import BaseController
from dto import Coordinates, Point, Size, Tile
from storage import RuntimeStorage
from utils import make_coordinates_by_size


class MapController(BaseController):
    def __init__(self, pad, storage: RuntimeStorage, scene_size: Size):
        super().__init__(pad, storage)

        self.st.scene_size = scene_size
        self.st.scene_coords = make_coordinates_by_size(scene_size)

        self.st.map = self._generate_map_from_surface()

        self.calculate_initial_screen_position()
        self.draw_surface()

    def _generate_map_from_surface(self):
        _map = list()
        for y, row in enumerate(self.st.surface):
            line = list()
            for x, col in enumerate(row):
                line.append(
                    Tile(
                        x=x,
                        y=y,
                        ch=self.st.heights_to_colors_map[col][0],
                        color=self.st.heights_to_colors_map[col][1],
                        height=col,
                    )
                )
            _map.append(line)
        return _map

    def process_event(self, key):
        if key == curses.KEY_UP:
            self.scroll_v(1)
        if key == curses.KEY_DOWN:
            self.scroll_v(-1)
        if key == curses.KEY_RIGHT:
            self.scroll_h(1)
        if key == curses.KEY_LEFT:
            self.scroll_h(-1)

    def calculate_initial_screen_position(self):
        if self.st.scene_size.w > self.st.map_size or self.st.scene_size.h > self.st.map_size:
            raise ValueError(
                'Screen ({}x{}) can not be larger than a map: {}.'.format(
                    self.st.scene_size.w,
                    self.st.scene_size.h,
                    self.st.map_size,
                ))
        else:
            map_edge = self.st.map_size -1
            lx = (map_edge - self.st.scene_size.w) // 2 + (map_edge - self.st.scene_size.w) % 2
            rx = lx + self.st.scene_size.w
            ty = (map_edge - self.st.scene_size.h) // 2 + (map_edge - self.st.scene_size.h) % 2
            by = ty + self.st.scene_size.h

            self.st.scene_on_map_coords = Coordinates(
                tl=Point(x=lx, y=ty), tr=Point(x=rx, y=ty), br=Point(x=rx, y=by), bl=Point(x=lx, y=by)
            )

    def scroll_v(self, step):
        if self.st.scene_on_map_coords.tl.y <= 0:
            if step > 0:
                self.st.screen_is_most_top = True
                self.refresh()
                return

        if self.st.scene_on_map_coords.br.y >= self.st.map_size:
            if step < 0:
                self.st.screen_is_most_bottom = True
                self.refresh()
                return

        if self.st.actor_screen_center_offset.h != 0:
            self.refresh()
            return

        self.st.scene_on_map_coords.tl.y -= step
        self.st.scene_on_map_coords.tr.y -= step
        self.st.scene_on_map_coords.br.y -= step
        self.st.scene_on_map_coords.bl.y -= step

        self.st.screen_is_most_top = False
        self.st.screen_is_most_bottom = False

        self.refresh()

    def scroll_h(self, step):
        if self.st.scene_on_map_coords.tr.x >= self.st.map_size:
            if step > 0:
                self.st.screen_is_most_right = True
                self.refresh()
                return

        if self.st.scene_on_map_coords.tl.x <= 0:
            if step < 0:
                self.st.screen_is_most_left = True
                self.refresh()
                return

        if self.st.actor_screen_center_offset.w != 0:
            self.refresh()
            return

        self.st.scene_on_map_coords.tl.x += step
        self.st.scene_on_map_coords.tr.x += step
        self.st.scene_on_map_coords.br.x += step
        self.st.scene_on_map_coords.bl.x += step

        self.st.screen_is_most_right = False
        self.st.screen_is_most_left = False

        self.refresh()

    def draw_surface(self):
        for row in self.st.map:
            for tile in row:
                self._pad.print(tile.ch, tile.y, tile.x, cpn=tile.color)
        self.refresh()

    def refresh(self):
        self._pad.noutrefresh(
            self.st.scene_on_map_coords.tl.y, self.st.scene_on_map_coords.tl.x,
            0, 0,
            self.st.scene_coords.br.y, self.st.scene_coords.br.x,
        )

    def do_animation(self):
        pass
