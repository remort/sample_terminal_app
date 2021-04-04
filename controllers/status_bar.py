import logging

from colors import A_BOLD, COLOR_STATUS_BAR_MESSAGES, COLOR_STATUS_BAR_STATS
from configuration.main import Configuration
from controllers.base import BaseController
from pad_wrapper import Pad

log = logging.getLogger(__name__)


class StatusBarController(BaseController):
    def __init__(self, pad: Pad, storage: Configuration) -> None:
        super().__init__(pad, storage)

        self.status_bar_width: int = self.st.status_bar_width
        self.pad.bkgd(' ', COLOR_STATUS_BAR_STATS)
        self.do_animation()

    def print_status(self) -> None:
        map_size = f'{self.st.map_size}x{self.st.map_size}'
        scene_size = f'{self.st.scene_size.h}x{self.st.scene_size.w}'

        actor_location = f'{self.st.actor_on_map_pos.y}x{self.st.actor_on_map_pos.x} '
        height = self.st.map[self.st.actor_on_map_pos.y][self.st.actor_on_map_pos.x].height

        border_bump = ''
        if self.st.scene_is_most_top and self.st.actor_on_map_pos.y == 0:
            border_bump = 'Top border reached.'
        if self.st.scene_is_most_bottom and self.st.actor_on_map_pos.y == self.st.map_size - 1:
            border_bump = 'Bottom border reached.'
        if self.st.scene_is_most_left and self.st.actor_on_map_pos.x == 0:
            border_bump = 'Left border reached.'
        if self.st.scene_is_most_right and self.st.actor_on_map_pos.x == self.st.map_size - 1:
            border_bump = 'Right border reached.'

        last_message = ''
        messages = len(self.st.messages)
        if messages > 0:
            last_message = self.st.messages.pop()
            messages -= 1

        if not last_message:
            last_message = border_bump

        status_line = f'Map:{map_size} Scene:{scene_size} H:{height}'
        message_line = f'{last_message}|{messages}'
        if len(message_line) + len(status_line) + len(actor_location) > self.status_bar_width:
            message_line = message_line[:(self.status_bar_width - len(status_line) - len(actor_location))]

        message_line_start = self.status_bar_width - len(message_line)

        self.pad.print(actor_location, attr=A_BOLD, cp=COLOR_STATUS_BAR_STATS)
        self.pad.print(status_line, 0, len(actor_location), cp=COLOR_STATUS_BAR_STATS)
        self.pad.print(message_line, 0, message_line_start, attr=A_BOLD, cp=COLOR_STATUS_BAR_MESSAGES)

    def process_event(self, key: int) -> None:
        pass

    def do_animation(self) -> None:
        self.pad.erase()
        self.print_status()
        # Resolves curses' "typing the last character of the last line" problem.
        self.pad.move(0, 0)

    def refresh(self) -> None:
        self.pad.noutrefresh(
            0, 0,
            self.st.scene_pad_coords.br.y + 1, 0,
            self.st.scene_pad_coords.br.y + 1, self.st.scene_pad_coords.br.x,
        )
