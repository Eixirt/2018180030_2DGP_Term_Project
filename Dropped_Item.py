import pico2d
import ctypes

import MainState


class Point(ctypes.Structure):
    _fields_ = [("x", ctypes.c_int),
                ("y", ctypes.c_int)]


DroppedItem_Type_Keys = ['GOLD', 'DIAMOND', 'TORCH']
DroppedItem_Type_Values = list(range(len(DroppedItem_Type_Keys)))
DroppedItem_Type = dict(zip(DroppedItem_Type_Keys, DroppedItem_Type_Values))

IMAGE_SCALE = 2


class Dropped_Item:
    shadow_image = pico2d.load_image('resource\\black_background.png')

    def __init__(self, selected_block=None, px=None, py=None):
        self.alpha_value = 1.0

        if px is None and py is None:
            self.pivot = Point(500, 500)
        else:
            self.pivot = Point(px, py)

        if selected_block is None:
            self.value = DroppedItem_Type['BLOCK_BASIC_STRONG_COLOR_1']
        else:
            self.value = selected_block

    def update(self):
        pass

    def draw(self):
        camera_x, camera_y = self.pivot.x - MainState.BlackBoard['camera']['camera_left'], self.pivot.y - MainState.BlackBoard['camera']['camera_bottom']

        image_start_point = Point(0, self.image.h - 26)
        if self.value == DroppedItem_Type['BLOCK_BASIC_STRONG_COLOR_1']:
            image_start_point = Point(0, self.image.h - 26)
        elif self.value == DroppedItem_Type['BLOCK_BASIC_WEAK_COLOR_1']:
            image_start_point = Point(26 * 2, self.image.h - 26)
        elif self.value == DroppedItem_Type['BLOCK_PINK_COLOR']:
            image_start_point = Point(26 * 2, self.image.h - 26 * 2)

        self.image.clip_draw(image_start_point.x, image_start_point.y,
                             self.BLOCK_IMAGE_WIDTH, self.BLOCK_IMAGE_HEIGHT,
                             camera_x, camera_y,
                             (self.BLOCK_IMAGE_WIDTH - 1) * IMAGE_SCALE, (self.BLOCK_IMAGE_HEIGHT - 1) * IMAGE_SCALE)

        self.shadow_image.opacify(self.alpha_value)
        self.shadow_image.clip_draw(300, 300,
                                    self.BLOCK_IMAGE_WIDTH, self.BLOCK_IMAGE_HEIGHT,
                                    camera_x, camera_y,
                                    (self.BLOCK_IMAGE_WIDTH - 1) * IMAGE_SCALE, (self.BLOCK_IMAGE_HEIGHT - 1) * IMAGE_SCALE)
        pass


