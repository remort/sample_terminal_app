from configuration.main import Configuration
from pad_wrapper import Pad


class BaseController:
    def __init__(self, pad: Pad, storage: Configuration) -> None:
        self.pad: Pad = pad
        self.st: Configuration = storage

    def process_event(self, key: int) -> None:
        pass

    def do_animation(self) -> None:
        pass

    def refresh(self) -> None:
        pass
