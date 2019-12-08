import pico2d
import GameFrameWork
import GameWorldManager
import MainState

name = "StartState"

image = None
ready_font = None
ready_bgm = None
blink_str = 0

fade_timer = 1.0
fade_image = None


def enter_state():
    global fade_image
    global image
    global ready_font
    global ready_bgm

    fade_image = pico2d.load_image('resource\\black_background.png')
    image = pico2d.load_image('resource\\start_image.jpg')
    ready_font = pico2d.load_font('resource\\NecroSans.ttf', 56)

    ready_bgm = pico2d.load_wav('resource\\sound\\start_bgm.wav')
    ready_bgm.set_volume(35)
    ready_bgm.repeat_play()

    pass


def exit_state():
    global fade_image
    global image
    global ready_font
    global ready_bgm

    pico2d.clear_canvas()

    del image
    del ready_font
    del ready_bgm
    del fade_image
    pass


def pause_state():
    pass


def resume_state():
    pass


def handle_events():
    global fade_timer

    events_list = pico2d.get_events()
    for curr_event in events_list:

        if curr_event.type == pico2d.SDL_QUIT:
            GameFrameWork.quit_state()
        elif curr_event.type == pico2d.SDL_KEYDOWN and curr_event.key == pico2d.SDLK_ESCAPE:
            GameFrameWork.quit_state()
        elif curr_event.type == pico2d.SDL_KEYDOWN and curr_event.key == pico2d.SDLK_RETURN:
            if fade_timer == 1.0:
                fade_timer -= GameFrameWork.frame_time
    pass


def update():
    global blink_str
    global fade_timer

    for game_object, object_layer in GameWorldManager.all_objects():
        game_object.update()

    blink_str += GameFrameWork.frame_time

    if fade_timer < 1.0:
        fade_timer -= GameFrameWork.frame_time
        if fade_timer < 0.0:
            fade_timer = 0.0
            GameFrameWork.change_state(MainState)
    pass


def draw():
    global fade_image
    global image
    global ready_font
    global blink_str
    global fade_timer

    pico2d.clear_canvas()

    if fade_timer > 0.0:
        image.draw(pico2d.get_canvas_width() // 2, pico2d.get_canvas_height() // 2)

        if blink_str > 1.2:
            blink_str = 0.0
            pass
        elif blink_str <= 0.6:
            pass
        elif blink_str <= 1.2:
            ready_font.draw(pico2d.get_canvas_width()//2, pico2d.get_canvas_height()//2 // 2 // 2, str("Press Enter"))
            pass

    if fade_timer < 0.0:
        fade_timer = 0.0
    fade_image.opacify(1.0 - fade_timer)
    fade_image.clip_draw(0, 0, pico2d.get_canvas_width(), pico2d.get_canvas_height(), 0, 0, pico2d.get_canvas_width() * 3, pico2d.get_canvas_height() * 3)

    pico2d.update_canvas()
    pass

