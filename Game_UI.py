import pico2d
import ctypes
import enum

import GameFrameWork
import GameWorldManager

import MainState


# Frame 구조체
class Point(ctypes.Structure):
    _fields_ = [("x", ctypes.c_int),
                ("y", ctypes.c_int)]


Shovel_Type_Keys = ['SHOVEL_NULL', 'SHOVEL_BASIC', 'SHOVEL_TITANIUM', 'SHOVEL_GLASS', 'SHOVEL_OBSIDIAN']
Shovel_Type_Values = list(range(-1, 5 - 1))
Shovel_Type = dict(zip(Shovel_Type_Keys, Shovel_Type_Values))


Weapon_Type_Keys = ['WEAPON_NULL', 'WEAPON_DAGGER_BASIC']
Weapon_Type_Values = list(range(-1, 2 - 1))
Weapon_Type = dict(zip(Weapon_Type_Keys, Weapon_Type_Values))

IMAGE_SCALE = 2


class UI_Player_Hp:
    HEART_IMAGE_WIDTH = 24
    HEART_IMAGE_HEIGHT = 22

    def __init__(self):
        self.image = pico2d.load_image('resource\\UI.png')
        self.pivot = Point(920, pico2d.get_canvas_height() - 35)
        self.curr_hp = 0
        self.max_hp = 0

    def update(self):
        self.curr_hp = MainState.BlackBoard['player']['curr_hp']
        self.max_hp = MainState.BlackBoard['player']['max_hp']
        pass

    def draw(self):
        # 하트
        hp_pivot = []
        for i in range(0, self.max_hp):
            if i % 2 == 0:
                interval_width = 52 * ((i // 2) % 5)
                interval_height = 47 * ((i // 2) // 5)
                hp_pivot = hp_pivot + [Point(self.pivot.x + interval_width, self.pivot.y - interval_height)]

            if i < self.curr_hp:
                if i % 2 == 0 and (i + 2) <= self.curr_hp:
                    # 꽉 찬 하트
                    self.image.clip_draw(0, self.image.h - self.HEART_IMAGE_HEIGHT,
                                         self.HEART_IMAGE_WIDTH, self.HEART_IMAGE_HEIGHT,
                                         hp_pivot[i // 2].x, hp_pivot[i // 2].y,
                                         self.HEART_IMAGE_WIDTH * IMAGE_SCALE, self.HEART_IMAGE_HEIGHT * IMAGE_SCALE)

                elif i % 2 == 0 and i + 1 == self.curr_hp:
                    # 절반의 하트
                    self.image.clip_draw(self.HEART_IMAGE_WIDTH + 5, self.image.h - self.HEART_IMAGE_HEIGHT,
                                         self.HEART_IMAGE_WIDTH, self.HEART_IMAGE_HEIGHT,
                                         hp_pivot[i // 2].x, hp_pivot[i // 2].y,
                                         self.HEART_IMAGE_WIDTH * IMAGE_SCALE, self.HEART_IMAGE_HEIGHT * IMAGE_SCALE)

            elif i >= self.curr_hp:
                # 빈 하트
                if i % 2 == 0:
                    self.image.clip_draw(self.HEART_IMAGE_WIDTH * 2 + 10, self.image.h - self.HEART_IMAGE_HEIGHT,
                                         self.HEART_IMAGE_WIDTH, self.HEART_IMAGE_HEIGHT,
                                         hp_pivot[i // 2].x, hp_pivot[i // 2].y,
                                         self.HEART_IMAGE_WIDTH * IMAGE_SCALE, self.HEART_IMAGE_HEIGHT * IMAGE_SCALE)


class UI_Player_Money:
    GOLD_WIDTH = 20
    GOLD_HEIGHT = 20
    DIAMOND_WIDTH = 25
    DIAMOND_HEIGHT = 20

    def __init__(self):
        self.image = pico2d.load_image('resource\\UI.png')
        self.font = pico2d.load_font('resource\\2dgp-money-cnt.ttf', 15)
        self.holding_gold = 0
        self.holding_diamond = 0
        self.pivot = Point(0, 0)

        self.gold_pivot = Point(pico2d.get_canvas_width() - 90, pico2d.get_canvas_height() - 35)
        self.diamond_pivot = Point(pico2d.get_canvas_width() - 90, pico2d.get_canvas_height() - 85)

    def update(self):
        self.holding_gold = MainState.BlackBoard['player']['holding_gold']
        self.holding_diamond = MainState.BlackBoard['player']['holding_diamond']
        pass

    def draw(self):
        # 골드
        self.image.clip_draw(87, self.image.h - 27 - self.GOLD_HEIGHT,
                             self.GOLD_WIDTH, self.GOLD_HEIGHT,
                             self.gold_pivot.x, self.gold_pivot.y,
                             self.GOLD_WIDTH * IMAGE_SCALE, self.GOLD_HEIGHT * IMAGE_SCALE)

        gold_str = 'x' + str(self.holding_gold)
        self.font.draw(self.gold_pivot.x + 28 + 2, self.gold_pivot.y - 3, gold_str, (0, 0, 0))  # 그림자
        self.font.draw(self.gold_pivot.x + 28, self.gold_pivot.y, gold_str, (255, 255, 255))  # 숫자

        # 다이아
        self.image.clip_draw(87, self.image.h - self.DIAMOND_HEIGHT,
                             self.DIAMOND_WIDTH, self.DIAMOND_HEIGHT,
                             self.diamond_pivot.x, self.diamond_pivot.y,
                             self.DIAMOND_WIDTH * IMAGE_SCALE, self.DIAMOND_HEIGHT * IMAGE_SCALE)

        diamond_str = 'x' + str(self.holding_diamond)
        self.font.draw(self.diamond_pivot.x + 28 + 2, self.diamond_pivot.y - 3, diamond_str, (0, 0, 0))  # 그림자
        self.font.draw(self.diamond_pivot.x + 28, self.diamond_pivot.y, diamond_str, (255, 255, 255))  # 숫자
    pass


class UI_Player_Equip:
    FRAME_IMAGE_WIDTH = 30
    FRAME_IMAGE_HEIGHT = 33
    FRAME_IMAGE_INTERVAL = 5
    FRAME_PIVOT_INTERVAL = 70

    SHOVEL_IMAGE_WIDTH = 24
    SHOVEL_IMAGE_HEIGHT = 25

    WEAPON_IMAGE_WIDTH = 13
    WEAPON_IMAGE_HEIGHT = 13
    WEAPON_IMAGE_INTERVAL = 5

    def __init__(self):
        self.frame_image = pico2d.load_image('resource\\UI.png')
        self.shovel_image = pico2d.load_image('resource\\Item_Shovel.png')
        self.weapon_image = pico2d.load_image('resource\\Item_Weapon.png')
        self.body_image = None
        self.head_image = None

        self.pivot = Point(50, pico2d.get_canvas_height() - self.FRAME_IMAGE_HEIGHT - 3)
        self.shovel_type = 0
        self.weapon_type = 0
        self.body_type = None
        self.head_type = None

    def update(self):
        self.shovel_type = MainState.BlackBoard['player']['equip_shovel']
        self.weapon_type = MainState.BlackBoard['player']['equip_weapon']
        pass

    def draw(self):
        shovel_frame_start_point = Point(self.FRAME_IMAGE_WIDTH * 0 + self.FRAME_IMAGE_INTERVAL * 0, self.frame_image.h - 54 - self.FRAME_IMAGE_HEIGHT)
        attack_frame_start_point = Point(self.FRAME_IMAGE_WIDTH * 1 + self.FRAME_IMAGE_INTERVAL * 1, self.frame_image.h - 54 - self.FRAME_IMAGE_HEIGHT)
        # 삽 틀
        self.frame_image.clip_draw(shovel_frame_start_point.x, shovel_frame_start_point.y,
                                   self.FRAME_IMAGE_WIDTH, self.FRAME_IMAGE_HEIGHT,
                                   self.pivot.x, self.pivot.y,
                                   self.FRAME_IMAGE_WIDTH * IMAGE_SCALE, self.FRAME_IMAGE_HEIGHT * IMAGE_SCALE)

        # 공격아이템 틀
        self.frame_image.clip_draw(attack_frame_start_point.x, attack_frame_start_point.y,
                                   self.FRAME_IMAGE_WIDTH, self.FRAME_IMAGE_HEIGHT,
                                   self.pivot.x + self.FRAME_PIVOT_INTERVAL, self.pivot.y,
                                   self.FRAME_IMAGE_WIDTH * IMAGE_SCALE, self.FRAME_IMAGE_HEIGHT * IMAGE_SCALE)

        # 삽 아이템
        if self.shovel_type != Shovel_Type['SHOVEL_NULL']:
            item_pivot = Point(50, pico2d.get_canvas_height() - 40)
            shovel_start_point = Point(self.SHOVEL_IMAGE_WIDTH * self.shovel_type + self.WEAPON_IMAGE_INTERVAL * self.shovel_type,
                                       self.shovel_image.h - 2 - self.SHOVEL_IMAGE_HEIGHT)

            self.shovel_image.clip_draw(shovel_start_point.x, shovel_start_point.y,
                                        self.SHOVEL_IMAGE_WIDTH, self.SHOVEL_IMAGE_HEIGHT,
                                        item_pivot.x, item_pivot.y,
                                        self.SHOVEL_IMAGE_WIDTH * IMAGE_SCALE, self.SHOVEL_IMAGE_HEIGHT * IMAGE_SCALE)
            pass

        if self.weapon_type != Weapon_Type['WEAPON_NULL']:
            item_pivot = Point(50 + 70, pico2d.get_canvas_height() - 40)
            weapon_start_point = Point(self.WEAPON_IMAGE_WIDTH * self.weapon_type + self.WEAPON_IMAGE_INTERVAL * self.weapon_type,
                                       self.weapon_image.h - 4 - self.WEAPON_IMAGE_HEIGHT)

            self.weapon_image.clip_draw(weapon_start_point.x, weapon_start_point.y,
                                        self.WEAPON_IMAGE_WIDTH, self.WEAPON_IMAGE_HEIGHT,
                                        item_pivot.x, item_pivot.y,
                                        self.WEAPON_IMAGE_WIDTH * IMAGE_SCALE, self.WEAPON_IMAGE_HEIGHT * IMAGE_SCALE)
            pass
        pass


class UI_HEARTBEAT:
    FRAME1_IMAGE_WIDTH = 34
    FRAME1_IMAGE_HEIGHT = 50

    FRAME2_IMAGE_WIDTH = 40
    FRAME2_IMAGE_HEIGHT = 50

    HEART_PUMP_TIMER = 0.55
    HEART_DUMP_TIMER = 0.6

    def __init__(self):
        self.image = pico2d.load_image('resource\\UI.png')
        self.pivot = Point(pico2d.get_canvas_width() // 2, pico2d.get_canvas_height() // 8)
        self.frame = 0

        self.timer = 0.0

    def update(self):
        self.timer += GameFrameWork.frame_time
        if self.timer >= self.HEART_DUMP_TIMER:
            self.timer -= self.HEART_DUMP_TIMER
            self.frame = 0
        elif self.timer >= self.HEART_PUMP_TIMER:
            self.frame = 1
        pass

    def draw(self):
        frame1_start_point = Point(117, self.image.h - self.FRAME1_IMAGE_HEIGHT)
        frame2_start_point = Point(155, self.image.h - self.FRAME2_IMAGE_HEIGHT)

        if self.frame == 0:
            self.image.clip_draw(frame1_start_point.x, frame1_start_point.y,
                                 self.FRAME1_IMAGE_WIDTH, self.FRAME1_IMAGE_HEIGHT,
                                 self.pivot.x, self.pivot.y,
                                 self.FRAME1_IMAGE_WIDTH * IMAGE_SCALE, self.FRAME1_IMAGE_HEIGHT * IMAGE_SCALE)
        else:
            self.image.clip_draw(frame2_start_point.x, frame2_start_point.y,
                                 self.FRAME2_IMAGE_WIDTH, self.FRAME2_IMAGE_HEIGHT,
                                 self.pivot.x, self.pivot.y,
                                 self.FRAME2_IMAGE_WIDTH * IMAGE_SCALE, self.FRAME2_IMAGE_HEIGHT * IMAGE_SCALE)
        pass

