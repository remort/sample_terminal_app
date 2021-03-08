import curses
import typing as t
from collections import deque
from time import sleep

from controllers.base import BaseController
from storage import RuntimeStorage
from tools import Pad


class AnimationRunner:
    def __init__(
            self,
            kb_pad: Pad,
            scenes: t.List[BaseController],
            storage: RuntimeStorage,
            sleep_time: t.Optional[float] = 0.05,
    ) -> None:
        self._kb_pad: Pad = kb_pad
        self._scenes: t.List[BaseController] = scenes
        self._st: RuntimeStorage = storage
        self._sleep_time: float = sleep_time
        self._step_times: t.Dict[int, float] = self._st.heights_to_wait_time_map
        self._time_to_wait: float = 0.0
        self._move_keys_buff = deque()
        self._move_keys_buff_len = 5

    def set_next_keyboard_interrupt_wait_time(self) -> float:
        if self._st.debug:
            return 0
        tile = self._st.map[self._st.actor_location.y][self._st.actor_location.x]
        self._time_to_wait = self._step_times[tile.height]

    def run(self) -> None:
        while True:
            key = self._kb_pad.getch()

            if key == curses.KEY_END:
                break

            if key in self._st.move_keys:
                if len(self._move_keys_buff) <= self._move_keys_buff_len:
                    self._move_keys_buff.append(key)

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
