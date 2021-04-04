import logging
import operator
import typing as t

from colors import COLOR_UNVEILED_MAP
from configuration.main import Configuration
from constants import KEY_DOWN, KEY_LEFT, KEY_RIGHT, KEY_UP, MOVE_KEYS
from controllers.base import BaseController
from dto import Coordinates, Point, Tile
from pad_wrapper import Pad
from utils import path_between_two_dots

log = logging.getLogger(__name__)


class MapController(BaseController):
    def __init__(self, pad: Pad, configuration: Configuration) -> None:
        super().__init__(pad, configuration)

        self.calculate_initial_scene_position()
        self.veiled_tile_char: str = '.'
        self.need_to_unveil = True
        self.vision = 8

        self.draw_map()

    def calculate_initial_scene_position(self) -> None:
        # Return, if loaded from saved file.
        if self.cf.scene_on_map_coords:
            return

        map_edge = self.cf.map_size
        horizontal_map_size = self.cf.map_size * 2 if self.cf.square_tiles else self.cf.map_size

        lx = (horizontal_map_size - self.cf.scene_size.w) // 2 + (horizontal_map_size - self.cf.scene_size.w) % 2
        rx = lx + self.cf.scene_size.w
        ty = (map_edge - self.cf.scene_size.h) // 2 + (map_edge - self.cf.scene_size.h) % 2
        by = ty + self.cf.scene_size.h

        self.cf.scene_on_map_coords = Coordinates(
            tl=Point(x=lx, y=ty), tr=Point(x=rx, y=ty), br=Point(x=rx, y=by), bl=Point(x=lx, y=by)
        )

    def unveil_tile(self, tile: Tile) -> None:
        tile.is_veiled = False
        self.pad.addch(tile.ch, tile.y, tile.x, cp=tile.color, sq=self.cf.square_tiles)

    def is_prev_tile_unveiled(self, ap: Point, tile: Tile) -> bool:
        prev_tile_loc = next(path_between_two_dots(tile.loc, ap))
        return not self.cf.map[prev_tile_loc.y][prev_tile_loc.x].is_veiled

    def prev_tile_is_lower(self, ap: Point, tile: Tile) -> bool:
        prev_tile_loc = next(path_between_two_dots(tile.loc, ap))
        return self.cf.map[prev_tile_loc.y][prev_tile_loc.x].height < tile.height

    def prev_tiles_lower(self, ap: Point, tile: Tile) -> bool:
        return self.compare_heights(ap, tile, operator.lt)

    def prev_tiles_not_higher(self, ap: Point, tile: Tile) -> bool:
        return self.compare_heights(ap, tile, operator.le)

    def compare_heights(self, ap: Point, tile: Tile, op: t.Callable[[t.Any, t.Any], bool]) -> bool:
        curr_tile_h = tile.height
        while True:
            try:
                prev_tile_loc = next(path_between_two_dots(tile.loc, ap))
            except StopIteration:
                return True

            tile = self.cf.map[prev_tile_loc.y][prev_tile_loc.x]
            if not op(tile.height, curr_tile_h):
                return False

    def unveil_map(self) -> None:
        if self.cf.debug or not self.need_to_unveil:
            return

        actor_p = self.cf.actor_on_map_pos
        actor_tile = self.cf.curr_height = self.cf.map[actor_p.y][actor_p.x]
        actor_h = actor_tile.height
        if actor_tile.is_veiled:
            self.unveil_tile(actor_tile)

        max_vision_y = max_vision_x = self.vision
        if actor_p.y < self.vision:
            max_vision_y = actor_p.y
        if actor_p.x < self.vision:
            max_vision_x = actor_p.x

        for dist in range(1, self.vision + 1):
            min_dist_x = dist if dist <= max_vision_x else max_vision_x
            min_dist_y = dist if dist <= max_vision_y else max_vision_y

            for row in self.cf.map[actor_p.y - min_dist_y:actor_p.y + dist + 1]:
                for tile in row[actor_p.x - min_dist_x:actor_p.x + dist + 1]:
                    if not tile.is_veiled:
                        continue

                    x_offset = abs(tile.x - actor_p.x)
                    y_offset = abs(tile.y - actor_p.y)

                    if x_offset == dist or y_offset == dist:
                        if dist == 1:
                            self.unveil_tile(tile)

                        if dist == 2:
                            self.unveil_tile(tile)

                        if dist == 3:
                            if tile.height <= actor_h and self.prev_tiles_not_higher(actor_p, tile):
                                self.unveil_tile(tile)
                            if tile.height > actor_h and self.prev_tiles_lower(actor_p, tile):
                                self.unveil_tile(tile)

                        if dist == 4:
                            if tile.height == actor_h and x_offset != y_offset:
                                if self.prev_tiles_not_higher(actor_p, tile):
                                    self.unveil_tile(tile)
                            if tile.height < actor_h and self.is_prev_tile_unveiled(actor_p, tile):
                                self.unveil_tile(tile)
                            if tile.height > actor_h and self.prev_tiles_lower(actor_p, tile):
                                self.unveil_tile(tile)

                        if dist == 5:
                            if tile.height < actor_h and self.is_prev_tile_unveiled(actor_p, tile):
                                self.unveil_tile(tile)
                            if tile.height > actor_h and self.prev_tiles_lower(actor_p, tile):
                                self.unveil_tile(tile)

                        if dist == 6:
                            if tile.height < actor_h and self.is_prev_tile_unveiled(actor_p, tile):
                                if x_offset != y_offset:
                                    self.unveil_tile(tile)
                            if tile.height > actor_h and self.prev_tiles_lower(actor_p, tile):
                                self.unveil_tile(tile)

                        if dist == 7:
                            if tile.height > actor_h and self.prev_tiles_lower(actor_p, tile):
                                self.unveil_tile(tile)

                        if dist == 8:
                            if tile.height > actor_h and self.prev_tiles_lower(actor_p, tile):
                                self.unveil_tile(tile)

        self.need_to_unveil = False

    def process_event(self, key: int) -> None:
        if key in MOVE_KEYS:
            if key == KEY_UP:
                self.scroll_v(1)
            if key == KEY_DOWN:
                self.scroll_v(-1)
            if key == KEY_RIGHT:
                self.scroll_h(2 if self.cf.square_tiles else 1)
            if key == KEY_LEFT:
                self.scroll_h(-2 if self.cf.square_tiles else -1)

            self.need_to_unveil = True

    def scroll_v(self, step: int) -> None:
        self.cf.scene_moved = False
        if self.cf.scene_is_most_top:
            if step > 0:
                return

        if self.cf.scene_is_most_bottom:
            if step < 0:
                return

        if self.cf.actor_scene_center_offset.h != 0:
            return

        self.cf.scene_on_map_coords.tl.y -= step
        self.cf.scene_on_map_coords.tr.y -= step
        self.cf.scene_on_map_coords.br.y -= step
        self.cf.scene_on_map_coords.bl.y -= step

        if self.cf.scene_on_map_coords.tl.y <= 0:
            self.cf.scene_is_most_top = True
        else:
            self.cf.scene_is_most_top = False

        if self.cf.scene_on_map_coords.br.y >= self.cf.map_size:
            self.cf.scene_is_most_bottom = True
        else:
            self.cf.scene_is_most_bottom = False

        self.cf.scene_moved = True

    def scroll_h(self, step: int) -> None:
        self.cf.scene_moved = False
        self.cf.short_scroll = False
        horizontal_map_size = self.cf.map_size * 2 if self.cf.square_tiles else self.cf.map_size

        if self.cf.scene_is_most_right:
            if step > 0:
                return

        if self.cf.scene_is_most_left:
            if step < 0:
                return

        if self.cf.square_tiles:
            self.cf.short_scroll = False

            # Scene is about to leave right/left border.
            # If actor scene X offset is -1 or 1 and increasing/decreasing: Short scene scroll should be made.
            # Author move on scene will complete the second half of the step and X offset will become 0.
            # So here we decide that one step of two symbols divides between scene and author, one symbol for each.

            # FOR TESTS: appears on for example scene widths: 57, 61
            # First scroll of scene from left border to map center caught, make it short.
            if self.cf.actor_scene_center_offset.w == -1:
                if step > 0:
                    step -= 1
                self.cf.short_scroll = True

            # FOR TESTS: appears on for example scene widths: 59, 63
            # First scroll of scene from right border to map center caught, make it short.
            elif self.cf.actor_scene_center_offset.w == 1:
                if step < 0:
                    step += 1
                self.cf.short_scroll = True

            elif self.cf.actor_scene_center_offset.w != 0:
                return

            # Scene is about to overstep right/left border: make a short step.
            # Scene steps over right border - decrease step to fit to the border.
            if self.cf.scene_on_map_coords.tr.x + step > horizontal_map_size and step > 0:
                step -= 1
                self.cf.short_scroll = True

            # Scene steps over left border - increase step to fit to the border.
            if self.cf.scene_on_map_coords.tl.x + step < 0:
                step += 1
                self.cf.short_scroll = True
        else:
            if self.cf.actor_scene_center_offset.w != 0:
                return

        self.cf.scene_on_map_coords.tl.x += step
        self.cf.scene_on_map_coords.tr.x += step
        self.cf.scene_on_map_coords.br.x += step
        self.cf.scene_on_map_coords.bl.x += step

        if self.cf.scene_on_map_coords.tr.x >= horizontal_map_size:
            self.cf.scene_is_most_right = True
            self.cf.scene_moved = True
        else:
            self.cf.scene_is_most_right = False

        if self.cf.scene_on_map_coords.tl.x <= 0:
            self.cf.scene_is_most_left = True
            self.cf.scene_moved = True
        else:
            self.cf.scene_is_most_left = False

    def draw_map(self) -> None:
        if self.cf.debug:
            for row in self.cf.map:
                for tile in row:
                    self.pad.print(tile.ch, tile.y, tile.x, cp=tile.color, sq=self.cf.square_tiles)
        else:
            for row in self.cf.map:
                for tile in row:
                    self.pad.print(
                        self.veiled_tile_char if tile.is_veiled else tile.ch,
                        tile.y, tile.x,
                        cp=COLOR_UNVEILED_MAP if tile.is_veiled else tile.color,
                        sq=self.cf.square_tiles,
                    )

        self.refresh()

    def refresh(self) -> None:
        self.pad.noutrefresh(
            self.cf.scene_on_map_coords.tl.y, self.cf.scene_on_map_coords.tl.x,
            0, 0,
            self.cf.scene_pad_coords.br.y, self.cf.scene_pad_coords.br.x,
        )

    def do_animation(self) -> None:
        self.unveil_map()
