import logging

from colors import A_BOLD, COLOR_ACTOR
from controllers.base import BaseController
from dto import Point
from storage import RuntimeStorage
from tools import Pad

log = logging.getLogger(__name__)


class ActorController(BaseController):
    def __init__(self, pad: Pad, storage: RuntimeStorage) -> None:
        super().__init__(pad, storage)
        self.draw_actor()

    def get_scene_center(self) -> Point:
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
        if not any((self.st.scene_is_most_top, self.st.scene_is_most_bottom)):
            return

        scene_center = self.get_scene_center()
        if self.st.scene_is_most_top and not self.st.scene_moved:
            if step > 0:
                if self.st.actor_scene_center_offset.h + scene_center.y > 0:
                    self.st.actor_scene_center_offset.h -= 1
            else:
                if self.st.actor_scene_center_offset.h < 0:
                    self.st.actor_scene_center_offset.h += 1

        elif self.st.scene_is_most_bottom and not self.st.scene_moved:
            if step < 0:
                if self.st.actor_scene_center_offset.h - (self.st.scene_pad_coords.br.y - scene_center.y) < 0:
                    self.st.actor_scene_center_offset.h += 1
            else:
                if self.st.actor_scene_center_offset.h > 0:
                    self.st.actor_scene_center_offset.h -= 1

    def move_h(self, step: int) -> None:
        if not any((self.st.scene_is_most_right, self.st.scene_is_most_left, self.st.short_scroll)):
            return

        scene_center = self.get_scene_center()

        # Happens only in square tile mode when scene size is odd.
        # Since map size is always even - short scene move happens and we need to adjust actor step on scene.
        if self.st.short_scroll:
            if step > 0:
                step -= 1
                self.st.actor_scene_center_offset.w += step
            else:
                step += 1
                self.st.actor_scene_center_offset.w += step
        else:
            if self.st.scene_is_most_right:
                if step > 0 and not self.st.scene_moved:
                    if self.st.actor_scene_center_offset.w + scene_center.x + step <= self.st.scene_pad_coords.tr.x:
                        self.st.actor_scene_center_offset.w += step
                else:
                    if self.st.actor_scene_center_offset.w > 0:
                        self.st.actor_scene_center_offset.w += step
            if self.st.scene_is_most_left:
                if step < 0 and not self.st.scene_moved:
                    if self.st.actor_scene_center_offset.w + step + scene_center.x >= 0:
                        self.st.actor_scene_center_offset.w += step
                    elif self.st.actor_scene_center_offset.w + step + 1 + scene_center.x >= 0:
                        self.st.actor_scene_center_offset.w += step + 1
                else:
                    if self.st.actor_scene_center_offset.w < 0:
                        self.st.actor_scene_center_offset.w += step

    def draw_actor(self) -> None:
        if self.update_actor_location():
            self._pad.print('+', cp=COLOR_ACTOR, attr=A_BOLD, sq=self.st.square_tiles)

    def get_actor_on_scene_coords(self) -> Point:
        scene_center = self.get_scene_center()

        return Point(
            y=scene_center.y + self.st.actor_scene_center_offset.h,
            x=scene_center.x + self.st.actor_scene_center_offset.w,
        )

    def update_actor_location(self) -> bool:
        actor_on_scene_coords = self.get_actor_on_scene_coords()

        actor_location_x = actor_on_scene_coords.x + self.st.scene_on_map_coords.tl.x
        if self.st.square_tiles:
            actor_location_x = actor_location_x // 2

        actor_on_map_coords = Point(
            x=actor_location_x,
            y=actor_on_scene_coords.y + self.st.scene_on_map_coords.tl.y,
        )

        if self.st.actor_on_map_pos != actor_on_map_coords:
            self.st.actor_on_map_pos = actor_on_map_coords
            return True

        return False

    def refresh(self) -> None:
        actor_on_scene = self.get_actor_on_scene_coords()

        self._pad.noutrefresh(
            0, 0,
            actor_on_scene.y, actor_on_scene.x,
            actor_on_scene.y, actor_on_scene.x + self._pad.width,
        )

    def do_animation(self) -> None:
        self.draw_actor()
