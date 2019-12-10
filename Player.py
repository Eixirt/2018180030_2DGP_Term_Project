import pico2d
import ctypes
import math
import copy
import random

import GameFrameWork
import MainState
import DeadEndState
import GameWorldManager
import Camera


# Frame 구조체
class Point(ctypes.Structure):
    _fields_ = [("x", ctypes.c_int),
                ("y", ctypes.c_int)]


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
        self.check_possible_attack = False
        self.attack_delay = Dagger_Attack.ATTACK_DELAY_TIMER
        self.timer = Dagger_Attack.ATTACK_TIMER
        self.dir = None

        self.damage = 1

        self.attack_sound = []
        for i in range(4):
            attack_sfx = pico2d.load_wav('resource\\sound\\attack_sound\\vo_cad_melee_1_0' + str(i + 1) + '.wav')
            attack_sfx.set_volume(100)
            self.attack_sound.append(attack_sfx)
            pass

    def init_attack(self, key):
        if self.check_attack is False:

            random_sound_idx = random.randint(0, 3)
            self.attack_sound[random_sound_idx].play()

            self.check_attack = True
            self.check_possible_attack = True
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


RIGHT_KEY_DOWN, LEFT_KEY_DOWN, UP_KEY_DOWN, DOWN_KEY_DOWN, RIGHT_KEY_UP, LEFT_KEY_UP, UP_KEY_UP, DOWN_KEY_UP, \
 W_KEY_DOWN, A_KEY_DOWN, S_KEY_DOWN, D_KEY_DOWN, W_KEY_UP, A_KEY_UP, S_KEY_UP, D_KEY_UP, PAGEUP_KEY_DOWN, PAGEDOWN_KEY_DOWN = range(18)

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
    (pico2d.SDL_KEYUP, pico2d.SDLK_d): D_KEY_UP,

    (pico2d.SDL_KEYDOWN, pico2d.SDLK_PAGEUP): PAGEUP_KEY_DOWN,
    (pico2d.SDL_KEYDOWN, pico2d.SDLK_PAGEDOWN): PAGEDOWN_KEY_DOWN
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

        # 시야 치트
        if event == PAGEDOWN_KEY_DOWN:
            if player.view_range > 1:
                player.view_range -= 1
            pass
        elif event == PAGEUP_KEY_DOWN:
            player.view_range += 1
            pass

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

            if player.equip_weapon_object.check_attack is False:
                if event == UP_KEY_DOWN:
                    player.equip_weapon_object.init_attack('UP')
                    pass
                elif event == DOWN_KEY_DOWN:
                    player.equip_weapon_object.init_attack('DOWN')
                    pass
                elif event == LEFT_KEY_DOWN:
                    player.equip_weapon_object.init_attack('LEFT')
                    pass
                elif event == RIGHT_KEY_DOWN:
                    player.equip_weapon_object.init_attack('RIGHT')
                    pass
        pass

    @staticmethod
    def do(player):
        player.frame['x'] = (player.frame['x'] + FRAMES_PER_ACTION * ACTION_PER_TIME * GameFrameWork.frame_time) % 4
        if player.frame['x'] == 0:
            player.frame['y'] = (player.frame['y'] + 1) % 2
            pass

        if player.equip_weapon_object.check_attack is True:
            player.equip_weapon_object.update()
        pass

    @staticmethod
    def draw(player):
        camera_x, camera_y = player.pivot.x - MainState.BlackBoard['camera']['camera_left'], player.pivot.y - MainState.BlackBoard['camera']['camera_bottom']
        # 몸

        player.image.clip_composite_draw(int(player.frame['x']) * player.BODY_IMAGE_WIDTH, player.image.h - 58 - player.BODY_IMAGE_HEIGHT,
                                         player.BODY_IMAGE_WIDTH, player.BODY_IMAGE_HEIGHT,
                                         player.rad, player.flip,
                                         camera_x, camera_y + 0.5 * player.BODY_IMAGE_HEIGHT * IMAGE_SCALE,
                                         player.BODY_IMAGE_WIDTH * IMAGE_SCALE, player.BODY_IMAGE_HEIGHT * IMAGE_SCALE)

        # 머리
        player.image.clip_composite_draw(int(player.frame['x']) * player.HEAD_IMAGE_WIDTH, player.image.h - player.HEAD_IMAGE_HEIGHT - 24 * int(player.frame['y']),
                                         player.HEAD_IMAGE_WIDTH, player.HEAD_IMAGE_HEIGHT,
                                         player.rad, player.flip,
                                         camera_x, camera_y + 0.5 * player.HEAD_IMAGE_HEIGHT * IMAGE_SCALE + player.HEAD_INTERVAL,
                                         player.HEAD_IMAGE_WIDTH * IMAGE_SCALE, player.HEAD_IMAGE_HEIGHT * IMAGE_SCALE)

        # 대거 공격
        if player.equip_weapon_object.check_attack is True and player.equip_weapon_object.timer >= 0:
            player.equip_weapon_object.draw()
        pass
    pass


