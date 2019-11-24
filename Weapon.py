import pico2d
import ctypes
import math

import MainState
import GameFrameWork


# Frame 구조체
class Point(ctypes.Structure):
    _fields_ = [("x", ctypes.c_int),
                ("y", ctypes.c_int)]


IMAGE_SCALE = 2


class Dagger_Attack:
    DAGGER_EFFECT_WIDTH = 21
    DAGGER_EFFECT_HEIGHT = 16

    ATTACK_TIMER = 30
    ATTACK_DELAY_TIMER = 50

    TIME_PER_ACTION = 0.2
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 3

    def __init__(self, x=None, y=None):
        self.image = pico2d.load_image('resource\\Effect_Weapon.png')
        self.pivot = Point(0, 0)
        if x is not None and y is not None:
            self.pivot = Point(x, y)
        self.frame = 0
        self.rad = 0
        self.flip = ''

        self.check_attack = False
        self.attack_delay = Dagger_Attack.ATTACK_DELAY_TIMER
        self.timer = Dagger_Attack.ATTACK_TIMER
        self.dir = None

        self.damage = 1

    def init_attack(self, key):
        if self.check_attack is False:
            self.check_attack = True
            self.pivot = Point(MainState.BlackBoard['player']['x'], MainState.BlackBoard['player']['y'])
            self.dir = key
            self.timer = Dagger_Attack.ATTACK_TIMER
            self.frame = 0
            self.attack_delay = Dagger_Attack.ATTACK_DELAY_TIMER

            if key == 'UP':
                self.rad = math.pi / 2
                self.flip = 'v'
                self.pivot.y += 50
            elif key == 'LEFT':
                self.rad = math.pi
                self.flip = 'v'
                self.pivot.x -= 50
            elif key == 'DOWN':
                self.rad = 1.5 * math.pi
                self.flip = ''
                self.pivot.y -= 50
            elif key == 'RIGHT':
                self.rad = 0
                self.flip = ''
                self.pivot.x += 50

    def update(self):
        # self.frame = (self.frame + 1) % 3
        self.frame = (self.frame + Dagger_Attack.FRAMES_PER_ACTION * Dagger_Attack.ACTION_PER_TIME * GameFrameWork.frame_time) % 3
        self.timer -= 1
        if self.timer < 0:
            self.attack_delay -= 1
            if self.attack_delay < 0:
                self.check_attack = False

    def draw(self):
        camera_x, camera_y = self.pivot.x - MainState.BlackBoard['camera']['camera_left'], self.pivot.y - MainState.BlackBoard['camera']['camera_bottom']

        self.image.clip_composite_draw(299 + int(self.frame) * Dagger_Attack.DAGGER_EFFECT_WIDTH, self.image.h - 19 - Dagger_Attack.DAGGER_EFFECT_HEIGHT,
                                       Dagger_Attack.DAGGER_EFFECT_WIDTH, Dagger_Attack.DAGGER_EFFECT_HEIGHT,
                                       self.rad, self.flip,
                                       camera_x, camera_y + Dagger_Attack.DAGGER_EFFECT_HEIGHT * 0.5 * IMAGE_SCALE,
                                       Dagger_Attack.DAGGER_EFFECT_WIDTH * IMAGE_SCALE, Dagger_Attack.DAGGER_EFFECT_HEIGHT * IMAGE_SCALE)
    pass