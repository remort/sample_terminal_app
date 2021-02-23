class RuntimeStorage:
    def __init__(self):
        self.scene_size = None
        self.map_size = None

        self.scene_coords = None
        self.map_coords = None

        self.screen_pad_coords = None

        self.map = None

        self.bar_height = None

        self.actor_screen_center_offset = None
        self.actor_location = None

        self.screen_is_most_top = False
        self.screen_is_most_bottom = False
        self.screen_is_most_right = False
        self.screen_is_most_left = False

        self.messages = []
