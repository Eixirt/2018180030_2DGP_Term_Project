import pico2d
import ctypes
import math
import copy

import GameFrameWork
import GameWorldManager


# Frame 구조체
class Point(ctypes.Structure):
    _fields_ = [("x", ctypes.c_int),
                ("y", ctypes.c_int)]


class Image_Origin_Size(ctypes.Structure):
    _fields_ = [("width", ctypes.c_int),
                ("height", ctypes.c_int)]


class Dagger_Attack:
    def __init__(self):
        self.image = pico2d.load_image('resource\\Effect_Weapon.png')
        self.pivot = Point(700, 100)
        self.frame = 0
        self.image_multiple_size = 2
        self.rad = 0
        self.flip = ''

    def attack_direction(self, key):
        if key == 'UP':
            self.rad = math.pi / 2
            self.flip = 'v'
        elif key == 'LEFT':
            self.rad = math.pi
            self.flip = 'v'
        elif key == 'DOWN':
            self.rad = 1.5 * math.pi
            self.flip = ''
        elif key == 'RIGHT':
            self.rad = 0
            self.flip = ''

    def update(self):
        self.frame = (self.frame + 1) % 3

    def draw(self):
        effect_origin_size = Image_Origin_Size(21, 16)
        self.image.clip_composite_draw(299 + self.frame * effect_origin_size.width, self.image.h - 19 - effect_origin_size.height,
                                       effect_origin_size.width, effect_origin_size.height,
                                       self.rad, self.flip,
                                       self.pivot.x - 100, self.pivot.y + effect_origin_size.height * 0.5 * self.image_multiple_size,
                                       effect_origin_size.width * self.image_multiple_size, effect_origin_size.height * self.image_multiple_size)
    pass


RIGHT_KEY_DOWN, LEFT_KEY_DOWN, UP_KEY_DOWN, DOWN_KEY_DOWN, RIGHT_KEY_UP, LEFT_KEY_UP, UP_KEY_UP, DOWN_KEY_UP, \
 W_KEY_DOWN, A_KEY_DOWN, S_KEY_DOWN, D_KEY_DOWN, W_KEY_UP, A_KEY_UP, S_KEY_UP, D_KEY_UP = range(16)

Shovel_Type_Keys = ['SHOVEL_NULL', 'SHOVEL_BASIC', 'SHOVEL_TITANIUM', 'SHOVEL_GLASS', 'SHOVEL_OBSIDIAN']
Shovel_Type_Values = list(range(-1, 5 - 1))
Shovel_Type = dict(zip(Shovel_Type_Keys, Shovel_Type_Values))

Weapon_Type_Keys = ['WEAPON_NULL', 'WEAPON_DAGGER_BASIC']
Weapon_Type_Values = list(range(-1, 2 - 1))
Weapon_Type = dict(zip(Weapon_Type_Keys, Weapon_Type_Values))

key_event_table = {
    (pico2d.SDL_KEYDOWN, pico2d.SDLK_RIGHT): RIGHT_KEY_DOWN,
    (pico2d.SDL_KEYDOWN, pico2d.SDLK_LEFT): LEFT_KEY_DOWN,
    (pico2d.SDL_KEYDOWN, pico2d.SDLK_UP): UP_KEY_DOWN,
    (pico2d.SDL_KEYDOWN, pico2d.SDLK_DOWN): DOWN_KEY_DOWN,
    (pico2d.SDL_KEYUP, pico2d.SDLK_RIGHT): RIGHT_KEY_UP,
    (pico2d.SDL_KEYUP, pico2d.SDLK_LEFT): LEFT_KEY_UP,
    (pico2d.SDL_KEYUP, pico2d.SDLK_UP): UP_KEY_UP,
    (pico2d.SDL_KEYUP, pico2d.SDLK_DOWN): DOWN_KEY_UP,

    (pico2d.SDL_KEYDOWN, pico2d.SDLK_w): W_KEY_DOWN,
    (pico2d.SDL_KEYDOWN, pico2d.SDLK_a): A_KEY_DOWN,
    (pico2d.SDL_KEYDOWN, pico2d.SDLK_s): S_KEY_DOWN,
    (pico2d.SDL_KEYDOWN, pico2d.SDLK_d): D_KEY_DOWN,
    (pico2d.SDL_KEYUP, pico2d.SDLK_w): W_KEY_UP,
    (pico2d.SDL_KEYUP, pico2d.SDLK_a): A_KEY_UP,
    (pico2d.SDL_KEYUP, pico2d.SDLK_s): S_KEY_UP,
    (pico2d.SDL_KEYUP, pico2d.SDLK_d): D_KEY_UP
}

