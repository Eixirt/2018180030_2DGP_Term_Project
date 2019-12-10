import pico2d
import GameFrameWork
import GameWorldManager
import random
import MainState

import Camera

name = "ClearState"
clear_font = None
clear_message_font = None
clear_score_font = None

clear_voice = []
clear_sfx = None

SHADOW_RANGE = 5

camera = None
get_damage_image = None
get_damage_timer = 25


def enter_state():
    global clear_font
    global clear_voice
    global clear_sfx
    global clear_message_font
    global clear_score_font

    global camera

    camera = MainState.camera
    camera.shake_camera()

    clear_font = pico2d.load_font('resource\\NecroSans.ttf', 82)
    clear_score_font = pico2d.load_font('resource\\NecroSans.ttf', 50)
    clear_message_font = pico2d.load_font('resource\\malgunbd.ttf', 30)

    clear_sfx = pico2d.load_wav('resource\\sound\\sfx_secretfound.wav')
    clear_sfx.set_volume(100)

    for i in range(3):
        bgm = pico2d.load_wav('resource\\sound\\vo_cad_yeah_0' + str(i + 2) + '.wav')
        bgm.set_volume(90)
        clear_voice.append(bgm)

    ran_val = random.randint(0, 2)
    clear_sfx.play()
    clear_voice[ran_val].play()
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

    clear_font.draw(pico2d.get_canvas_width() // 2 + SHADOW_RANGE, pico2d.get_canvas_height() // 2 + pico2d.get_canvas_height() // 4 - SHADOW_RANGE, str("GAME CLEAR"), (0, 0, 0))
    clear_font.draw(pico2d.get_canvas_width() // 2, pico2d.get_canvas_height() // 2 + pico2d.get_canvas_height() // 4, str("GAME CLEAR"), (255, 255, 255))

    clear_font.draw(500 + SHADOW_RANGE, pico2d.get_canvas_height() // 2 - SHADOW_RANGE, str("Game Score : "), (0, 0, 0))
    clear_font.draw(500, pico2d.get_canvas_height() // 2, str("Game Score : "), (255, 255, 255))

    clear_score_font.draw(pico2d.get_canvas_width() - 500 + SHADOW_RANGE, pico2d.get_canvas_height() // 2 - SHADOW_RANGE, "%d" % MainState.BlackBoard['player']['holding_gold'],
                          (0, 0, 0))
    clear_score_font.draw(pico2d.get_canvas_width() - 500, pico2d.get_canvas_height() // 2, "%d" % MainState.BlackBoard['player']['holding_gold'], (55, 55, 55))

    clear_message_font.draw(pico2d.get_canvas_width() // 2 + SHADOW_RANGE, pico2d.get_canvas_height() // 8 - SHADOW_RANGE, str("게임을 종료하려면 ESC 키를 누르세요"), (0, 0, 0))
    clear_message_font.draw(pico2d.get_canvas_width() // 2, pico2d.get_canvas_height() // 8, str("게임을 종료하려면 ESC 키를 누르세요"), (255, 255, 255))

    pico2d.update_canvas()
    pass

