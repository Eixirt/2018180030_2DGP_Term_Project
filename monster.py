import pico2d
import ctypes

import MainState
import GameFrameWork
from BehaviorTree import BehaviorTree, SelectorNode, SequenceNode, LeafNode


class Point(ctypes.Structure):
    _fields_ = [("x", ctypes.c_int),
                ("y", ctypes.c_int)]


Monster_Type_Keys = ['MONSTER_NULL',
                     'MONSTER_SLIME_GREEN', 'MONSTER_SLIME_BLUE',
                     'MONSTER_SKULL_WHITE', 'MONSTER_BAT_BASIC',
                     'MONSTER_BANSHEE']
Monster_Type_Values = list(range(len(Monster_Type_Keys)))
Monster_Type = dict(zip(Monster_Type_Keys, Monster_Type_Values))

IMAGE_SCALE = 2

# Monster Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION


class Monster:
    hp_image = None
    HP_OBJECT_WIDTH = 12
    HP_OBJECT_HEIGHT = 11
    HP_AND_MOB_INTERVAL = 3

    def __init__(self):
        if Monster.hp_image is None:
            Monster.hp_image = pico2d.load_image('resource\\UI.png')
        self.full_hp_image_start_point = Point(227, Monster.hp_image.h - 40)
        self.empty_hp_image_start_point = Point(241, Monster.hp_image.h - 40)

        self.pivot = Point(0, 0)

        self.curr_hp = None
        self.max_hp = None

        self.object_width = None
        self.object_height = None

        self.image_start_point = None
        self.frame = None
        self.max_frame = None

        self.dir = None
        self.timer = None
        self.bt = None

    def update(self):
        pass

    def draw(self):
        camera_x, camera_y = self.pivot.x - MainState.BlackBoard['camera']['camera_left'], self.pivot.y - MainState.BlackBoard['camera']['camera_bottom']

        self.image.clip_draw(self.image_start_point[int(self.frame)].x, self.image_start_point[int(self.frame)].y,
                             self.object_width, self.object_height,
                             camera_x, camera_y,
                             (self.object_width - 1) * IMAGE_SCALE, (self.object_height - 1) * IMAGE_SCALE)

        # 하트 그리기
        for i in range(0, self.max_hp):
            # 꽉 찬 하트
            if i < self.curr_hp:
                self.hp_image.clip_draw(self.full_hp_image_start_point.x, self.full_hp_image_start_point.y,
                                        Monster.HP_OBJECT_WIDTH, Monster.HP_OBJECT_HEIGHT,
                                        camera_x + (i + 0.5 - self.max_hp / 2) * (Monster.HP_OBJECT_WIDTH * IMAGE_SCALE), camera_y + (self.object_height / 2 + Monster.HP_AND_MOB_INTERVAL) * IMAGE_SCALE,
                                        Monster.HP_OBJECT_WIDTH * IMAGE_SCALE, Monster.HP_OBJECT_HEIGHT * IMAGE_SCALE)
                pass
            # 빈 하트
            elif i >= self.curr_hp:
                self.hp_image.clip_draw(self.empty_hp_image_start_point.x, self.empty_hp_image_start_point.y,
                                        Monster.HP_OBJECT_WIDTH, Monster.HP_OBJECT_HEIGHT,
                                        camera_x + (i + 0.5 - self.max_hp / 2) * (Monster.HP_OBJECT_WIDTH * IMAGE_SCALE), camera_y + (self.object_height / 2 + Monster.HP_AND_MOB_INTERVAL) * IMAGE_SCALE,
                                        Monster.HP_OBJECT_WIDTH * IMAGE_SCALE, Monster.HP_OBJECT_HEIGHT * IMAGE_SCALE)
                pass

        pass


class Slime_Green(Monster):
    image = None

    def __init__(self, px=None, py=None):
        super().__init__()

        if Slime_Green.image is None:
            Slime_Green.image = pico2d.load_image('resource\\Monster_Slime.png')
            pass

        if px is None and py is None:
            self.pivot = Point(0, 0)
        else:
            self.pivot = Point(px, py)
            pass

        self.max_hp = 6
        self.curr_hp = 2

        self.object_width = 26
        self.object_height = 25

        self.image_start_point = [Point(0, self.image.h - self.object_height), Point(28, self.image.h - self.object_height),
                                  Point(54, self.image.h - self.object_height), Point(80, self.image.h - self.object_height)]
        self.frame = 0
        self.max_frame = 4

        self.bt = None
        self.timer = 0.5
        self.build_behavior_tree()

        self.jump_start_pivot = Point(self.pivot.x, self.pivot.y)
        self.check_jumping = False

    def jump(self):

        if self.check_jumping is False:
            self.check_jumping = True
            self.jump_start_pivot = Point(self.pivot.x, self.pivot.y)

        self.timer -= GameFrameWork.frame_time
        if self.timer < 0:
            self.timer += 0.5
            self.pivot = Point(self.jump_start_pivot.x, self.jump_start_pivot.y)
        elif self.timer < 0.1:
            self.pivot.y -= 2
        elif self.timer < 0.2:
            self.pivot.y += 2
        elif self.timer < 0.5:
            pass

        return BehaviorTree.SUCCESS
        pass

    def update(self):
        self.frame = (self.frame + self.max_frame * ACTION_PER_TIME * GameFrameWork.frame_time) % self.max_frame
        self.bt.run()
        pass

    def build_behavior_tree(self):
        jump_node = LeafNode("Jump_Mark_Time", self.jump)

        root_node = SelectorNode("Root")
        root_node.add_child(jump_node)
        self.bt = BehaviorTree(root_node)
        pass

    pass


class Slime_Blue(Monster):
    pass


class Skeleton_White(Monster):
    pass


class Bat_Basic(Monster):
    pass

