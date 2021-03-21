from colors import A_BOLD, COLOR_ACTOR
from controllers.base import BaseController
from dto import Point
from storage import RuntimeStorage
from tools import Pad


class ActorController(BaseController):
    def __init__(self, pad: Pad, storage: RuntimeStorage) -> None:
        super().__init__(pad, storage)
        self.draw_actor()

    def get_screen_center(self) -> Point:
        rx = self.st.scene_pad_coords.tr.x
        lx = self.st.scene_pad_coords.tl.x
        ty = self.st.scene_pad_coords.tl.y
        by = self.st.scene_pad_coords.bl.y

        sc = Point(
            x=(rx - lx) // 2 + (rx - lx) % 2,
            y=(by - ty) // 2 + (by - ty) % 2,
        )

        if self.st.square_tiles:
            sc.x -= 1

        return sc

    def process_event(self, key: int) -> None:
        if key in self.st.move_keys:
            if key == self.st.key_up:
                self.move_v(1)
            if key == self.st.key_down:
                self.move_v(-1)
            if key == self.st.key_right:
                self.move_h(2 if self.st.square_tiles else 1)
            if key == self.st.key_left:
                self.move_h(-2 if self.st.square_tiles else -1)

            self.draw_actor()

    def move_v(self, step: int) -> None:
        if not any((self.st.screen_is_most_top, self.st.screen_is_most_bottom)):
            return

        screen_center = self.get_screen_center()
        if self.st.screen_is_most_top and not self.st.scene_moved:
            if step > 0:
                if self.st.actor_screen_center_offset.h + screen_center.y > 0:
                    self.st.actor_screen_center_offset.h -= 1
            else:
                if self.st.actor_screen_center_offset.h < 0:
                    self.st.actor_screen_center_offset.h += 1

        elif self.st.screen_is_most_bottom and not self.st.scene_moved:
            if step < 0:
                if self.st.actor_screen_center_offset.h - (self.st.scene_pad_coords.br.y - screen_center.y) < 0:
                    self.st.actor_screen_center_offset.h += 1
            else:
                if self.st.actor_screen_center_offset.h > 0:
                    self.st.actor_screen_center_offset.h -= 1

    def move_h(self, step: int) -> None:
        if not any((self.st.screen_is_most_right, self.st.screen_is_most_left, self.st.short_scroll)):
            return

        screen_center = self.get_screen_center()

        # Happens only in square tile mode when screen size is odd.
        # Since map size is always even - short screen move happens and we need to adjust actor step on screen.
        if self.st.short_scroll:
            if step > 0:
                step -= 1
            else:
                step += 1
            self.st.actor_screen_center_offset.w += step
        else:
            if self.st.screen_is_most_right:
                if step > 0 and not self.st.scene_moved:
                    if self.st.actor_screen_center_offset.w + screen_center.x + step <= self.st.scene_pad_coords.tr.x:
                        self.st.actor_screen_center_offset.w += step
                else:
                    if self.st.actor_screen_center_offset.w > 0:
                        self.st.actor_screen_center_offset.w += step
            if self.st.screen_is_most_left:
                if step < 0 and not self.st.scene_moved:
                    if self.st.actor_screen_center_offset.w + step + screen_center.x >= 0:
                        self.st.actor_screen_center_offset.w += step
                    elif self.st.actor_screen_center_offset.w + step + 1 + screen_center.x >= 0:
                        self.st.actor_screen_center_offset.w += step + 1
                else:
                    if self.st.actor_screen_center_offset.w < 0:
                        self.st.actor_screen_center_offset.w += step

    def draw_actor(self) -> None:
        self.update_actor_location()
        self._pad.print('+', cp=COLOR_ACTOR, attr=A_BOLD, sq=self.st.square_tiles)

    def get_actor_on_screen_coords(self) -> Point:
        screen_center = self.get_screen_center()

        return Point(
            y=screen_center.y + self.st.actor_screen_center_offset.h,
            x=screen_center.x + self.st.actor_screen_center_offset.w,
        )

    def update_actor_location(self) -> None:
        actor_on_screen_coords = self.get_actor_on_screen_coords()

        actor_location_x = actor_on_screen_coords.x + self.st.scene_on_map_coords.tl.x
        if self.st.square_tiles:
            actor_location_x = actor_location_x // 2

        actor_on_map_coords = Point(
            x=actor_location_x,
            y=actor_on_screen_coords.y + self.st.scene_on_map_coords.tl.y,
        )
        self.st.actor_on_map_pos = actor_on_map_coords

    def refresh(self) -> None:
        actor_on_screen = self.get_actor_on_screen_coords()

        self._pad.noutrefresh(
            0, 0,
            actor_on_screen.y, actor_on_screen.x,
            actor_on_screen.y, actor_on_screen.x + self._pad.width,
        )

    def do_animation(self) -> None:
        self.draw_actor()
