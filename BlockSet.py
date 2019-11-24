import pico2d
import ctypes

import MainState


class Point(ctypes.Structure):
    _fields_ = [("x", ctypes.c_int),
                ("y", ctypes.c_int)]


Block_Type_Keys = ['BLOCK_NULL',
                   'BLOCK_BASIC_STRONG_COLOR_1', 'BLOCK_BASIC_WEAK_COLOR_1',
                   'BLOCK_BASIC_STRONG_COLOR_2', 'BLOCK_BASIC_WEAK_COLOR_2',
                   'BLOCK_CYAN_COLOR', 'BLOCK_PINK_COLOR', 'BLOCK_STAIR_CLOSED', 'BLOCK_STAIR_OPENED']
Block_Type_Values = list(range(len(Block_Type_Keys)))
Block_Type = dict(zip(Block_Type_Keys, Block_Type_Values))


Wall_Type_Keys = ['WALL_NULL', 'WALL_BASIC_1', 'WALL_BASIC_2', 'WALL_VINE', 'WALL_STONE',
                  'WALL_STONE_DAMAGED', 'WALL_SKULL_1', 'WALL_SKULL_2', 'WALL_SKULL_3']
Wall_Type_Values = list(range(len(Wall_Type_Keys)))
Wall_Type = dict(zip(Wall_Type_Keys, Wall_Type_Values))

IMAGE_SCALE = 2


class Block:
    image = None
    BLOCK_IMAGE_WIDTH = 26
    BLOCK_IMAGE_HEIGHT = 26

    def __init__(self, selected_block=None, px=None, py=None):
        if Block.image is None:
            Block.image = pico2d.load_image('resource\\Block_Floors.png')
        if px is None and py is None:
            self.pivot = Point(500, 500)
        else:
            self.pivot = Point(px, py)

        if selected_block is None:
            self.value = Block_Type['BLOCK_BASIC_STRONG_COLOR_1']
        else:
            self.value = selected_block

    def update(self):
        pass

    def draw(self):
        camera_x, camera_y = self.pivot.x - MainState.BlackBoard['camera']['camera_left'], self.pivot.y - MainState.BlackBoard['camera']['camera_bottom']

        image_start_point = Point(0, self.image.h - 26)
        if self.value == Block_Type['BLOCK_BASIC_STRONG_COLOR_1']:
            image_start_point = Point(0, self.image.h - 26)
        elif self.value == Block_Type['BLOCK_BASIC_WEAK_COLOR_1']:
            image_start_point = Point(26 * 2, self.image.h - 26)
        elif self.value == Block_Type['BLOCK_PINK_COLOR']:
            image_start_point = Point(26 * 2, self.image.h - 26 * 2)

        self.image.clip_draw(image_start_point.x, image_start_point.y,
                             self.BLOCK_IMAGE_WIDTH, self.BLOCK_IMAGE_HEIGHT,
                             camera_x, camera_y,
                             (self.BLOCK_IMAGE_WIDTH - 1) * IMAGE_SCALE, (self.BLOCK_IMAGE_HEIGHT - 1) * IMAGE_SCALE)
        pass


class Wall:
    image = None
    WALL_IMAGE_WIDTH = 24
    WALL_IMAGE_HEIGHT = 40

    def __init__(self, selected_wall=None, px=None, py=None):
        if Wall.image is None:
            Wall.image = pico2d.load_image('resource\\Block_Walls.png')
        if px is None and py is None:
            self.pivot = Point(400, 500)
        else:
            self.pivot = Point(px, py)

        if selected_wall is None:
            self.value = Wall_Type['WALL_BASIC_1']
        else:
            self.value = selected_wall

    def update(self):
        pass

    def draw(self):
        camera_x, camera_y = self.pivot.x - MainState.BlackBoard['camera']['camera_left'], self.pivot.y - MainState.BlackBoard['camera']['camera_bottom']

        image_start_point = Point(0, self.image.h - 40)
        if self.value == Wall_Type['WALL_BASIC_1']:
            image_start_point = Point(0, self.image.h - 40)
        elif self.value == Wall_Type['WALL_BASIC_2']:
            image_start_point = Point(24 * 1, self.image.h - 40)
        elif self.value == Wall_Type['WALL_VINE']:
            image_start_point = Point(24 * 2, self.image.h - 40)
        elif self.value == Wall_Type['WALL_STONE']:
            image_start_point = Point(24 * 29, self.image.h - 40)
        elif self.value == Wall_Type['WALL_STONE_DAMAGED']:
            image_start_point = Point(24 * 30, self.image.h - 40)
        elif self.value == Wall_Type['WALL_SKULL_1']:
            image_start_point = Point(24 * 7, self.image.h - 40)
        elif self.value == Wall_Type['WALL_SKULL_2']:
            image_start_point = Point(24 * 8, self.image.h - 40)
        elif self.value == Wall_Type['WALL_SKULL_3']:
            image_start_point = Point(24 * 9, self.image.h - 40)

        self.image.clip_draw(image_start_point.x, image_start_point.y,
                             self.WALL_IMAGE_WIDTH, self.WALL_IMAGE_HEIGHT,
                             camera_x, camera_y,
                             (self.WALL_IMAGE_WIDTH + 1) * IMAGE_SCALE, (self.WALL_IMAGE_HEIGHT) * IMAGE_SCALE)
        pass