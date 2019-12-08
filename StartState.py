import pico2d
import GameFrameWork
import GameWorldManager
import MainState

name = "StartState"

image = None
ready_font = None
ready_bgm = None


def enter_state():
    global image
    global ready_font
    global ready_bgm

    image = pico2d.load_image('resource\\start_image.jpg')
    ready_font = pico2d.load_font('resource\\NecroSans.ttf', 20)

    ready_bgm = pico2d.load_music('resource\\sound\\start_bgm.mp3')
    ready_bgm.set_volume(90)
    ready_bgm.play(3)

    pass


def exit_state():
    global image
    global ready_font
    global ready_bgm

    del image
    del ready_font
    del ready_bgm
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
        elif curr_event.type == pico2d.SDL_KEYDOWN and curr_event.key == pico2d.SDLK_RETURN:
            GameFrameWork.change_state(MainState)
    pass


def update():
    for game_object, object_layer in GameWorldManager.all_objects():
        game_object.update()

    pass


def draw():
    global image
    global ready_font

    pico2d.clear_canvas()

    image.draw(pico2d.get_canvas_width()//2, pico2d.get_canvas_height()//2)
    ready_font.draw(pico2d.get_canvas_width()//2, pico2d.get_canvas_height()//2, str("Press Enter"))

    pico2d.update_canvas()
    pass

