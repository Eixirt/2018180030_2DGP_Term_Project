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


class UI_Player_Money:
    def __init__(self, money_type, val):
        self.image = pico2d.load_image('resource\\UI.png')
        self.font = pico2d.load_font('resource\\2dgp-money-cnt.ttf', 15)
        self.image_multiple_size = 2
        self.money_type = money_type
        if self.money_type == 'gold':
            self.pivot = Point(CANVAS_WIDTH - 90, CANVAS_HEIGHT - 35)
        elif self.money_type == 'diamond':
            self.pivot = Point(CANVAS_WIDTH - 90, CANVAS_HEIGHT - 85)
        self.value = val

    def update(self):
        pass

    def draw(self):
        money_origin_size = 0
        image_start_point = Point(0, 0)

        if self.money_type == 'gold':
            money_origin_size = Image_Origin_Size(20, 20)
            image_start_point = Point(87, self.image.h - 27 - money_origin_size.height)

        elif self.money_type == 'diamond':
            money_origin_size = Image_Origin_Size(25, 20)
            image_start_point = Point(87, self.image.h - money_origin_size.height)

        self.image.clip_draw(image_start_point.x, image_start_point.y,
                             money_origin_size.width, money_origin_size.height,
                             self.pivot.x, self.pivot.y,
                             money_origin_size.width * self.image_multiple_size, money_origin_size.height * self.image_multiple_size)

        money_str = 'x' + str(self.value)
        self.font.draw(self.pivot.x + 28+2, self.pivot.y-3, money_str, (0, 0, 0)) # 그림자
        self.font.draw(self.pivot.x + 28, self.pivot.y, money_str, (255, 255, 255)) # 숫자


player_hp = UI_Player_Hp()
player_gold = UI_Player_Money('gold', 212)
player_dia = UI_Player_Money('diamond', 3)

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
    player_gold.draw()
    player_dia.draw()
    player_hp.update()
    player_gold.update()
    player_dia.update()

    pico2d.update_canvas()

    pico2d.delay(0.1)
    # pico2d.get_events()

pico2d.close_canvas()
