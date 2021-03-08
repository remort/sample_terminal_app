from controllers.base import BaseController
from dto import Coordinates, Point, Size, Tile
from storage import RuntimeStorage, MapType
from utils import make_coordinates_by_size
from colors import COLOR_UNVEILED_MAP


class MapController(BaseController):
    def __init__(self, pad, storage: RuntimeStorage, scene_size: Size) -> None:
        super().__init__(pad, storage)

        self.st.scene_size = scene_size
        self.st.scene_coords = make_coordinates_by_size(scene_size)

        self.st.map = self._generate_map_from_surface()

        self.calculate_initial_screen_position()
        self.unveiled_tile_char: str = '.'
        self.vision = 6

        self.draw_surface()

    def _generate_map_from_surface(self) -> MapType:
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

    def unveil_tile(self, tile: Tile) -> None:
        tile.is_veiled = False
        self._pad.addch(tile.ch, tile.y, tile.x, cp=tile.color)

    def is_prev_tile_unveiled(self, ap: Point, tile: Tile) -> bool:
        prev_tile_coords = Point(x=tile.x, y=tile.y)

        if tile.x > ap.x:
            prev_tile_coords.x -= 1
        if tile.x < ap.x:
            prev_tile_coords.x += 1
        if tile.y > ap.y:
            prev_tile_coords.y -= 1
        if tile.y < ap.y:
            prev_tile_coords.y += 1

        return not self.st.map[prev_tile_coords.y][prev_tile_coords.x].is_veiled

    def unveil_map(self) -> None:
        if self.st.debug:
            return

        actor_p = self.st.actor_location
        curr_h = self.st.curr_height = self.st.map[self.st.actor_location.y][self.st.actor_location.x].height

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
                            if tile.height == curr_h:
                                self.unveil_tile(tile)
                            if tile.height < curr_h and self.is_prev_tile_unveiled(actor_p, tile):
                                self.unveil_tile(tile)
                            if tile.height == curr_h + 1:
                                self.unveil_tile(tile)

                        if dist == 4:
                            if tile.height == curr_h:
                                if x_offset != y_offset:
                                    self.unveil_tile(tile)
                            if tile.height < curr_h and self.is_prev_tile_unveiled(actor_p, tile):
                                self.unveil_tile(tile)

                        if dist == 5:
                            if tile.height < curr_h and self.is_prev_tile_unveiled(actor_p, tile):
                                self.unveil_tile(tile)

                        if dist == 6:
                            if tile.height < curr_h and self.is_prev_tile_unveiled(actor_p, tile):
                                if x_offset != y_offset:
                                    self.unveil_tile(tile)

    def process_event(self, key: int) -> None:
        if key in self.st.move_keys:
            if key == self.st.key_up:
                self.scroll_v(1)
            if key == self.st.key_down:
                self.scroll_v(-1)
            if key == self.st.key_right:
                self.scroll_h(1)
            if key == self.st.key_left:
                self.scroll_h(-1)

    def calculate_initial_screen_position(self) -> None:
        if self.st.scene_size.w > self.st.map_size or self.st.scene_size.h > self.st.map_size:
            raise ValueError(
                'Screen ({}x{}) can not be larger than a map: {}.'.format(
                    self.st.scene_size.w,
                    self.st.scene_size.h,
                    self.st.map_size,
                ))
        else:
            map_edge = self.st.map_size - 1
            lx = (map_edge - self.st.scene_size.w) // 2 + (map_edge - self.st.scene_size.w) % 2
            rx = lx + self.st.scene_size.w
            ty = (map_edge - self.st.scene_size.h) // 2 + (map_edge - self.st.scene_size.h) % 2
            by = ty + self.st.scene_size.h

            self.st.scene_on_map_coords = Coordinates(
                tl=Point(x=lx, y=ty), tr=Point(x=rx, y=ty), br=Point(x=rx, y=by), bl=Point(x=lx, y=by)
            )

    def scroll_v(self, step: int) -> None:
        if self.st.scene_on_map_coords.tl.y <= 0:
            if step > 0:
                self.st.screen_is_most_top = True
                return

        if self.st.scene_on_map_coords.br.y >= self.st.map_size:
            if step < 0:
                self.st.screen_is_most_bottom = True
                return

        if self.st.actor_screen_center_offset.h != 0:
            return

        self.st.scene_on_map_coords.tl.y -= step
        self.st.scene_on_map_coords.tr.y -= step
        self.st.scene_on_map_coords.br.y -= step
        self.st.scene_on_map_coords.bl.y -= step

        self.st.screen_is_most_top = False
        self.st.screen_is_most_bottom = False

    def scroll_h(self, step: int) -> None:
        if self.st.scene_on_map_coords.tr.x >= self.st.map_size:
            if step > 0:
                self.st.screen_is_most_right = True
                return

        if self.st.scene_on_map_coords.tl.x <= 0:
            if step < 0:
                self.st.screen_is_most_left = True
                return

        if self.st.actor_screen_center_offset.w != 0:
            return

        self.st.scene_on_map_coords.tl.x += step
        self.st.scene_on_map_coords.tr.x += step
        self.st.scene_on_map_coords.br.x += step
        self.st.scene_on_map_coords.bl.x += step

        self.st.screen_is_most_right = False
        self.st.screen_is_most_left = False

    def draw_surface(self) -> None:
        if self.st.debug:
            for row in self.st.map:
                for tile in row:
                    self._pad.print(tile.ch, tile.y, tile.x, cp=tile.color)
        else:
            for row in self.st.map:
                for tile in row:
                    self._pad.print(self.unveiled_tile_char, tile.y, tile.x, cp=COLOR_UNVEILED_MAP)

        self.refresh()

    def refresh(self) -> None:
        self._pad.noutrefresh(
            self.st.scene_on_map_coords.tl.y, self.st.scene_on_map_coords.tl.x,
            0, 0,
            self.st.scene_coords.br.y, self.st.scene_coords.br.x,
        )

    def do_animation(self) -> None:
        self.unveil_map()
