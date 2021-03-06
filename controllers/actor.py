import curses

from colors import COLOR_ACTOR
from controllers.base import BaseController
from dto import Point, Size
from storage import RuntimeStorage


class ActorControler(BaseController):
    def __init__(self, pad, storage: RuntimeStorage):
        super().__init__(pad, storage)

        self.st.actor_screen_center_offset = Size(w=0, h=0)
        self.draw_actor()

    def get_screen_center(self):
        rx = self.st.scene_on_map_coords.tr.x
        lx = self.st.scene_on_map_coords.tl.x
        ty = self.st.scene_on_map_coords.tl.y
        by = self.st.scene_on_map_coords.bl.y

        return Point(
            x=(rx - lx) // 2 + (rx - lx) % 2,
            y=(by - ty) // 2 + (by - ty) % 2,
        )

    def process_event(self, key):
        if key == curses.KEY_UP:
            self.move_v(1)
        if key == curses.KEY_DOWN:
            self.move_v(-1)
        if key == curses.KEY_RIGHT:
            self.move_h(1)
        if key == curses.KEY_LEFT:
            self.move_h(-1)

    def move_v(self, step):
        if not self.st.screen_is_most_top and not self.st.screen_is_most_bottom:
            self.draw_actor()
            return

        screen_center = self.get_screen_center()
        if self.st.screen_is_most_top:

            if step > 0:
                if self.st.actor_screen_center_offset.h + screen_center.y > 0:
                    self.st.actor_screen_center_offset.h -= 1
            else:
                if self.st.actor_screen_center_offset.h < 0:
                    self.st.actor_screen_center_offset.h += 1

        elif self.st.screen_is_most_bottom:
            if step < 0:
                if self.st.actor_screen_center_offset.h - (self.st.scene_coords.br.y - screen_center.y) < 0:
                    self.st.actor_screen_center_offset.h += 1
            else:
                if self.st.actor_screen_center_offset.h > 0:
                    self.st.actor_screen_center_offset.h -= 1

        self.draw_actor()

    def move_h(self, step):
        if not self.st.screen_is_most_right and not self.st.screen_is_most_left:
            self.draw_actor()
            return

        screen_center = self.get_screen_center()
        if self.st.screen_is_most_right:
            if step > 0:
                if self.st.actor_screen_center_offset.w - (self.st.scene_coords.br.x - screen_center.x) < 0:
                    self.st.actor_screen_center_offset.w += 1
            else:
                if self.st.actor_screen_center_offset.w > 0:
                    self.st.actor_screen_center_offset.w -= 1
        elif self.st.screen_is_most_left:
            if step < 0:
                if self.st.actor_screen_center_offset.w + screen_center.x > 0:
                    self.st.actor_screen_center_offset.w -= 1
            else:
                if self.st.actor_screen_center_offset.w < 0:
                    self.st.actor_screen_center_offset.w += 1

        self.draw_actor()

    def draw_actor(self):
        self.update_actor_location()
        self._pad.print('Ѫ', cpn=COLOR_ACTOR, attr=curses.A_BOLD)
        self.refresh()

    def get_actor_on_screen_coords(self):
        screen_center = self.get_screen_center()

        return Point(
            y=screen_center.y + self.st.actor_screen_center_offset.h,
            x=screen_center.x + self.st.actor_screen_center_offset.w,
        )

    def update_actor_location(self):
        actor_on_screen_coords = self.get_actor_on_screen_coords()
        actor_on_map_coords = Point(
            x=actor_on_screen_coords.x + self.st.scene_on_map_coords.tl.x,
            y=actor_on_screen_coords.y + self.st.scene_on_map_coords.tl.y,
        )
        self.st.actor_location = actor_on_map_coords

    def refresh(self):
        actor_on_screen = self.get_actor_on_screen_coords()

        self._pad.noutrefresh(
            0, 0,
            actor_on_screen.y, actor_on_screen.x,
            actor_on_screen.y, actor_on_screen.x,
        )

    def do_animation(self):
        pass
