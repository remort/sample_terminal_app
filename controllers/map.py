import logging

from colors import COLOR_UNVEILED_MAP
from controllers.base import BaseController
from dto import Coordinates, Point, Tile
from pad_wrapper import Pad
from storage import RuntimeStorage

log = logging.getLogger(__name__)


class MapController(BaseController):
    def __init__(self, pad: Pad, storage: RuntimeStorage) -> None:
        super().__init__(pad, storage)

        self.calculate_initial_scene_position()
        self.veiled_tile_char: str = '.'
        self.need_to_unveil = True
        self.vision = 8

        self.draw_surface()

    def _get_tile(self, line: int, col: int) -> Tile:
        if self.st.square_tiles:
            col = col // 2

        return self.st.map[line][col]

    def calculate_initial_scene_position(self) -> None:
        map_edge = self.st.map_size
        horizontal_map_size = self.st.map_size * 2 if self.st.square_tiles else self.st.map_size

        lx = (horizontal_map_size - self.st.scene_size.w) // 2 + (horizontal_map_size - self.st.scene_size.w) % 2
        rx = lx + self.st.scene_size.w
        ty = (map_edge - self.st.scene_size.h) // 2 + (map_edge - self.st.scene_size.h) % 2
        by = ty + self.st.scene_size.h

        self.st.scene_on_map_coords = Coordinates(
            tl=Point(x=lx, y=ty), tr=Point(x=rx, y=ty), br=Point(x=rx, y=by), bl=Point(x=lx, y=by)
        )

    def unveil_tile(self, tile: Tile) -> None:
        tile.is_veiled = False
        self.pad.addch(tile.ch, tile.y, tile.x, cp=tile.color, sq=self.st.square_tiles)

    def get_previous_tile(self, ap: Point, tile: Tile) -> Tile:
        prev_tile_coords = Point(x=tile.x, y=tile.y)

        if tile.x > ap.x:
            prev_tile_coords.x -= 2 if self.st.square_tiles else 1
        if tile.x < ap.x:
            prev_tile_coords.x += 2 if self.st.square_tiles else 1
        if tile.y > ap.y:
            prev_tile_coords.y -= 1
        if tile.y < ap.y:
            prev_tile_coords.y += 1

        return self._get_tile(prev_tile_coords.y, prev_tile_coords.x)

    def is_prev_tile_unveiled(self, ap: Point, tile: Tile) -> bool:
        prev_tile = self.get_previous_tile(ap, tile)
        return not prev_tile.is_veiled

    def is_prev_tile_lower(self, ap: Point, tile: Tile) -> bool:
        prev_tile = self.get_previous_tile(ap, tile)
        return prev_tile.height < tile.height

    def are_prev_tiles_lower(self, ap: Point, tile: Tile, dist: int) -> bool:
        curr_tile_h = tile.height
        for d in range(1, dist):
            tile = self.get_previous_tile(ap, tile)
            if tile.height >= curr_tile_h:
                return False
        return True

    def unveil_map(self) -> None:
        if self.st.debug or not self.need_to_unveil:
            return

        actor_p = self.st.actor_on_map_pos
        actor_tile = self.st.curr_height = self.st.map[self.st.actor_on_map_pos.y][self.st.actor_on_map_pos.x]
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

            for row in self.st.map[actor_p.y - min_dist_y:actor_p.y + dist + 1]:
                for tile in row[actor_p.x - min_dist_x:actor_p.x + dist + 1]:
                    x_offset = abs(tile.x - actor_p.x)
                    y_offset = abs(tile.y - actor_p.y)

                    if x_offset == dist or y_offset == dist:
                        if dist == 1:
                            self.unveil_tile(tile)

                        if dist == 2:
                            self.unveil_tile(tile)

                        if dist == 3:
                            if tile.height <= actor_h:
                                self.unveil_tile(tile)
                            if tile.height > actor_h and self.are_prev_tiles_lower(actor_p, tile, dist):
                                self.unveil_tile(tile)

                        if dist == 4:
                            if tile.height == actor_h:
                                if x_offset != y_offset:
                                    self.unveil_tile(tile)
                            if tile.height < actor_h and self.is_prev_tile_unveiled(actor_p, tile):
                                self.unveil_tile(tile)
                            if tile.height > actor_h and self.are_prev_tiles_lower(actor_p, tile, dist):
                                self.unveil_tile(tile)

                        if dist == 5:
                            if tile.height < actor_h and self.is_prev_tile_unveiled(actor_p, tile):
                                self.unveil_tile(tile)
                            if tile.height > actor_h and self.are_prev_tiles_lower(actor_p, tile, dist):
                                self.unveil_tile(tile)

                        if dist == 6:
                            if tile.height < actor_h and self.is_prev_tile_unveiled(actor_p, tile):
                                if x_offset != y_offset:
                                    self.unveil_tile(tile)
                            if tile.height > actor_h and self.are_prev_tiles_lower(actor_p, tile, dist):
                                self.unveil_tile(tile)

                        if dist == 7:
                            if tile.height > actor_h and self.are_prev_tiles_lower(actor_p, tile, dist):
                                self.unveil_tile(tile)

                        if dist == 8:
                            if tile.height > actor_h and self.are_prev_tiles_lower(actor_p, tile, dist):
                                self.unveil_tile(tile)

        self.need_to_unveil = False

    def process_event(self, key: int) -> None:
        if key in self.st.move_keys:
            if key == self.st.key_up:
                self.scroll_v(1)
            if key == self.st.key_down:
                self.scroll_v(-1)
            if key == self.st.key_right:
                self.scroll_h(2 if self.st.square_tiles else 1)
            if key == self.st.key_left:
                self.scroll_h(-2 if self.st.square_tiles else -1)

            self.need_to_unveil = True

    def scroll_v(self, step: int) -> None:
        self.st.scene_moved = False
        if self.st.scene_is_most_top:
            if step > 0:
                return

        if self.st.scene_is_most_bottom:
            if step < 0:
                return

        if self.st.actor_scene_center_offset.h != 0:
            return

        self.st.scene_on_map_coords.tl.y -= step
        self.st.scene_on_map_coords.tr.y -= step
        self.st.scene_on_map_coords.br.y -= step
        self.st.scene_on_map_coords.bl.y -= step

        if self.st.scene_on_map_coords.tl.y <= 0:
            self.st.scene_is_most_top = True
        else:
            self.st.scene_is_most_top = False

        if self.st.scene_on_map_coords.br.y >= self.st.map_size:
            self.st.scene_is_most_bottom = True
        else:
            self.st.scene_is_most_bottom = False

        self.st.scene_moved = True

    def scroll_h(self, step: int) -> None:
        self.st.scene_moved = False
        self.st.short_scroll = False
        horizontal_map_size = self.st.map_size * 2 if self.st.square_tiles else self.st.map_size

        if self.st.scene_is_most_right:
            if step > 0:
                return

        if self.st.scene_is_most_left:
            if step < 0:
                return

        if self.st.square_tiles:
            self.st.short_scroll = False

            # Scene is about to leave right/left border.
            # If actor scene X offset is -1 or 1 and increasing/decreasing: Short scene scroll should be made.
            # Author move on scene will complete the second half of the step and X offset will become 0.
            # So here we decide that one step of two symbols divides between scene and author, one symbol for each.

            # FOR TESTS: appears on for example scene widths: 57, 61
            # First scroll of scene from left border to map center caught, make it short.
            if self.st.actor_scene_center_offset.w == -1:
                if step > 0:
                    step -= 1
                self.st.short_scroll = True

            # FOR TESTS: appears on for example scene widths: 59, 63
            # First scroll of scene from right border to map center caught, make it short.
            elif self.st.actor_scene_center_offset.w == 1:
                if step < 0:
                    step += 1
                self.st.short_scroll = True

            elif self.st.actor_scene_center_offset.w != 0:
                return

            # Scene is about to overstep right/left border: make a short step.
            # Scene steps over right border - decrease step to fit to the border.
            if self.st.scene_on_map_coords.tr.x + step > horizontal_map_size and step > 0:
                step -= 1
                self.st.short_scroll = True

            # Scene steps over left border - increase step to fit to the border.
            if self.st.scene_on_map_coords.tl.x + step < 0:
                step += 1
                self.st.short_scroll = True
        else:
            if self.st.actor_scene_center_offset.w != 0:
                return

        self.st.scene_on_map_coords.tl.x += step
        self.st.scene_on_map_coords.tr.x += step
        self.st.scene_on_map_coords.br.x += step
        self.st.scene_on_map_coords.bl.x += step

        if self.st.scene_on_map_coords.tr.x >= horizontal_map_size:
            self.st.scene_is_most_right = True
            self.st.scene_moved = True
        else:
            self.st.scene_is_most_right = False

        if self.st.scene_on_map_coords.tl.x <= 0:
            self.st.scene_is_most_left = True
            self.st.scene_moved = True
        else:
            self.st.scene_is_most_left = False

    def draw_surface(self) -> None:
        if self.st.debug:
            for row in self.st.map:
                for tile in row:
                    self.pad.print(tile.ch, tile.y, tile.x, cp=tile.color, sq=self.st.square_tiles)
        else:
            for row in self.st.map:
                for tile in row:
                    self.pad.print(
                        self.veiled_tile_char,
                        tile.y, tile.x,
                        cp=COLOR_UNVEILED_MAP,
                        sq=self.st.square_tiles,
                    )

        self.refresh()

    def refresh(self) -> None:
        self.pad.noutrefresh(
            self.st.scene_on_map_coords.tl.y, self.st.scene_on_map_coords.tl.x,
            0, 0,
            self.st.scene_pad_coords.br.y, self.st.scene_pad_coords.br.x,
        )

    def do_animation(self) -> None:
        self.unveil_map()
