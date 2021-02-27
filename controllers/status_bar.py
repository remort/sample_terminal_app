import curses

from colors import COLOR_STATUS_BAR_MESSAGES, COLOR_STATUS_BAR_STATS
from storage import RuntimeStorage


class StatusBarController:
    def __init__(self, pad, storage: RuntimeStorage):
        self._pad = pad
        self.st = storage
        self.do_animation()

        self._pad.pad.bkgd(' ', curses.color_pair(COLOR_STATUS_BAR_STATS))

    def print_status(self):
        screen_size = f'{self.st.scene_size.h}x{self.st.scene_size.w}'
        map_size = f'{self.st.map_size.h}x{self.st.map_size.w}'
        screen_most_point = f'{self.st.scene_coords.br.y},{self.st.scene_coords.br.x}'

        actor_location = f'{self.st.actor_location.y}x{self.st.actor_location.x}'

        bump = ''
        if self.st.screen_is_most_top and self.st.actor_location.y == 0:
            bump = 'Top border reached.'
        if self.st.screen_is_most_bottom and self.st.actor_location.y == self.st.map_coords.br.y:
            bump = 'Bottom border reached.'
        if self.st.screen_is_most_left and self.st.actor_location.x == 0:
            bump = 'Left border reached.'
        if self.st.screen_is_most_right and self.st.actor_location.x == self.st.map_coords.br.x:
            bump = 'Right border reached.'

        last_message = ''
        messages = len(self.st.messages)
        if messages > 1:
            last_message = self.st.messages.pop()
            messages -= 1

        location_string = f'{actor_location} '
        status_line = f'{map_size}|{screen_size}|{screen_most_point}|{bump}'
        message_line = f'{last_message}|{messages}'
        message_line_start = self.st.scene_coords.br.x - len(message_line)

        self._pad.print(location_string, attr=curses.A_BOLD, cpn=COLOR_STATUS_BAR_STATS)
        self._pad.print(status_line, 0, len(location_string), attr=curses.A_DIM, cpn=COLOR_STATUS_BAR_STATS)
        self._pad.print(message_line, 0, message_line_start, n=5, attr=curses.A_BOLD, cpn=COLOR_STATUS_BAR_MESSAGES)

    def process_event(self, key):
        pass

    def do_animation(self):
        self._pad.erase()
        self.print_status()
        self._pad.noutrefresh(
            0, 0,
            self.st.scene_coords.br.y + 1, 0,
            self.st.scene_coords.br.y + 1, self.st.scene_coords.br.x,
        )
