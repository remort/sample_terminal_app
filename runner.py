import curses
import logging
import typing as t
from collections import deque
from time import sleep

from configuration.main import Configuration
from constants import HEIGHTS_TO_WAIT_TIME_MAP, KEY_SAVE, MOVE_KEYS
from controllers.base import BaseController
from pad_wrapper import Pad

log = logging.getLogger(__name__)


class ApplicationRunner:
    def __init__(
            self,
            kb_pad: Pad,
            scenes: t.List[BaseController],
            conf: Configuration,
            sleep_time: t.Optional[float] = 0.05,
    ) -> None:
        self._kb_pad: Pad = kb_pad
        self._scenes: t.List[BaseController] = scenes
        self._config: Configuration = conf
        self._sleep_time: float = sleep_time
        self._step_times: t.Dict[int, float] = HEIGHTS_TO_WAIT_TIME_MAP
        self._time_to_wait: float = 0.0
        self._move_keys_buff = deque()
        self._move_keys_buff_size = 10

    def set_next_keyboard_interrupt_wait_time(self) -> float:
        if self._config.debug:
            return 0
        tile = self._config.map[self._config.actor_on_map_pos.y][self._config.actor_on_map_pos.x]
        self._time_to_wait = self._step_times[tile.height]

    def run(self) -> None:
        while True:
            key = self._kb_pad.getch()

            if key == curses.KEY_END:
                break

            if key in MOVE_KEYS:
                if len(self._move_keys_buff) <= self._move_keys_buff_size:
                    self._move_keys_buff.append(key)
                curses.flushinp()
            elif key == KEY_SAVE:
                self._config.save()

            if self._time_to_wait <= 0:
                try:
                    oldest_key = self._move_keys_buff.popleft()
                except IndexError:
                    pass
                else:
                    for scene in self._scenes:
                        scene.process_event(oldest_key)
                    self.set_next_keyboard_interrupt_wait_time()

            for scene in self._scenes:
                scene.do_animation()
                scene.refresh()

            curses.doupdate()

            if self._time_to_wait > 0:
                self._time_to_wait -= self._sleep_time

            sleep(self._sleep_time)
