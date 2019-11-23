import pico2d


class Scrolled_Background:
    def __init__(self):
        self.image = pico2d.load_image('resource\\black_background.jpg')
        self.canvas_width = pico2d.get_canvas_width()
        self.canvas_height = pico2d.get_canvas_height()

        self.window_left = 0
        self.window_bottom = 0

        self.w = self.image.w
        self.h = self.image.h
        self.focus_object = None

    def set_focus_object(self, player_cadence):
        # fill here
        self.focus_object = player_cadence
        pass

    def draw(self):
        # fill here
        self.image.clip_draw_to_origin(self.window_left, self.window_bottom,
                                       self.canvas_width, self.canvas_height, 0, 0)
        pass

    def update(self):
        # fill here
        self.window_left = pico2d.clamp(0, int(self.focus_object.pivot.x) - self.canvas_width // 2, self.w - self.canvas_width)
        self.window_bottom = pico2d.clamp(0, int(self.focus_object.pivot.y) - self.canvas_height // 2, self.h - self.canvas_height)
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

        self.q1l, self.q1b, self.q1w, self.q1h = 0, 0, 0, 0
        self.q2l, self.q2b, self.q2w, self.q2h = 0, 0, 0, 0
        self.q3l, self.q3b, self.q3w, self.q3h = 0, 0, 0, 0
        self.q4l, self.q4b, self.q4w, self.q4h = 0, 0, 0, 0

    def set_center_object(self, player_cadence):
        self.focus_object = player_cadence

    def draw(self):
        self.image.clip_draw_to_origin(self.q3l, self.q3b, self.q3w, self.q3h, 0, 0)
        pass

    def update(self):
        self.q3l = (int(self.focus_object.pivot.x) - self.canvas_width // 2) % self.w
        self.q3b = (int(self.focus_object.pivot.y) - self.canvas_height // 2) % self.h
        self.q3w = pico2d.clamp(0, self.w - self.q3l, self.w)
        self.q3h = pico2d.clamp(0, self.h - self.q3b, self.h)

        # quadrant 2
        self.q2l = 0
        self.q2b = 0
        self.q2w = 0
        self.q2h = 0

        # quadrand 4
        self.q4l = 0
        self.q4b = 0
        self.q4w = 0
        self.q4h = 0

        # quadrand 1
        self.q1l = 0
        self.q1b = 0
        self.q1w = 0
        self.q1h = 0
        pass

    pass
