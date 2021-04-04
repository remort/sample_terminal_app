import logging

from colors import A_BOLD, COLOR_ACTOR
from configuration.main import Configuration
from constants import KEY_DOWN, KEY_LEFT, KEY_RIGHT, KEY_UP, MOVE_KEYS
from controllers.base import BaseController
from dto import Point
from pad_wrapper import Pad

log = logging.getLogger(__name__)


class ActorController(BaseController):
    def __init__(self, pad: Pad, configuration: Configuration) -> None:
        super().__init__(pad, configuration)
        self.draw_actor()

    def get_scene_center(self) -> Point:
        rx = self.cf.scene_pad_coords.tr.x
        lx = self.cf.scene_pad_coords.tl.x
        ty = self.cf.scene_pad_coords.tl.y
        by = self.cf.scene_pad_coords.bl.y

        sc = Point(
            x=(rx - lx) // 2 + (rx - lx) % 2,
            y=(by - ty) // 2 + (by - ty) % 2,
        )

        if self.cf.square_tiles:
            sc.x -= 1

        return sc

    def process_event(self, key: int) -> None:
        if key in MOVE_KEYS:
            if key == KEY_UP:
                self.move_v(1)
            if key == KEY_DOWN:
                self.move_v(-1)
            if key == KEY_RIGHT:
                self.move_h(2 if self.cf.square_tiles else 1)
            if key == KEY_LEFT:
                self.move_h(-2 if self.cf.square_tiles else -1)

            self.draw_actor()

    def move_v(self, step: int) -> None:
        if not any((self.cf.scene_is_most_top, self.cf.scene_is_most_bottom)):
            return

        scene_center = self.get_scene_center()
        if self.cf.scene_is_most_top and not self.cf.scene_moved:
            if step > 0:
                if self.cf.actor_scene_center_offset.h + scene_center.y > 0:
                    self.cf.actor_scene_center_offset.h -= 1
            else:
                if self.cf.actor_scene_center_offset.h < 0:
                    self.cf.actor_scene_center_offset.h += 1

        elif self.cf.scene_is_most_bottom and not self.cf.scene_moved:
            if step < 0:
                if self.cf.actor_scene_center_offset.h - (self.cf.scene_pad_coords.br.y - scene_center.y) < 0:
                    self.cf.actor_scene_center_offset.h += 1
            else:
                if self.cf.actor_scene_center_offset.h > 0:
                    self.cf.actor_scene_center_offset.h -= 1

    def move_h(self, step: int) -> None:
        if not any((self.cf.scene_is_most_right, self.cf.scene_is_most_left, self.cf.short_scroll)):
            return

        scene_center = self.get_scene_center()

        # Happens only in square tile mode when scene size is odd.
        # Since map size is always even - short scene move happens and we need to adjust actor step on scene.
        if self.cf.short_scroll:
            if step > 0:
                step -= 1
                self.cf.actor_scene_center_offset.w += step
            else:
                step += 1
                self.cf.actor_scene_center_offset.w += step
        else:
            if self.cf.scene_is_most_right:
                if step > 0 and not self.cf.scene_moved:
                    if self.cf.actor_scene_center_offset.w + scene_center.x + step <= self.cf.scene_pad_coords.tr.x:
                        self.cf.actor_scene_center_offset.w += step
                else:
                    if self.cf.actor_scene_center_offset.w > 0:
                        self.cf.actor_scene_center_offset.w += step
            if self.cf.scene_is_most_left:
                if step < 0 and not self.cf.scene_moved:
                    if self.cf.actor_scene_center_offset.w + step + scene_center.x >= 0:
                        self.cf.actor_scene_center_offset.w += step
                    elif self.cf.actor_scene_center_offset.w + step + 1 + scene_center.x >= 0:
                        self.cf.actor_scene_center_offset.w += step + 1
                else:
                    if self.cf.actor_scene_center_offset.w < 0:
                        self.cf.actor_scene_center_offset.w += step

    def draw_actor(self) -> None:
        if self.update_actor_location():
            self.pad.print('+', cp=COLOR_ACTOR, attr=A_BOLD, sq=self.cf.square_tiles)

    def get_actor_on_scene_coords(self) -> Point:
        scene_center = self.get_scene_center()

        return Point(
            y=scene_center.y + self.cf.actor_scene_center_offset.h,
            x=scene_center.x + self.cf.actor_scene_center_offset.w,
        )

    def update_actor_location(self) -> bool:
        actor_on_scene_coords = self.get_actor_on_scene_coords()

        actor_location_x = actor_on_scene_coords.x + self.cf.scene_on_map_coords.tl.x
        if self.cf.square_tiles:
            actor_location_x = actor_location_x // 2

        actor_on_map_coords = Point(
            x=actor_location_x,
            y=actor_on_scene_coords.y + self.cf.scene_on_map_coords.tl.y,
        )

        if self.cf.actor_on_map_pos != actor_on_map_coords:
            self.cf.actor_on_map_pos = actor_on_map_coords
            return True

        return False

    def refresh(self) -> None:
        actor_on_scene = self.get_actor_on_scene_coords()

        self.pad.noutrefresh(
            0, 0,
            actor_on_scene.y, actor_on_scene.x,
            actor_on_scene.y, actor_on_scene.x + self.pad.width,
        )

    def do_animation(self) -> None:
        self.draw_actor()
