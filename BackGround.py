import pico2d


class Scrolled_Background:
    def __init__(self):
        self.image = pico2d.load_image('resource\\black_background.jpg')
        self.canvas_width = pico2d.get_canvas_width()
        self.canvas_height = pico2d.get_canvas_height()
        self.w = self.image.w
        self.h = self.image.h

    def set_focus_object(self, player_cadence):
        # fill here
        pass

    def draw(self):
        # fill here
        pass

    def update(self):
        # fill here
        pass

    def handle_event(self, event):
        pass

    pass


class Infinite_Background:
    def __init__(self):
        self.image = pico2d.load_image('resource\\black_background.jpg')
        self.canvas_width = pico2d.get_canvas_width()
        self.canvas_height = pico2d.get_canvas_height()
        self.w = self.image.w
        self.h = self.image.h

        self.focus_object = None
        self.window_left = 0
        self.window_bottom = 0

    def set_center_object(self, player_cadence):
        self.focus_object = player_cadence

    def draw(self):
        self.image.clip_draw_to_origin(self.window_left, self.window_bottom, self.canvas_width, self.canvas_height, 0, 0)
        pass

    def update(self):
        self.window_left = pico2d.clamp(0, int(self.focus_object.x) - self.canvas_width // 2, self.w - self.canvas_width)
        self.window_bottom = pico2d.clamp(0, int(self.focus_object.y) - self.canvas_height // 2, self.h - self.canvas_height)
        pass

    pass
