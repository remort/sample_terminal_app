import curses
import random

from dto import Coordinates, Point, Size, Tile
from storage import RuntimeStorage
from utils import make_coordinates_from_size


class MapController:
    def __init__(self, pad, storage: RuntimeStorage, pad_size: Size, screen_size: Size):
        self.st = storage

        self.st.scene_size = Size(w=screen_size.w, h=screen_size.h)
        self.st.map_size = Size(w=pad_size.w, h=pad_size.h)

        self.st.scene_coords = make_coordinates_from_size(screen_size)
        self.st.map_coords = make_coordinates_from_size(pad_size)

        self.st.map = self._generate_map(pad_size.w, pad_size.h)

        self._pad = pad

        self.calculate_initial_screen_position()
        self.draw_surface()

    @staticmethod
    def _generate_map(pad_w, pad_h):
        _map = []
        for y in range(0, pad_h):
            line = []
            for x in range(0, pad_w):
                line.append(Tile(x=x, y=y, ch=random.choice('.,_'), attr=curses.A_DIM, height=random.randint(0, 5)))
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
        if self.st.scene_size.w > self.st.map_size.w or self.st.scene_size.h > self.st.map_size.h:
            pass
        else:
            lx = (self.st.map_size.w - self.st.scene_size.w) // 2 + (self.st.map_size.w - self.st.scene_size.w) % 2
            rx = lx + self.st.scene_size.w
            ty = (self.st.map_size.h - self.st.scene_size.h) // 2 + (self.st.map_size.h - self.st.scene_size.h) % 2
            by = ty + self.st.scene_size.h
            self.st.screen_pad_coords = Coordinates(
                tl=Point(x=lx, y=ty), tr=Point(x=rx, y=ty), br=Point(x=rx, y=by), bl=Point(x=lx, y=by)
            )

    def scroll_v(self, step):
        if self.st.screen_pad_coords.tl.y <= 0:
            if step > 0:
                self.st.screen_is_most_top = True
                self.refresh()
                return

        if self.st.screen_pad_coords.br.y >= self.st.map_size.h:
            if step < 0:
                self.st.screen_is_most_bottom = True
                self.refresh()
                return

        if self.st.actor_screen_center_offset.y != 0:
            self.refresh()
            return

        self.st.screen_pad_coords.tl.y -= step
        self.st.screen_pad_coords.tr.y -= step
        self.st.screen_pad_coords.br.y -= step
        self.st.screen_pad_coords.bl.y -= step

        self.st.screen_is_most_top = False
        self.st.screen_is_most_bottom = False

        self.refresh()

    def scroll_h(self, step):
        if self.st.screen_pad_coords.tr.x >= self.st.map_size.w:
            if step > 0:
                self.st.screen_is_most_right = True
                self.refresh()
                return

        if self.st.screen_pad_coords.tl.x <= 0:
            if step < 0:
                self.st.screen_is_most_left = True
                self.refresh()
                return

        if self.st.actor_screen_center_offset.x != 0:
            self.refresh()
            return

        self.st.screen_pad_coords.tl.x += step
        self.st.screen_pad_coords.tr.x += step
        self.st.screen_pad_coords.br.x += step
        self.st.screen_pad_coords.bl.x += step

        self.st.screen_is_most_right = False
        self.st.screen_is_most_left = False

        self.refresh()

    def draw_surface(self):
        for row in self.st.map:
            for tile in row:
                self._pad.addch(tile.y, tile.x, tile.ch, tile.attr)
        self.refresh()

    def refresh(self):
        self._pad.noutrefresh(
            self.st.screen_pad_coords.tl.y, self.st.screen_pad_coords.tl.x,
            0, 0,
            self.st.scene_coords.br.y, self.st.scene_coords.br.x,
        )

    def do_animation(self):
        pass
