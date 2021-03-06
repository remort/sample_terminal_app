from storage import RuntimeStorage
from tools import Pad


class BaseController:
    def __init__(self, pad, storage: RuntimeStorage):
        self._pad: Pad = pad
        self.st: RuntimeStorage = storage

    def process_event(self, key):
        pass

    def do_animation(self):
        pass
