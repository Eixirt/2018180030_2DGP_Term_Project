import pico2d
import GameFrameWork
import GameWorldManager

import Player
import Game_UI
import BackGround

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


# layer 0: Background Objects
# layer 1: Map Objects
# layer 2: Foreground Objects
# layer 3: UI Objects

player_cadence = None
ui_heart = None
ui_money = None
ui_equip = None

BlackBoard = {'player': {'x': None, 'y': None,
                         'curr_hp': None, 'max_hp': None,
                         'holding_gold': None, 'holding_diamond': None,
                         'equip_shovel': None, 'equip_weapon': None}}


def update_blackboard():
    global BlackBoard

    BlackBoard['player']['x'] = player_cadence.pivot.x
    BlackBoard['player']['y'] = player_cadence.pivot.y
    BlackBoard['player']['curr_hp'] = player_cadence.curr_hp
    BlackBoard['player']['max_hp'] = player_cadence.max_hp
    BlackBoard['player']['holding_gold'] = player_cadence.holding_gold
    BlackBoard['player']['holding_diamond'] = player_cadence.holding_diamond
    BlackBoard['player']['equip_shovel'] = player_cadence.equip_shovel
    BlackBoard['player']['equip_weapon'] = player_cadence.equip_weapon
    pass


def enter_state():
    global player_cadence
    global ui_heart, ui_money, ui_equip
    global BlackBoard

    player_cadence = Player.Player_Cadence()
    ui_heart = Game_UI.UI_Player_Hp()
    ui_money = Game_UI.UI_Player_Money()
    ui_equip = Game_UI.UI_Player_Equip()

    GameWorldManager.add_object(player_cadence, 2)
    GameWorldManager.add_object(ui_heart, 3)
    GameWorldManager.add_object(ui_money, 3)
    GameWorldManager.add_object(ui_equip, 3)

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
    for game_object in GameWorldManager.all_objects():
        game_object.update()

    update_blackboard()
    # 충돌체크

    pass


def draw():
    pico2d.clear_canvas()
    for game_object in GameWorldManager.all_objects():
        game_object.draw()

    pico2d.update_canvas()
    pass

