import pico2d
import ctypes
import copy

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
        self.start_pivot = Point(0, 0)

        self.type = None
        self.curr_hp = None
        self.max_hp = None
        self.damage = None

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

        self.type = Monster_Type['MONSTER_SLIME_GREEN']
        self.max_hp = 2
        self.curr_hp = 2
        self.damage = 1

        self.object_width = 26
        self.object_height = 25

        self.image_start_point = [Point(0, self.image.h - self.object_height), Point(28, self.image.h - self.object_height),
                                  Point(54, self.image.h - self.object_height), Point(80, self.image.h - self.object_height)]
        self.frame = 0
        self.max_frame = 4

        self.bt = None
        self.timer = 0.5
        self.build_behavior_tree()

        self.start_pivot = Point(self.pivot.x, self.pivot.y)
        self.check_jumping = False

    def jump(self):

        if self.check_jumping is False:
            self.check_jumping = True
            self.start_pivot = Point(self.pivot.x, self.pivot.y)

        self.timer -= GameFrameWork.frame_time
        if self.timer < 0:
            self.timer += 0.5
            self.pivot = Point(self.start_pivot.x, self.start_pivot.y)
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
    image = None
    MOVE_TIMER = 25

    def __init__(self, px=None, py=None):
        super().__init__()

        if Bat_Basic.image is None:
            Bat_Basic.image = pico2d.load_image('resource\\Monster_Bat.png')
            pass

        if px is None and py is None:
            self.pivot = Point(0, 0)
        else:
            self.pivot = Point(px, py)
            pass

        self.type = Monster_Type['MONSTER_BAT_BASIC']
        self.max_hp = 1
        self.curr_hp = 1
        self.damage = 1

        self.object_width = 24
        self.object_height = 18

        self.image_start_point = [Point(2, self.image.h - self.object_height), Point(23, self.image.h - self.object_height),
                                  Point(48, self.image.h - self.object_height), Point(72, self.image.h - self.object_height),
                                  Point(72, self.image.h - self.object_height), Point(72, self.image.h - self.object_height), Point(72, self.image.h - self.object_height)]
        self.frame = 0
        self.max_frame = 7

        self.dir = None

        self.start_pivot = Point(self.pivot.x, self.pivot.y)
        self.move_timer = Bat_Basic.MOVE_TIMER

        self.bt = None
        self.build_behavior_tree()

    # 플레이어를 추격하기위해 다음 포지션 결정
    def set_next_position_to_chase_player(self):
        self.start_pivot = Point(self.pivot.x, self.pivot.y)

        get_player_pivot = Point(copy.copy(MainState.BlackBoard['player']['x']), copy.copy(MainState.BlackBoard['player']['y']))
        player_rect = MainState.call_object_in_rect(get_player_pivot.x, get_player_pivot.y)
        monster_rect = MainState.call_object_in_rect(self.start_pivot.x, self.start_pivot.y)

        self.move_timer = Bat_Basic.MOVE_TIMER

        check_collide = [False, False, False, False]

        if ((player_rect[0] + player_rect[2]) // 2) < ((monster_rect[0] + monster_rect[2]) // 2):
            for wall in MainState.curr_stage.wall_list:
                if MainState.check_collide_interaction(self.start_pivot, wall.pivot, 'LEFT'):
                    check_collide[0] = True
                    break

            if MainState.check_collide_interaction(self.start_pivot, get_player_pivot, 'LEFT'):
                check_collide[0] = True
                MainState.player_cadence.get_damage(self.damage)
                self.dir = ''
                return BehaviorTree.SUCCESS
                pass

            for mob in MainState.curr_stage.monster_list:
                if MainState.check_collide_interaction(self.start_pivot, mob.pivot, 'LEFT'):
                    self.dir = ''
                    return BehaviorTree.SUCCESS

            if check_collide[0] is False:
                self.dir = 'LEFT'
                return BehaviorTree.SUCCESS
            pass

        if ((player_rect[0] + player_rect[2]) // 2) > ((monster_rect[0] + monster_rect[2]) // 2):
            for wall in MainState.curr_stage.wall_list:
                if MainState.check_collide_interaction(self.start_pivot, wall.pivot, 'RIGHT'):
                    check_collide[1] = True
                    break
                pass

            if MainState.check_collide_interaction(self.start_pivot, get_player_pivot, 'RIGHT'):
                check_collide[0] = True
                MainState.player_cadence.get_damage(self.damage)
                self.dir = ''
                return BehaviorTree.SUCCESS
                pass

            for mob in MainState.curr_stage.monster_list:
                if MainState.check_collide_interaction(self.start_pivot, mob.pivot, 'RIGHT'):
                    self.dir = ''
                    return BehaviorTree.SUCCESS

            if check_collide[1] is False:
                self.dir = 'RIGHT'
                return BehaviorTree.SUCCESS
            pass

        if ((player_rect[1] + player_rect[3]) // 2) < ((monster_rect[1] + monster_rect[3]) // 2):
            for wall in MainState.curr_stage.wall_list:
                if MainState.check_collide_interaction(self.start_pivot, wall.pivot, 'DOWN'):
                    check_collide[2] = True
                    break
                pass

            if MainState.check_collide_interaction(self.start_pivot, get_player_pivot, 'DOWN'):
                check_collide[0] = True
                MainState.player_cadence.get_damage(self.damage)
                self.dir = ''
                return BehaviorTree.SUCCESS
                pass

            for mob in MainState.curr_stage.monster_list:
                if MainState.check_collide_interaction(self.start_pivot, mob.pivot, 'DOWN'):
                    self.dir = ''
                    return BehaviorTree.SUCCESS

            if check_collide[2] is False:
                self.dir = 'DOWN'
                return BehaviorTree.SUCCESS
            pass

        if ((player_rect[1] + player_rect[3]) // 2) > ((monster_rect[1] + monster_rect[3]) // 2):
            for wall in MainState.curr_stage.wall_list:
                if MainState.check_collide_interaction(self.start_pivot, wall.pivot, 'UP'):
                    check_collide[3] = True
                    break
                pass

            if MainState.check_collide_interaction(self.start_pivot, get_player_pivot, 'UP'):
                check_collide[0] = True
                MainState.player_cadence.get_damage(self.damage)
                self.dir = ''
                return BehaviorTree.SUCCESS
                pass

            for mob in MainState.curr_stage.monster_list:
                if MainState.check_collide_interaction(self.start_pivot, mob.pivot, 'UP'):
                    self.dir = ''
                    return BehaviorTree.SUCCESS

            if check_collide[3] is False:
                self.dir = 'UP'
                return BehaviorTree.SUCCESS
            pass

        self.dir = ''
        return BehaviorTree.FAIL
        pass

    def move_to_player(self):
        self.move_timer -= 1
        if self.move_timer >= 0:
            if self.dir == 'LEFT':
                self.pivot.x -= 2
                pass
            elif self.dir == 'RIGHT':
                self.pivot.x += 2
                pass
            elif self.dir == 'UP':
                self.pivot.y += 2
                pass
            elif self.dir == 'DOWN':
                self.pivot.y -= 2
                pass
        if self.move_timer <= -100:
            return BehaviorTree.SUCCESS
        return BehaviorTree.RUNNING
        pass

    def update(self):
        self.frame = (self.frame + self.max_frame * ACTION_PER_TIME * GameFrameWork.frame_time) % self.max_frame
        self.bt.run()
        pass

    def build_behavior_tree(self):
        chase_next_position_node = LeafNode("Chase Next Position", self.set_next_position_to_chase_player)
        chase_player_node = LeafNode("Move to Player", self.move_to_player)
        chase_node = SequenceNode("Chase Player")
        chase_node.add_children(chase_next_position_node, chase_player_node)

        self.bt = BehaviorTree(chase_node)
        pass

    pass

