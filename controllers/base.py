from configuration.main import Configuration
from pad_wrapper import Pad


class BaseController:
    def __init__(self, pad: Pad, configuration: Configuration) -> None:
        self.pad: Pad = pad
        self.cf: Configuration = configuration

    def process_event(self, key: int) -> None:
        pass

    def do_animation(self) -> None:
        pass

    def refresh(self) -> None:
        pass
