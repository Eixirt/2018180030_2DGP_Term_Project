import pico2d
import GameFrameWork
import GameWorldManager
import copy

import Camera

import Player
import Game_UI

import Map_First_Stage

name = "MainState"


def check_collide(a, b):
    # fill here
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b:
        return False
    if right_a < left_b:
        return False
    if top_a < bottom_b:
        return False
    if bottom_a > top_b:
        return False

    return True
    pass


def call_object_in_rect(object_pivot_x, object_pivot_y):
    # left, bottom, right, top
    rect = [(object_pivot_x // 50) * 50 - 25, (object_pivot_y // 50 + 1) * 50 - 25, (object_pivot_x // 50 + 1) * 50 - 25, (object_pivot_y // 50 + 2) * 50 - 25]
    # print(str(rect[0]) + ", " + str(rect[1]) + ", " + str(rect[2]) + ", " + str(rect[3]))
    return rect
    pass


def check_collide_interaction(moving_object_pivot, fixed_object_pivot, move_dir):
    moving_object_rect = []
    if move_dir == 'LEFT':
        moving_object_rect = call_object_in_rect(moving_object_pivot.x - 50, moving_object_pivot.y)
        pass
    elif move_dir == 'RIGHT':
        moving_object_rect = call_object_in_rect(moving_object_pivot.x + 50, moving_object_pivot.y)
        pass
    elif move_dir == 'UP':
        moving_object_rect = call_object_in_rect(moving_object_pivot.x, moving_object_pivot.y + 50)
        pass
    elif move_dir == 'DOWN':
        moving_object_rect = call_object_in_rect(moving_object_pivot.x, moving_object_pivot.y - 50)
        pass

    if (moving_object_rect[0] < fixed_object_pivot.x) and (fixed_object_pivot.x < moving_object_rect[2]) and \
            (moving_object_rect[1] < fixed_object_pivot.y) and (fixed_object_pivot.y < moving_object_rect[3]):
        return True
    else:
        return False
    pass


camera = None

player_cadence = None
ui_heart = None
ui_money = None
ui_equip = None

curr_stage = None

BlackBoard = {'player': {'x': None, 'y': None,
                         'curr_hp': None, 'max_hp': None,
                         'holding_gold': None, 'holding_diamond': None,
                         'equip_shovel': None, 'equip_weapon': None},
              'camera': {'camera_left': None, 'camera_bottom': None}}


def update_blackboard():
    global BlackBoard
    global player_cadence
    global camera

    BlackBoard['player']['x'] = player_cadence.pivot.x
    BlackBoard['player']['y'] = player_cadence.pivot.y
    BlackBoard['player']['curr_hp'] = player_cadence.curr_hp
    BlackBoard['player']['max_hp'] = player_cadence.max_hp
    BlackBoard['player']['holding_gold'] = player_cadence.holding_gold
    BlackBoard['player']['holding_diamond'] = player_cadence.holding_diamond
    BlackBoard['player']['equip_shovel'] = player_cadence.equip_shovel
    BlackBoard['player']['equip_weapon'] = player_cadence.equip_weapon

    BlackBoard['camera']['camera_left'] = camera.window_left
    BlackBoard['camera']['camera_bottom'] = camera.window_bottom
    pass

# layer 0: Background Objects
# layer 1: Map Objects
# layer 2: Foreground Objects
# layer 3: UI Objects


def enter_state():
    # 플레이어
    global player_cadence
    player_cadence = Player.Player_Cadence()
    GameWorldManager.add_object(player_cadence, 2)

    # UI
    global ui_heart, ui_money, ui_equip
    ui_heart = Game_UI.UI_Player_Hp()
    ui_money = Game_UI.UI_Player_Money()
    ui_equip = Game_UI.UI_Player_Equip()
    GameWorldManager.add_object(ui_heart, 3)
    GameWorldManager.add_object(ui_money, 3)
    GameWorldManager.add_object(ui_equip, 3)

    # 배경
    # global background
    # background = BackGround.Scrolled_Background()
    # GameWorldManager.add_object(background, 0)

    # background.set_focus_object(player_cadence)
    # player_cadence.set_background(background)

    # 카메라
    global camera
    camera = Camera.Camera()
    GameWorldManager.add_object(camera, 0)

    camera.set_focus_object(player_cadence)

    # 스테이지
    global curr_stage
    curr_stage = Map_First_Stage.FirstStage()

    # BlackBoard Update
    update_blackboard()

    # BackGround.Scrolled_Background.set_focus_object(player_cadence)

    pass


def exit_state():
    GameWorldManager.clear()
    pass


def pause_state():
    pass


def resume_state():
    pass


def handle_events():
    events_list = pico2d.get_events()
    for curr_event in events_list:

        if curr_event.type == pico2d.SDL_QUIT:
            GameFrameWork.quit_state()
        elif curr_event.type == pico2d.SDL_KEYDOWN and curr_event.key == pico2d.SDLK_ESCAPE:
            GameFrameWork.quit_state()
        else:
            player_cadence.handle_event(curr_event)

        pass
    pass


def update():
    for game_object, object_layer in GameWorldManager.all_objects():
        game_object.update()

    update_blackboard()
    # 충돌체크
    check_collide_player_and_wall()
    pass


def check_collide_player_and_wall():
    if player_cadence.check_jumping is True and player_cadence.check_moving_collide is False:

        if player_cadence.jump_dir == 'RIGHT':
            for wall in curr_stage.wall_list:
                if check_collide_interaction(player_cadence.start_point, wall.pivot, 'RIGHT'):
                    player_cadence.check_jumping = False
                    player_cadence.pivot = copy.copy(player_cadence.start_point)
                    break
                pass
            player_cadence.check_moving_collide = True
            pass

        elif player_cadence.jump_dir == 'LEFT':
            for wall in curr_stage.wall_list:
                if check_collide_interaction(player_cadence.start_point, wall.pivot, 'LEFT'):
                    player_cadence.check_jumping = False
                    player_cadence.pivot = copy.copy(player_cadence.start_point)
                    break
                pass
            player_cadence.check_moving_collide = True
            pass

        elif player_cadence.jump_dir == 'UP':
            for wall in curr_stage.wall_list:
                if check_collide_interaction(player_cadence.start_point, wall.pivot, 'UP'):
                    player_cadence.check_jumping = False
                    player_cadence.pivot = copy.copy(player_cadence.start_point)
                    break
                pass
            player_cadence.check_moving_collide = True
            pass

        elif player_cadence.jump_dir == 'DOWN':
            for wall in curr_stage.wall_list:
                if check_collide_interaction(player_cadence.start_point, wall.pivot, 'DOWN'):
                    player_cadence.check_jumping = False
                    player_cadence.pivot = copy.copy(player_cadence.start_point)
                    break
                pass
            player_cadence.check_moving_collide = True
            pass

        pass
    pass

# layer 0: Background Objects
# layer 1: Map Objects
# layer 2: Foreground Objects
# layer 3: UI Objects


def draw():
    global camera
    pico2d.clear_canvas()
    for game_object, object_layer in GameWorldManager.all_objects():
        if object_layer == 0 or object_layer == 3:
            game_object.draw()
            pass

        else:
            if camera.check_object_in_camera(game_object.pivot.x, game_object.pivot.y):
                game_object.draw()

    pico2d.update_canvas()
    pass

