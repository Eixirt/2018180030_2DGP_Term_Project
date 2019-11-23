import pico2d
import GameFrameWork
import GameWorldManager

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