IMAGE_SCALE = 2

# Player Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4

TIME_PER_JUMP = 0.1
JUMP_PER_TIME = 1.0 / TIME_PER_JUMP
FRAMES_PER_JUMP = 50


class IdleState:
    @staticmethod
    def enter_state(player, event):
        # 이동
        if player.check_jumping is False:
            if event == W_KEY_DOWN:
                # player.pivot.y += 50
                pass
            elif event == A_KEY_DOWN:
                # player.pivot.x -= 50
                # player.rad = math.pi
                # player.flip = 'v'
                pass
            elif event == S_KEY_DOWN:
                # player.pivot.y -= 50
                pass
            elif event == D_KEY_DOWN:
                # player.pivot.x += 50
                # player.rad = 0
                # player.flip = ''
                pass

        # 공격

        pass

    @staticmethod
    def exit_state(player, event):
        if player.check_jumping is False:
            if event == W_KEY_DOWN:
                player.init_jump('UP')
                pass
            elif event == A_KEY_DOWN:
                player.init_jump('LEFT')
                player.rad = math.pi
                player.flip = 'v'
                pass
            elif event == S_KEY_DOWN:
                player.init_jump('DOWN')
                pass
            elif event == D_KEY_DOWN:
                player.init_jump('RIGHT')
                player.rad = 0
                player.flip = ''
                pass
        pass

    @staticmethod
    def do(player):
        player.frame['x'] = (player.frame['x'] + FRAMES_PER_ACTION * ACTION_PER_TIME * GameFrameWork.frame_time) % 4
        if player.frame['x'] == 0:
            player.frame['y'] = (player.frame['y'] + 1) % 2
            pass

        pass

    @staticmethod
    def draw(player):
        # 몸
        player.image.clip_composite_draw(int(player.frame['x']) * player.BODY_IMAGE_WIDTH, player.image.h - 58 - player.BODY_IMAGE_HEIGHT,
                                         player.BODY_IMAGE_WIDTH, player.BODY_IMAGE_HEIGHT,
                                         player.rad, player.flip,
                                         player.pivot.x, player.pivot.y + 0.5 * player.BODY_IMAGE_HEIGHT * IMAGE_SCALE,
                                         player.BODY_IMAGE_WIDTH * IMAGE_SCALE, player.BODY_IMAGE_HEIGHT * IMAGE_SCALE)

        # 머리
        player.image.clip_composite_draw(int(player.frame['x']) * player.HEAD_IMAGE_WIDTH, player.image.h - player.HEAD_IMAGE_HEIGHT - 24 * int(player.frame['y']),
                                         player.HEAD_IMAGE_WIDTH, player.HEAD_IMAGE_HEIGHT,
                                         player.rad, player.flip,
                                         player.pivot.x, player.pivot.y + 0.5 * player.HEAD_IMAGE_HEIGHT * IMAGE_SCALE + player.HEAD_INTERVAL,
                                         player.HEAD_IMAGE_WIDTH * IMAGE_SCALE, player.HEAD_IMAGE_HEIGHT * IMAGE_SCALE)
        pass
    pass


next_state_table = {
    IdleState: {W_KEY_DOWN: IdleState, A_KEY_DOWN: IdleState, S_KEY_DOWN: IdleState, D_KEY_DOWN: IdleState,
                W_KEY_UP: IdleState, A_KEY_UP: IdleState, S_KEY_UP: IdleState, D_KEY_UP: IdleState,
                UP_KEY_DOWN: IdleState, DOWN_KEY_DOWN: IdleState, LEFT_KEY_DOWN: IdleState, RIGHT_KEY_DOWN: IdleState,
                UP_KEY_UP: IdleState, DOWN_KEY_UP: IdleState, LEFT_KEY_UP: IdleState, RIGHT_KEY_UP: IdleState}
}


