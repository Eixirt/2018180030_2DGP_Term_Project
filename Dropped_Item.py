import pico2d
import ctypes

import MainState
import GameFrameWork


class Point(ctypes.Structure):
    _fields_ = [("x", ctypes.c_int),
                ("y", ctypes.c_int)]


DroppedItem_Type_Keys = ['ITEM_GOLD', 'ITEM_DIAMOND', 'ITEM_TORCH_BASIC', 'ITEM_TORCH_NORMAL', 'ITEM_TORCH_BLUE', 'ITEM_HEAL']
DroppedItem_Type_Values = list(range(len(DroppedItem_Type_Keys)))
DroppedItem_Type = dict(zip(DroppedItem_Type_Keys, DroppedItem_Type_Values))

IMAGE_SCALE = 2

TIME_PER_ACTION = 0.1
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION


class Dropped_Item:
    image = None
    shadow_image = None
    ITEM_IMAGE_WIDTH = None
    ITEM_IMAGE_HEIGHT = None
    MOVING_TIMER = 0.05

    get_sound = None

    def __init__(self, item_type=None, px=None, py=None):
        if Dropped_Item.shadow_image is None:
            Dropped_Item.shadow_image = pico2d.load_image('resource\\black_background.png')

        if Dropped_Item.get_sound is None:
            Dropped_Item.get_sound = pico2d.load_wav('resource\\sound\\obj_sound\\sfx_pickup_general_ST.wav')
            self.get_sound.set_volume(100)
            pass

        self.alpha_value = 1.0

        if px is None and py is None:
            self.pivot = Point(500, 500)
        else:
            self.pivot = Point(px, py + 10)

        if item_type is None:
            self.value = DroppedItem_Type['ITEM_GOLD']
        else:
            self.value = item_type

        self.image_start_point = None

        self.jump_max = 5
        self.starting_y = self.pivot.y
        self.dir = 1
        self.timer = self.MOVING_TIMER

    def play_get_item_sound(self):
        pass

    def get_item(self, player):
        pass

    def update(self):
        self.timer -= GameFrameWork.frame_time
        if self.timer < 0:
            self.timer += self.MOVING_TIMER
            self.pivot.y += self.dir * 1

        if self.pivot.y >= (self.starting_y + self.jump_max):
            self.dir = -1
        elif self.pivot.y <= (self.starting_y - self.jump_max):
            self.dir = 1
        self.pivot.y = pico2d.clamp(self.starting_y - self.jump_max, self.pivot.y, self.starting_y + self.jump_max)
        pass

    def draw(self):
        camera_x, camera_y = self.pivot.x - MainState.BlackBoard['camera']['camera_left'], self.pivot.y - MainState.BlackBoard['camera']['camera_bottom']

        self.image.clip_draw(self.image_start_point.x, self.image_start_point.y,
                             self.ITEM_IMAGE_WIDTH, self.ITEM_IMAGE_HEIGHT,
                             camera_x, camera_y,
                             (self.ITEM_IMAGE_WIDTH - 1) * IMAGE_SCALE, (self.ITEM_IMAGE_HEIGHT - 1) * IMAGE_SCALE)

        self.shadow_image.opacify(self.alpha_value)
        self.shadow_image.clip_draw(300, 300,
                                    self.ITEM_IMAGE_WIDTH, self.ITEM_IMAGE_HEIGHT,
                                    camera_x, camera_y,
                                    (self.ITEM_IMAGE_WIDTH - 1) * IMAGE_SCALE, (self.ITEM_IMAGE_HEIGHT - 1) * IMAGE_SCALE)
        pass


class Torch_Item(Dropped_Item):
    def __init__(self, item_type=None, px=None, py=None):
        super().__init__(item_type, px, py)
        self.image = pico2d.load_image('resource\\item_image\\Torches.png')

        self.ITEM_IMAGE_WIDTH = 23
        self.ITEM_IMAGE_HEIGHT = 27

        self.item_value = 1

        if self.value == DroppedItem_Type['ITEM_TORCH_BASIC']:
            self.image_start_point = Point(23 * 0, self.image.h - 27)
            self.item_value = 1
            pass
        elif self.value == DroppedItem_Type['ITEM_TORCH_NORMAL']:
            self.image_start_point = Point(23 * 2, self.image.h - 27)
            self.item_value = 2
            pass
        elif self.value == DroppedItem_Type['ITEM_TORCH_BLUE']:
            self.image_start_point = Point(23 * 3, self.image.h - 27)
            self.item_value = 3
            pass

    def play_get_item_sound(self):
        self.get_sound.play()
        pass

    def get_item(self, player):
        player.view_range += self.item_value
    pass


class Heal_Item(Dropped_Item):
    def __init__(self, item_type=None, px=None, py=None):
        super().__init__(item_type, px, py)
        self.image = pico2d.load_image('resource\\item_image\\Consumables.png')

        self.heal_sound = pico2d.load_wav('resource\\sound\\obj_sound\\sfx_item_food.wav')
        self.heal_sound.set_volume(99)

        self.ITEM_IMAGE_WIDTH = 22
        self.ITEM_IMAGE_HEIGHT = 22

        if self.value is None:
            self.value = DroppedItem_Type['ITEM_HEAL']
        else:
            self.value = item_type

        self.image_start_point = Point(72, self.image.h - 186)

    def get_item(self, player):
        player.equip_weapon_object.damage = 3
        player.curr_hp = player.max_hp
        pass

    def play_get_item_sound(self):
        self.get_sound.play()
        pass

    pass
