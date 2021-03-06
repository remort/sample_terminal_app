import curses

from colors import COLOR_ACTOR
from dto import Point
from storage import RuntimeStorage


class ActorControler:
    def __init__(self, pad, storage: RuntimeStorage):
        self._pad = pad
        self.st = storage
        self.st.actor_screen_center_offset = Point(x=0, y=0)

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
                if self.st.actor_screen_center_offset.y + screen_center.y > 0:
                    self.st.actor_screen_center_offset.y -= 1
            else:
                if self.st.actor_screen_center_offset.y < 0:
                    self.st.actor_screen_center_offset.y += 1

        elif self.st.screen_is_most_bottom:
            if step < 0:
                if self.st.actor_screen_center_offset.y - (self.st.scene_coords.br.y - screen_center.y) < 0:
                    self.st.actor_screen_center_offset.y += 1
            else:
                if self.st.actor_screen_center_offset.y > 0:
                    self.st.actor_screen_center_offset.y -= 1

        self.draw_actor()

    def move_h(self, step):
        if not self.st.screen_is_most_right and not self.st.screen_is_most_left:
            self.draw_actor()
            return

        screen_center = self.get_screen_center()
        if self.st.screen_is_most_right:
            if step > 0:
                if self.st.actor_screen_center_offset.x - (self.st.scene_coords.br.x - screen_center.x) < 0:
                    self.st.actor_screen_center_offset.x += 1
            else:
                if self.st.actor_screen_center_offset.x > 0:
                    self.st.actor_screen_center_offset.x -= 1
        elif self.st.screen_is_most_left:
            if step < 0:
                if self.st.actor_screen_center_offset.x + screen_center.x > 0:
                    self.st.actor_screen_center_offset.x -= 1
            else:
                if self.st.actor_screen_center_offset.x < 0:
                    self.st.actor_screen_center_offset.x += 1

        self.draw_actor()

    def draw_actor(self):
        self.update_actor_location()
        self._pad.print('Ѫ', cpn=COLOR_ACTOR, attr=curses.A_BOLD)
        self.refresh()

    def get_actor_on_screen_coords(self):
        screen_center = self.get_screen_center()

        return Point(
            y=screen_center.y + self.st.actor_screen_center_offset.y,
            x=screen_center.x + self.st.actor_screen_center_offset.x,
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