class Player_Cadence:
    BODY_IMAGE_WIDTH = 24
    BODY_IMAGE_HEIGHT = 14
    HEAD_IMAGE_WIDTH = 24
    HEAD_IMAGE_HEIGHT = 12
    
    # 머리와 몸 간의 간격 차이
    HEAD_INTERVAL = BODY_IMAGE_HEIGHT * IMAGE_SCALE - 3 * IMAGE_SCALE

    def __init__(self):
        self.image = pico2d.load_image('resource\\Character_Player.png')
        self.pivot = Point(500, 100)
        self.frame = {'x': 0, 'y': 0}
        self.rad = 0
        self.flip = ''

        # for jump
        self.check_jumping = False
        self.jumping_count = 0
        self.start_point = self.pivot
        self.mid_point = self.pivot
        self.end_point = self.pivot
        self.jump_dir = None
        self.start_jumping_time = 0.0

        self.event_que = []
        self.init_state = IdleState
        self.curr_state = IdleState
        self.curr_state.enter_state(self, None)

        self.curr_hp = 13
        self.max_hp = 16

        self.holding_gold = 0
        self.holding_diamond = 0

        self.equip_shovel = Shovel_Type['SHOVEL_TITANIUM']
        self.equip_weapon = Weapon_Type['WEAPON_DAGGER_BASIC']
        self.equip_body = 0
        self.equip_head = 0

    def init_jump(self, jump_dir=None):
        if self.check_jumping is False:
            self.check_jumping = True
            self.start_point = copy.copy(self.pivot)
            self.mid_point = copy.copy(self.pivot)
            self.end_point = copy.copy(self.pivot)
            self.jump_dir = jump_dir
            self.jumping_count = 0
            self.start_jumping_time = pico2d.get_time()
            if self.jump_dir == 'UP':
                self.mid_point.x += 10
                self.mid_point.y += 25

                self.end_point.y += 50
                pass
            elif self.jump_dir == 'DOWN':
                self.mid_point.x += 10
                self.mid_point.y -= 25

                self.end_point.y -= 50
                pass
            elif self.jump_dir == 'LEFT':
                self.mid_point.x -= 25
                self.mid_point.y += 10

                self.end_point.x -= 50
                pass
            elif self.jump_dir == 'RIGHT':
                self.mid_point.x += 25
                self.mid_point.y += 10

                self.end_point.x += 50
                pass

            pass
        pass

    def jump(self):
        jump_time = pico2d.get_time() - self.start_jumping_time
        self.jumping_count = (self.jumping_count + FRAMES_PER_JUMP * JUMP_PER_TIME * GameFrameWork.frame_time)
        jump_progress = int(self.jumping_count) / FRAMES_PER_JUMP
        # x = (2 * t ** 2 - 3 * t + 1) * p1[0] + (-4 * t ** 2 + 4 * t) * p2[0] + (2 * t ** 2 - t) * p3[0]
        # y = (2 * t ** 2 - 3 * t + 1) * p1[1] + (-4 * t ** 2 + 4 * t) * p2[1] + (2 * t ** 2 - t) * p3[1]

        self.pivot.x = int((2 * jump_progress ** 2 - 3 * jump_progress + 1) * self.start_point.x +
                           (-4 * jump_progress ** 2 + 4 * jump_progress) * self.mid_point.x +
                           (2 * jump_progress ** 2 - jump_progress) * self.end_point.x)

        self.pivot.y = int((2 * jump_progress ** 2 - 3 * jump_progress + 1) * self.start_point.y +
                           (-4 * jump_progress ** 2 + 4 * jump_progress) * self.mid_point.y +
                           (2 * jump_progress ** 2 - jump_progress) * self.end_point.y)
        if self.jump_dir == 'UP':
            if int(self.jumping_count) >= FRAMES_PER_JUMP - 1:
                self.pivot.x = copy.copy(self.end_point.x)
                self.pivot.y = copy.copy(self.end_point.y)
                self.check_jumping = False
                pass
            pass
        elif self.jump_dir == 'DOWN':
            if int(self.jumping_count) >= FRAMES_PER_JUMP - 1:
                self.pivot.x = copy.copy(self.end_point.x)
                self.pivot.y = copy.copy(self.end_point.y)
                self.check_jumping = False
                pass
            pass
        elif self.jump_dir == 'LEFT':
            if int(self.jumping_count) >= FRAMES_PER_JUMP - 1:
                self.pivot.x = copy.copy(self.end_point.x)
                self.pivot.y = copy.copy(self.end_point.y)
                self.check_jumping = False
                pass
            pass
        elif self.jump_dir == 'RIGHT':
            if int(self.jumping_count) >= FRAMES_PER_JUMP - 1:
                self.pivot.x = copy.copy(self.end_point.x)
                self.pivot.y = copy.copy(self.end_point.y)
                self.check_jumping = False
                pass
            pass

        pass

    def add_event(self, event):
        self.event_que.insert(0, event)
        pass

    def handle_event(self, event):
        if(event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)
            pass
        pass

    def update(self):
        self.curr_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.curr_state.exit_state(self, event)
            self.curr_state = next_state_table[self.curr_state][event]
            self.curr_state.enter_state(self, event)
        pass

        if self.check_jumping is True:
            self.jump()
    pass

    def draw(self):
        self.curr_state.draw(self)
        pass
    pass


