from storage import RuntimeStorage
from tools import Pad


class BaseController:
    def __init__(self, pad: Pad, storage: RuntimeStorage) -> None:
        self._pad: Pad = pad
        self.st: RuntimeStorage = storage

    def process_event(self, key: int) -> None:
        pass

    def do_animation(self) -> None:
        pass
