import pico2d
import ctypes
import math

CANVAS_WIDTH, CANVAS_HEIGHT = 1280, 720

pico2d.open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT, False, False)
character_player = pico2d.load_image('resource\\Character_Player.png')


# Frame 구조체
class Point(ctypes.Structure):
    _fields_ = [("x", ctypes.c_int),
                ("y", ctypes.c_int)]


class Image_Origin_Size(ctypes.Structure):
    _fields_ = [("width", ctypes.c_int),
                ("height", ctypes.c_int)]


class UI_Player_Hp:
    def __init__(self):
        self.image = pico2d.load_image('resource\\UI.png')
        self.pivot = Point(920, CANVAS_HEIGHT - 35)
        self.image_multiple_size = 2
        self.curr_hp = 11
        self.max_hp = 14

    def update(self):
        pass

    def draw(self):
        # 하트
        hp_pivot = []
        heart_origin_size = Image_Origin_Size(24, 22)
        for i in range(0, self.max_hp):
            if i % 2 == 0:
                interval_width = 52 * ((i // 2) % 5)
                interval_height = 47 * ((i // 2) // 5)
                hp_pivot = hp_pivot + [Point(self.pivot.x + interval_width, self.pivot.y - interval_height)]

            if i < self.curr_hp:
                if i % 2 == 0 and (i + 2) <= self.curr_hp:
                    # 꽉 찬 하트
                    self.image.clip_draw(0, self.image.h - heart_origin_size.height,
                                         heart_origin_size.width, heart_origin_size.height,
                                         hp_pivot[i // 2].x, hp_pivot[i // 2].y,
                                         heart_origin_size.width * self.image_multiple_size, heart_origin_size.height * self.image_multiple_size)

                elif i % 2 == 0 and i + 1 == self.curr_hp:
                    # 절반의 하트
                    self.image.clip_draw(heart_origin_size.width + 5, self.image.h - heart_origin_size.height,
                                         heart_origin_size.width, heart_origin_size.height,
                                         hp_pivot[i // 2].x, hp_pivot[i // 2].y,
                                         heart_origin_size.width * self.image_multiple_size, heart_origin_size.height * self.image_multiple_size)

            elif i >= self.curr_hp:
                # 빈 하트
                if i % 2 == 0:
                    self.image.clip_draw(heart_origin_size.width * 2 + 10, self.image.h - heart_origin_size.height,
                                         heart_origin_size.width, heart_origin_size.height,
                                         hp_pivot[i // 2].x, hp_pivot[i // 2].y,
                                         heart_origin_size.width * self.image_multiple_size, heart_origin_size.height * self.image_multiple_size)



player_hp = UI_Player_Hp()

x = 400
frame1 = 0
frame3 = 0
is_up = True
running = True


def handle_events():
    global running
    events = pico2d.get_events()
    for event in events:
        if event.type == pico2d.SDL_QUIT:
            running = False
        elif event.type == pico2d.SDL_KEYDOWN:
            if event.key == pico2d.SDLK_ESCAPE:
                running = False


while running:
    pico2d.clear_canvas()

    handle_events()

    player_hp.draw()
    player_hp.update()

    pico2d.update_canvas()

    pico2d.delay(0.1)
    # pico2d.get_events()

pico2d.close_canvas()