next_state_table = {
    IdleState: {W_KEY_DOWN: IdleState, A_KEY_DOWN: IdleState, S_KEY_DOWN: IdleState, D_KEY_DOWN: IdleState,
                W_KEY_UP: IdleState, A_KEY_UP: IdleState, S_KEY_UP: IdleState, D_KEY_UP: IdleState,
                UP_KEY_DOWN: IdleState, DOWN_KEY_DOWN: IdleState, LEFT_KEY_DOWN: IdleState, RIGHT_KEY_DOWN: IdleState,
                UP_KEY_UP: IdleState, DOWN_KEY_UP: IdleState, LEFT_KEY_UP: IdleState, RIGHT_KEY_UP: IdleState,
                PAGEUP_KEY_DOWN: IdleState, PAGEDOWN_KEY_DOWN: IdleState}
}


class Player_Cadence:
    BODY_IMAGE_WIDTH = 24
    BODY_IMAGE_HEIGHT = 14
    HEAD_IMAGE_WIDTH = 24
    HEAD_IMAGE_HEIGHT = 12

    HIT_TIMER = 50
    
    # 머리와 몸 간의 간격 차이
    HEAD_INTERVAL = BODY_IMAGE_HEIGHT * IMAGE_SCALE - 3 * IMAGE_SCALE

    def __init__(self):
        self.image = pico2d.load_image('resource\\Character_Player.png')
        self.pivot = Point(1000, 345)
        self.frame = {'x': 0, 'y': 0}
        self.rad = 0
        self.flip = ''

        # for jump
        self.check_jumping = False
        self.jumping_count = 0
        self.start_point = self.pivot
        self.mid_point = self.pivot
        self.end_point = self.pivot
        self.jump_dir = 'RIGHT'
        self.start_jumping_time = 0.0
        self.check_moving_collide = False

        self.event_que = []
        self.init_state = IdleState
        self.curr_state = IdleState
        self.curr_state.enter_state(self, None)

        # hit_damage
        self.curr_hp = 12
        self.max_hp = 12

        self.check_get_damage = False
        self.get_damage_timer = self.HIT_TIMER
        self.get_damage_image = Camera.HitImage()

        # money
        self.holding_gold = 0
        self.holding_diamond = 0

        # attack
        self.equip_shovel = Shovel_Type['SHOVEL_TITANIUM']
        self.equip_weapon = Weapon_Type['WEAPON_DAGGER_BASIC']
        self.equip_weapon_object = Dagger_Attack(self.pivot.x, self.pivot.y)

        self.equip_body = 0
        self.equip_head = 0

        # sound
        self.hit_voice = []
        self.hit_bgm = pico2d.load_wav('resource\\sound\\hit_sound\\sfx_player_hit_ST.wav')
        self.hit_bgm.set_volume(100)
        for i in range(6):
            bgm = pico2d.load_wav('resource\\sound\\hit_sound\\vo_cad_hurt_0' + str(i+1) + '.wav')
            bgm.set_volume(90)
            self.hit_voice.append(bgm)
            pass

        # view
        self.view_range = 2

    def init_jump(self, jump_dir=None):
        if self.check_jumping is False:
            self.check_moving_collide = False
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

    def get_damage(self, damage):
        if self.check_get_damage is False:
            self.check_get_damage = True
            self.curr_hp -= damage
            if self.curr_hp <= 0:
                GameFrameWork.push_state(DeadEndState)
                pass
            else:
                self.get_damage_timer = self.HIT_TIMER
                MainState.camera.shake_camera()
                GameWorldManager.add_object(self.get_damage_image, MainState.LAYER_MESSAGE)

                ran_val = random.randrange(0, 5 + 1)
                self.hit_voice[ran_val].play()
                self.hit_bgm.play()
        pass

    def add_event(self, event):
        self.event_que.insert(0, event)
        pass

    def handle_event(self, event):
        if(event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)
            pass
        elif event.type == pico2d.SDL_KEYDOWN and event.key == pico2d.SDLK_HOME:
            print(self.pivot.x)
            print(self.pivot.y)
            print('===========')
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
        if self.check_get_damage is True:
            self.get_damage_timer -= 1
            if self.get_damage_timer < 0:
                self.get_damage_timer = 0
                self.check_get_damage = False
                GameWorldManager.remove_object(self.get_damage_image)

    pass

    def draw(self):
        if self.curr_hp > 0:
            self.curr_state.draw(self)
        pass
    pass


