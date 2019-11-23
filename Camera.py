import pico2d
import ctypes
import GameWorldManager


class Point(ctypes.Structure):
    _fields_ = [("x", ctypes.c_int),
                ("y", ctypes.c_int)]


class Camera:
    BOUNDARY_INTERVAL = 300

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
        pass

    def set_focus_object(self, player_object):
        self.focus_object = player_object
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

    def update(self):
        self.window_left = self.focus_object.pivot.x - self.canvas_width // 2
        self.window_bottom = self.focus_object.pivot.y - self.canvas_height // 2
        pass

    def draw(self):
        self.image.clip_draw_to_origin(0, 0,
                                       self.canvas_width, self.canvas_height, 0, 0)
        pass

    pass
