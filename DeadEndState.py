import pico2d
import GameFrameWork
import GameWorldManager
import random
import MainState

import Camera

name = "DeadEndState"
dead_font = None
dead_message_font = None
dead_score_font = None

dead_voice = []
dead_sfx = None

SHADOW_RANGE = 5

camera = None
get_damage_image = None
get_damage_timer = 25


def enter_state():
    global dead_font
    global dead_voice
    global dead_sfx
    global dead_message_font
    global dead_score_font

    global camera
    global get_damage_image

    camera = MainState.camera
    camera.shake_camera()
    get_damage_image = Camera.HitImage()

    GameWorldManager.add_object(get_damage_image, MainState.LAYER_MESSAGE)

    dead_font = pico2d.load_font('resource\\NecroSans.ttf', 82)
    dead_score_font = pico2d.load_font('resource\\NecroSans.ttf', 50)
    dead_message_font = pico2d.load_font('resource\\malgunbd.ttf', 30)

    dead_sfx = pico2d.load_wav('resource\\sound\\hit_sound\\sfx_player_death_ST.wav')
    dead_sfx.set_volume(100)

    for i in range(3):
        bgm = pico2d.load_wav('resource\\sound\\hit_sound\\vo_cad_death_0' + str(i + 1) + '.wav')
        bgm.set_volume(90)
        dead_voice.append(bgm)

    ran_val = random.randint(0, 2)
    dead_sfx.play()
    dead_voice[ran_val].play()
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
    pass


def update():
    global get_damage_timer
    global get_damage_image

    for game_object, object_layer in GameWorldManager.all_objects():
        game_object.update()
        pass
    MainState.update_blackboard()
    
    get_damage_timer -= 1
    if get_damage_timer < 0:
        GameWorldManager.remove_object(get_damage_image)
    pass


def draw():

    pico2d.clear_canvas()

    for game_object, object_layer in GameWorldManager.all_objects():
        game_object.draw()

    dead_font.draw(pico2d.get_canvas_width() // 2 + SHADOW_RANGE, pico2d.get_canvas_height() // 2 + pico2d.get_canvas_height() // 4 - SHADOW_RANGE, str("GAME OVER"), (0, 0, 0))
    dead_font.draw(pico2d.get_canvas_width() // 2, pico2d.get_canvas_height() // 2 + pico2d.get_canvas_height() // 4, str("GAME OVER"), (255, 255, 255))

    dead_font.draw(500 + SHADOW_RANGE, pico2d.get_canvas_height() // 2 - SHADOW_RANGE, str("Game Score : "), (0, 0, 0))
    dead_font.draw(500, pico2d.get_canvas_height() // 2, str("Game Score : "), (255, 255, 255))

    dead_score_font.draw(pico2d.get_canvas_width() - 500 + SHADOW_RANGE, pico2d.get_canvas_height() // 2 - SHADOW_RANGE, "%d" % MainState.BlackBoard['player']['holding_gold'], (0, 0, 0))
    dead_score_font.draw(pico2d.get_canvas_width() - 500, pico2d.get_canvas_height() // 2, "%d" % MainState.BlackBoard['player']['holding_gold'], (55, 55, 55))

    dead_message_font.draw(pico2d.get_canvas_width() // 2 + SHADOW_RANGE, pico2d.get_canvas_height() // 8 - SHADOW_RANGE, str("게임을 종료하려면 ESC 키를 누르세요"), (0, 0, 0))
    dead_message_font.draw(pico2d.get_canvas_width() // 2, pico2d.get_canvas_height() // 8, str("게임을 종료하려면 ESC 키를 누르세요"), (255, 255, 255))

    pico2d.update_canvas()
    pass

