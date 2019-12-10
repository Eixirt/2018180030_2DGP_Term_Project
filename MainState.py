import pico2d
import GameFrameWork
import GameWorldManager
import copy
import random

import Camera

import Player
import Game_UI

import Dropped_Item
import Monster
import Map_First_Stage

import DeadEndState
import ClearState

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
    rect_constant_x = object_pivot_x % 50
    rect_constant_y = object_pivot_y % 50
    if rect_constant_x < 25:
        object_pivot_x -= rect_constant_x
    elif rect_constant_x > 25:
        object_pivot_x += (50 - rect_constant_x)

    if rect_constant_y < 25:
        object_pivot_y -= rect_constant_y
    elif rect_constant_y > 25:
        object_pivot_y += (50 - rect_constant_y)

    rect = [(object_pivot_x // 50) * 50 - 25, (object_pivot_y // 50) * 50 - 25, (object_pivot_x // 50 + 1) * 50 - 25, (object_pivot_y // 50 + 1) * 50 - 25]
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
    elif move_dir == '':
        moving_object_rect = call_object_in_rect(moving_object_pivot.x, moving_object_pivot.y)

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
ui_heartbeat = None

curr_stage = None

# 블랙보드 위치 수정 요망
BlackBoard = {'player': {'x': None, 'y': None,
                         'curr_hp': None, 'max_hp': None,
                         'holding_gold': None, 'holding_diamond': None,
                         'equip_shovel': None, 'equip_weapon': None},
              'camera': {'camera_left': None, 'camera_bottom': None}}

# layer 0: Background Objects
# layer 1: Map Objects
# layer 2: Monster Objects
# layer 3: Player Objects
# layer 4: Map-UnderWall Objects
# layer 5: UI Objects
# layer 6: Hit Image and Message
LAYER_BACKGROUND, LAYER_MAP, LAYER_EXIT, LAYER_ITEM, LAYER_MONSTER, LAYER_PLAYER, LAYER_UNDER_WALL, LAYER_UI, LAYER_MESSAGE = range(9)

# sound


def update_blackboard():
    global BlackBoard
    global player_cadence
    global camera

    if player_cadence is not None:
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
# layer 2: Monster Objects
# layer 3: Player Objects
# layer 4: Map-UnderWall Objects
# layer 5: UI Objects
# layer 6: Hit Image and Message


fade_timer = 1.0
fade_image = None


def enter_state():
    global fade_image
    # fade image
    fade_image = pico2d.load_image('resource\\black_background.png')

    # 플레이어
    global player_cadence
    player_cadence = Player.Player_Cadence()
    GameWorldManager.add_object(player_cadence, LAYER_PLAYER)

    # UI
    global ui_heart, ui_money, ui_equip, ui_heartbeat
    ui_heart = Game_UI.UI_Player_Hp()
    ui_money = Game_UI.UI_Player_Money()
    ui_equip = Game_UI.UI_Player_Equip()
    ui_heartbeat = Game_UI.UI_HEARTBEAT()
    GameWorldManager.add_object(ui_heart, LAYER_UI)
    GameWorldManager.add_object(ui_money, LAYER_UI)
    GameWorldManager.add_object(ui_equip, LAYER_UI)
    GameWorldManager.add_object(ui_heartbeat, LAYER_UI)

    # 배경
    # global background
    # background = BackGround.Scrolled_Background()
    # GameWorldManager.add_object(background, 0)

    # background.set_focus_object(player_cadence)
    # player_cadence.set_background(background)

    # 카메라
    global camera
    camera = Camera.Camera()
    GameWorldManager.add_object(camera, LAYER_BACKGROUND)

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
    global player_cadence
    global camera
    update_blackboard()
    camera.set_focus_object(None)
    GameWorldManager.remove_object(player_cadence)
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
            pass
        else:
            player_cadence.handle_event(curr_event)

        pass
    pass


def update():
    global fade_timer

    if fade_timer > 0.0:
        fade_timer -= GameFrameWork.frame_time * 1.2
        if fade_timer < 0.0:
            fade_timer = 0.0

    for game_object, object_layer in GameWorldManager.all_objects():
        game_object.update()

    curr_stage.update()
    update_blackboard()

    # 충돌체크
    check_collide_player_and_wall()
    check_collide_player_and_monster()
    check_collide_player_attack_and_monster()
    check_collide_monster_and_wall()

    pass


def check_collide_player_and_wall():
    global player_cadence
    running_collide_chest = False
    # and player_cadence.check_moving_collide is False
    if player_cadence.check_jumping is True and player_cadence.check_moving_collide is False:

        if player_cadence.jump_dir == 'RIGHT':
            for wall in curr_stage.wall_list:
                if check_collide_interaction(player_cadence.start_point, wall.pivot, 'RIGHT'):
                    player_cadence.check_jumping = False
                    player_cadence.pivot = copy.copy(player_cadence.start_point)
                    break
                pass
            if check_collide_interaction(player_cadence.start_point, curr_stage.next_floor.pivot, 'RIGHT') and curr_stage.next_floor.running_open:
                GameFrameWork.push_state(ClearState)
                pass
            elif check_collide_interaction(player_cadence.start_point, curr_stage.next_floor.pivot, 'RIGHT'):
                player_cadence.check_jumping = False
                player_cadence.pivot = copy.copy(player_cadence.start_point)
                pass

            for chest in curr_stage.chest_list:
                if check_collide_interaction(player_cadence.start_point, chest.pivot, 'RIGHT'):
                    player_cadence.check_jumping = False
                    player_cadence.pivot = copy.copy(player_cadence.start_point)
                    chest.chest_open()
                    curr_stage.chest_list.remove(chest)
                    if chest.chest_item == Dropped_Item.DroppedItem_Type['ITEM_HEAL']:
                        drop_item = Dropped_Item.Heal_Item(chest.chest_item, chest.pivot.x, chest.pivot.y)
                        pass
                    else:
                        drop_item = Dropped_Item.Torch_Item(chest.chest_item, chest.pivot.x, chest.pivot.y)
                    curr_stage.item_list.append(drop_item)
                    GameWorldManager.add_object(drop_item, LAYER_ITEM)

                    GameWorldManager.remove_object(chest)
                    running_collide_chest = True
                    break
                pass

            if running_collide_chest is False:
                for item in curr_stage.item_list:
                    if check_collide_interaction(player_cadence.start_point, item.pivot, 'RIGHT'):
                        item.play_get_item_sound()
                        item.get_item(player_cadence)
                        player_cadence.holding_gold += 10
                        curr_stage.item_list.remove(item)
                        GameWorldManager.remove_object(item)
                        pass
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
            if check_collide_interaction(player_cadence.start_point, curr_stage.next_floor.pivot, 'LEFT') and curr_stage.next_floor.running_open:
                GameFrameWork.push_state(ClearState)
                pass
            elif check_collide_interaction(player_cadence.start_point, curr_stage.next_floor.pivot, 'LEFT'):
                player_cadence.check_jumping = False
                player_cadence.pivot = copy.copy(player_cadence.start_point)
                pass

            for chest in curr_stage.chest_list:
                if check_collide_interaction(player_cadence.start_point, chest.pivot, 'LEFT'):
                    player_cadence.check_jumping = False
                    player_cadence.pivot = copy.copy(player_cadence.start_point)
                    chest.chest_open()
                    curr_stage.chest_list.remove(chest)
                    if chest.chest_item == Dropped_Item.DroppedItem_Type['ITEM_HEAL']:
                        drop_item = Dropped_Item.Heal_Item(chest.chest_item, chest.pivot.x, chest.pivot.y)
                        pass
                    else:
                        drop_item = Dropped_Item.Torch_Item(chest.chest_item, chest.pivot.x, chest.pivot.y)
                    curr_stage.item_list.append(drop_item)
                    GameWorldManager.add_object(drop_item, LAYER_ITEM)

                    GameWorldManager.remove_object(chest)
                    running_collide_chest = True
                    break
                pass

            if running_collide_chest is False:
                for item in curr_stage.item_list:
                    if check_collide_interaction(player_cadence.start_point, item.pivot, 'LEFT'):
                        item.play_get_item_sound()
                        item.get_item(player_cadence)
                        player_cadence.holding_gold += 10
                        curr_stage.item_list.remove(item)
                        GameWorldManager.remove_object(item)
                        pass
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
            if check_collide_interaction(player_cadence.start_point, curr_stage.next_floor.pivot, 'UP') and curr_stage.next_floor.running_open:
                GameFrameWork.push_state(ClearState)

            elif check_collide_interaction(player_cadence.start_point, curr_stage.next_floor.pivot, 'UP'):
                player_cadence.check_jumping = False
                player_cadence.pivot = copy.copy(player_cadence.start_point)
                pass

            for chest in curr_stage.chest_list:
                if check_collide_interaction(player_cadence.start_point, chest.pivot, 'UP'):
                    player_cadence.check_jumping = False
                    player_cadence.pivot = copy.copy(player_cadence.start_point)
                    chest.chest_open()
                    curr_stage.chest_list.remove(chest)
                    if chest.chest_item == Dropped_Item.DroppedItem_Type['ITEM_HEAL']:
                        drop_item = Dropped_Item.Heal_Item(chest.chest_item, chest.pivot.x, chest.pivot.y)
                        pass
                    else:
                        drop_item = Dropped_Item.Torch_Item(chest.chest_item, chest.pivot.x, chest.pivot.y)
                    curr_stage.item_list.append(drop_item)
                    GameWorldManager.add_object(drop_item, LAYER_ITEM)

                    GameWorldManager.remove_object(chest)
                    running_collide_chest = True
                    break
                pass

            if running_collide_chest is False:
                for item in curr_stage.item_list:
                    if check_collide_interaction(player_cadence.start_point, item.pivot, 'UP'):
                        item.play_get_item_sound()
                        item.get_item(player_cadence)
                        player_cadence.holding_gold += 10
                        curr_stage.item_list.remove(item)
                        GameWorldManager.remove_object(item)
                        pass
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
            if check_collide_interaction(player_cadence.start_point, curr_stage.next_floor.pivot, 'DOWN') and curr_stage.next_floor.running_open:
                GameFrameWork.push_state(ClearState)
            elif check_collide_interaction(player_cadence.start_point, curr_stage.next_floor.pivot, 'DOWN'):
                player_cadence.check_jumping = False
                player_cadence.pivot = copy.copy(player_cadence.start_point)
                pass

            for chest in curr_stage.chest_list:
                if check_collide_interaction(player_cadence.start_point, chest.pivot, 'DOWN'):
                    player_cadence.check_jumping = False
                    player_cadence.pivot = copy.copy(player_cadence.start_point)
                    chest.chest_open()
                    curr_stage.chest_list.remove(chest)

                    if chest.chest_item == Dropped_Item.DroppedItem_Type['ITEM_HEAL']:
                        drop_item = Dropped_Item.Heal_Item(chest.chest_item, chest.pivot.x, chest.pivot.y)
                        pass
                    else:
                        drop_item = Dropped_Item.Torch_Item(chest.chest_item, chest.pivot.x, chest.pivot.y)
                    curr_stage.item_list.append(drop_item)
                    GameWorldManager.add_object(drop_item, LAYER_ITEM)

                    GameWorldManager.remove_object(chest)
                    running_collide_chest = True
                    break
                pass

            if running_collide_chest is False:
                for item in curr_stage.item_list:
                    if check_collide_interaction(player_cadence.start_point, item.pivot, 'DOWN'):
                        item.play_get_item_sound()
                        item.get_item(player_cadence)
                        player_cadence.holding_gold += 10
                        curr_stage.item_list.remove(item)
                        GameWorldManager.remove_object(item)
                        pass
                    pass

            player_cadence.check_moving_collide = True
            pass

        pass
    pass


def check_collide_player_and_monster():
    mob_pivot = None
    if player_cadence.check_jumping is True:
        if player_cadence.jump_dir == 'RIGHT':
            for mob in curr_stage.monster_list:
                if mob.type == Monster.Monster_Type['MONSTER_SLIME_GREEN']:
                    mob_pivot = mob.start_pivot
                else:
                    mob_pivot = mob.pivot

                if check_collide_interaction(player_cadence.start_point, mob_pivot, 'RIGHT'):
                    player_cadence.check_jumping = False
                    player_cadence.pivot = copy.copy(player_cadence.start_point)
                    player_cadence.get_damage(mob.damage)
                    break
                pass
            player_cadence.check_moving_collide = True
            pass

        elif player_cadence.jump_dir == 'LEFT':
            for mob in curr_stage.monster_list:

                if mob.type == Monster.Monster_Type['MONSTER_SLIME_GREEN']:
                    mob_pivot = mob.start_pivot
                else:
                    mob_pivot = mob.pivot

                if check_collide_interaction(player_cadence.start_point, mob_pivot, 'LEFT'):
                    player_cadence.check_jumping = False
                    player_cadence.pivot = copy.copy(player_cadence.start_point)
                    player_cadence.get_damage(mob.damage)
                    break
                pass
            player_cadence.check_moving_collide = True
            pass

        elif player_cadence.jump_dir == 'UP':
            for mob in curr_stage.monster_list:

                if mob.type == Monster.Monster_Type['MONSTER_SLIME_GREEN']:
                    mob_pivot = mob.start_pivot
                else:
                    mob_pivot = mob.pivot

                if check_collide_interaction(player_cadence.start_point, mob_pivot, 'UP'):
                    player_cadence.check_jumping = False
                    player_cadence.pivot = copy.copy(player_cadence.start_point)
                    player_cadence.get_damage(mob.damage)
                    break
                pass
            player_cadence.check_moving_collide = True
            pass

        elif player_cadence.jump_dir == 'DOWN':
            for mob in curr_stage.monster_list:

                if mob.type == Monster.Monster_Type['MONSTER_SLIME_GREEN']:
                    mob_pivot = mob.start_pivot
                else:
                    mob_pivot = mob.pivot

                if check_collide_interaction(player_cadence.start_point, mob_pivot, 'DOWN'):
                    player_cadence.check_jumping = False
                    player_cadence.pivot = copy.copy(player_cadence.start_point)
                    player_cadence.get_damage(mob.damage)
                    break
                pass
            player_cadence.check_moving_collide = True
            pass
    pass


def check_collide_player_attack_and_monster():
    player_attack = player_cadence.equip_weapon_object
    mob_pivot = None
    if player_attack.check_attack is True and player_attack.timer >= 0 and player_attack.check_possible_attack is True:
        for mob in curr_stage.monster_list:
            if mob.type == Monster.Monster_Type['MONSTER_SLIME_GREEN']:
                mob_pivot = mob.start_pivot
            else:
                mob_pivot = mob.pivot

            if check_collide_interaction(player_attack.pivot, mob_pivot, ''):
                mob.curr_hp -= player_attack.damage
                if mob.type == Monster.Monster_Type['MONSTER_BANSHEE']:
                    if mob.curr_hp <= mob.max_hp / 2 and mob.running_rage is False:
                        mob.rage()
                        mob.running_rage = True
                        mob.object_width = mob.object_rage_width
                    pass

                if mob.curr_hp > 0 and mob.type != Monster.Monster_Type['MONSTER_BANSHEE']:
                    mob.hit_sound.play()
                elif mob.curr_hp > 0 and mob.type == Monster.Monster_Type['MONSTER_BANSHEE']:
                    ran_hit_sound = random.randint(0, 2)
                    mob.hit_sound[ran_hit_sound].play()
                player_attack.check_possible_attack = False
                break

            pass
        pass
    pass


def check_collide_monster_and_wall():
    for mob in curr_stage.monster_list:
        if mob.type == Monster.Monster_Type['MONSTER_BAT_BASIC']:
            pass
        pass
    pass

# layer 0: Background Objects
# layer 1: Map Objects
# layer 2: Monster Objects
# layer 3: Player Objects
# layer 4: Map-UnderWall Objects
# layer 5: UI Objects
# layer 6: Hit Image and Message


def draw():
    global camera

    pico2d.clear_canvas()
    for game_object, object_layer in GameWorldManager.all_objects():
        if object_layer == LAYER_BACKGROUND or object_layer == LAYER_MESSAGE or object_layer == LAYER_UI:
            game_object.draw()
            pass

        else:
            if camera.check_object_in_camera(game_object.pivot.x, game_object.pivot.y):
                view_val = check_object_view(game_object.pivot.x, game_object.pivot.y)
                if view_val == 0:
                    game_object.alpha_value = 0.0
                    game_object.draw()
                    pass
                elif view_val == 1:
                    game_object.alpha_value = 0.3
                    game_object.draw()
                    pass
                elif view_val == 2:
                    game_object.alpha_value = 0.8
                    game_object.draw()
                else:
                    game_object.alpha_value = 1.0
                    pass

    fade_image.opacify(fade_timer)
    fade_image.clip_draw(0, 0, pico2d.get_canvas_width(), pico2d.get_canvas_height(), 0, 0, pico2d.get_canvas_width() * 3, pico2d.get_canvas_height() * 3)

    pico2d.update_canvas()
    pass


def check_object_view(object_pivot_x, object_pivot_y):
    global player_cadence

    obj_range_x = (player_cadence.pivot.x - object_pivot_x)
    obj_range_y = (player_cadence.pivot.y - object_pivot_y)

    obj_range_pow = obj_range_x * obj_range_x + obj_range_y * obj_range_y

    RANGE_SIZE = 30

    view_range = (player_cadence.view_range * RANGE_SIZE) * (player_cadence.view_range * RANGE_SIZE)

    if obj_range_pow < view_range:
        return 0

    view_range = ((player_cadence.view_range + 1) * RANGE_SIZE) * ((player_cadence.view_range + 1) * RANGE_SIZE)
    if obj_range_pow < view_range:
        return 1

    view_range = ((player_cadence.view_range + 2) * RANGE_SIZE) * ((player_cadence.view_range + 2) * RANGE_SIZE)
    if obj_range_pow < view_range:
        return 2

    return 3
    pass

