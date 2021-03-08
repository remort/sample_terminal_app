from colors import A_BOLD, COLOR_STATUS_BAR_MESSAGES, COLOR_STATUS_BAR_STATS
from controllers.base import BaseController
from storage import RuntimeStorage


class StatusBarController(BaseController):
    def __init__(self, pad, storage: RuntimeStorage, screen_width: int) -> None:
        super().__init__(pad, storage)

        self.status_bar_width: int = screen_width
        self._pad.bkgd(' ', COLOR_STATUS_BAR_STATS)
        self.do_animation()

    def print_status(self) -> None:
        scene_size = f'{self.st.scene_size.h}x{self.st.scene_size.w}'
        map_size = f'{self.st.map_size}x{self.st.map_size}'

        actor_location = f'{self.st.actor_location.y}x{self.st.actor_location.x} '

        height = self.st.map[self.st.actor_location.y][self.st.actor_location.x].height

        border_bump = ''
        if self.st.screen_is_most_top and self.st.actor_location.y == 0:
            border_bump = 'Top border reached.'
        if self.st.screen_is_most_bottom and self.st.actor_location.y == self.st.map_coords.br.y:
            border_bump = 'Bottom border reached.'
        if self.st.screen_is_most_left and self.st.actor_location.x == 0:
            border_bump = 'Left border reached.'
        if self.st.screen_is_most_right and self.st.actor_location.x == self.st.map_coords.br.x:
            border_bump = 'Right border reached.'

        last_message = ''
        messages = len(self.st.messages)
        if messages > 1:
            last_message = self.st.messages.pop()
            messages -= 1

        if not last_message:
            last_message = border_bump

        status_line = f'Map:{map_size} Scene:{scene_size} H:{height}'
        message_line = f'{last_message}|{messages}'
        if len(message_line) + len(status_line) + len(actor_location) > self.status_bar_width:
            message_line = message_line[:(self.status_bar_width - len(status_line) - len(actor_location))]

        message_line_start = self.status_bar_width - len(message_line)

        self._pad.print(actor_location, attr=A_BOLD, cp=COLOR_STATUS_BAR_STATS)
        self._pad.print(status_line, 0, len(actor_location), cp=COLOR_STATUS_BAR_STATS)
        self._pad.print(message_line, 0, message_line_start, attr=A_BOLD, cp=COLOR_STATUS_BAR_MESSAGES)

    def process_event(self, key: int) -> None:
        pass

    def do_animation(self) -> None:
        self._pad.erase()
        self.print_status()

    def refresh(self) -> None:
        self._pad.noutrefresh(
            0, 0,
            self.st.scene_coords.br.y + 1, 0,
            self.st.scene_coords.br.y + 1, self.st.scene_coords.br.x,
        )
