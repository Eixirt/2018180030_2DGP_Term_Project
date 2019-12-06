import pico2d
import GameFrameWork
import GameWorldManager
import MainState

name = "StartState"
image = None


def enter_state():
    global image
    image = pico2d.load_image('resource/start_image.jpg')
    pass


def exit_state():
    global image
    del image
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
        elif curr_event.type == pico2d.SDL_KEYDOWN and curr_event.key == pico2d.SDLK_KP_ENTER:
            GameFrameWork.change_state(MainState)
    pass


def update():
    for game_object, object_layer in GameWorldManager.all_objects():
        game_object.update()

    pass


def draw():
    global image
    pico2d.clear_canvas()

    image.clip_draw(0, 0)

    pico2d.update_canvas()
    pass

