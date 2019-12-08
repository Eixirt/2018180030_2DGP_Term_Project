import pico2d
import ctypes
import random
import MainState
import GameWorldManager


class Point(ctypes.Structure):
    _fields_ = [("x", ctypes.c_int),
                ("y", ctypes.c_int)]


class HitImage:
    def __init__(self):
        self.image = pico2d.load_image('resource\\hit_background.png')
        self.canvas_width = pico2d.get_canvas_width()
        self.canvas_height = pico2d.get_canvas_height()

    def update(self):
        pass

    def draw(self):
        self.image.opacify(0.25)
        self.image.clip_draw(0, 0, self.canvas_width, self.canvas_height, 0, 0, self.canvas_width * 3, self.canvas_width * 3)
        pass


class Camera:
    BOUNDARY_INTERVAL = 300
    SHAKE_TIMER = 25

    def __init__(self):
        self.image = pico2d.load_image('resource\\black_background.jpg')
        self.canvas_width = pico2d.get_canvas_width()
        self.canvas_height = pico2d.get_canvas_height()

        self.window_left = 0
        self.window_bottom = 0

        self.pivot = Point(self.window_left, self.window_bottom)

        self.w = self.image.w
        self.h = self.image.h

        self.focus_object = None

        # Camera Shake
        self.check_shaking_camera = False
        self.shaking_timer = Camera.SHAKE_TIMER
        pass

    def set_focus_object(self, player_object):
        self.focus_object = player_object
        if self.focus_object is None:
            self.focus_object = None
        pass

    def check_object_in_camera(self, object_pivot_x, object_pivot_y):

        if (self.window_left - Camera.BOUNDARY_INTERVAL <= object_pivot_x) and \
                (object_pivot_x <= self.window_left + self.canvas_width + Camera.BOUNDARY_INTERVAL) and\
                (self.window_bottom - Camera.BOUNDARY_INTERVAL <= object_pivot_y) and\
                (object_pivot_y <= self.window_bottom + self.canvas_height + Camera.BOUNDARY_INTERVAL):
            return True
        else:
            return False
        pass

    def shake_camera(self):
        if self.check_shaking_camera is False:
            self.check_shaking_camera = True
            self.shaking_timer = Camera.SHAKE_TIMER
        pass

    def update(self):
        if self.focus_object is not None:
            self.window_left = self.focus_object.pivot.x - self.canvas_width // 2
            self.window_bottom = self.focus_object.pivot.y - self.canvas_height // 2
        else:
            self.window_left = MainState.BlackBoard['player']['x'] - self.canvas_width // 2
            self.window_bottom = MainState.BlackBoard['player']['y'] - self.canvas_height // 2

        if self.check_shaking_camera is True:
            self.shaking_timer -= 1
            self.window_left += random.randrange(-20, 20)
            self.window_bottom += random.randrange(-10, 10)

            if self.shaking_timer < 0:
                self.check_shaking_camera = 0

                if self.focus_object is not None:
                    self.window_left = self.focus_object.pivot.x - self.canvas_width // 2
                    self.window_bottom = self.focus_object.pivot.y - self.canvas_height // 2
                else:
                    self.window_left = MainState.BlackBoard['player']['x'] - self.canvas_width // 2
                    self.window_bottom = MainState.BlackBoard['player']['y'] - self.canvas_height // 2
                    pass

                self.check_shaking_camera = False
            pass
        pass

    def draw(self):
        self.image.clip_draw_to_origin(0, 0, self.canvas_width, self.canvas_height, 0, 0)
        pass

    pass
