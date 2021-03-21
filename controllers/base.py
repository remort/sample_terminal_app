from pad_wrapper import Pad
from storage import RuntimeStorage


class BaseController:
    def __init__(self, pad: Pad, storage: RuntimeStorage) -> None:
        self.pad: Pad = pad
        self.st: RuntimeStorage = storage

    def process_event(self, key: int) -> None:
        pass

    def do_animation(self) -> None:
        pass

    def refresh(self) -> None:
        pass
