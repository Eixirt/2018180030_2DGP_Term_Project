import pico2d
import GameFrameWork
import GameWorldManager
import copy

name = "StartState"


def enter_state():
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
    for game_object, object_layer in GameWorldManager.all_objects():
        game_object.update()

    pass


def draw():
    pico2d.clear_canvas()

    for game_object, object_layer in GameWorldManager.all_objects():
        game_object.draw()

    pico2d.update_canvas()
    pass

