import pico2d
import ctypes
import math

CANVAS_WIDTH, CANVAS_HEIGHT = 1280, 720

# 수직동기화 sync = False
pico2d.open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT, False, False)
character_player = pico2d.load_image('resource\\Character_Player.png')


# Frame 구조체
class Point(ctypes.Structure):
    _fields_ = [("x", ctypes.c_int),
                ("y", ctypes.c_int)]


class Image_Origin_Size(ctypes.Structure):
    _fields_ = [("width", ctypes.c_int),
                ("height", ctypes.c_int)]


class Dagger_Attack:
    def __init__(self):
        self.image = pico2d.load_image('resource\\Effect_Weapon.png')
        self.pivot = Point(700, 100)
        self.frame = 0
        self.image_multiple_size = 2
        self.rad = 0
        self.flip = ''

    def attack_direction(self, key):
        if key == 'UP':
            self.rad = math.pi / 2
            self.flip = 'v'
        elif key == 'LEFT':
            self.rad = math.pi
            self.flip = 'v'
        elif key == 'DOWN':
            self.rad = 1.5 * math.pi
            self.flip = ''
        elif key == 'RIGHT':
            self.rad = 0
            self.flip = ''

    def update(self):
        self.frame = (self.frame + 1) % 3

    def draw(self):
        effect_origin_size = Image_Origin_Size(21, 16)
        self.image.clip_composite_draw(299 + self.frame * effect_origin_size.width, self.image.h - 19 - effect_origin_size.height,
                                       effect_origin_size.width, effect_origin_size.height,
                                       self.rad, self.flip,
                                       self.pivot.x - 100, self.pivot.y + effect_origin_size.height * 0.5 * self.image_multiple_size,
                                       effect_origin_size.width * self.image_multiple_size, effect_origin_size.height * self.image_multiple_size)


class Player:
    def __init__(self):
        self.image = pico2d.load_image('resource\\Character_Player.png')
        self.pivot = Point(500, 100)
        self.frame = Point(0, 0)
        self.image_multiple_size = 2
        self.rad = 0
        self.flip = ''

    def jump(self, key):
        if key == 'w':
            self.pivot.y += 50
        elif key == 'a':
            self.pivot.x -= 50
            self.rad = math.pi
            self.flip = 'v'
        elif key == 's':
            self.pivot.y -= 50
        elif key == 'd':
            self.pivot.x += 50
            self.rad = 0
            self.flip = ''

    def update(self):
        self.frame.x = (self.frame.x + 1) % 4
        if self.frame.x == 0:
            self.frame.y = (self.frame.y + 1) % 2

    def draw(self):
        # 몸
        body_origin_size = Image_Origin_Size(24, 14)
        self.image.clip_composite_draw(self.frame.x * body_origin_size.width, self.image.h - 58 - body_origin_size.height,
                                       body_origin_size.width, body_origin_size.height,
                                       self.rad, self.flip,
                                       self.pivot.x, self.pivot.y + 0.5 * body_origin_size.height * self.image_multiple_size,
                                       body_origin_size.width * self.image_multiple_size, body_origin_size.height * self.image_multiple_size)
        # 머리
        head_origin_size = Image_Origin_Size(24, 12)

        # 머리와 몸 간의 간격 차이
        head_interval = body_origin_size.height * self.image_multiple_size - 3 * self.image_multiple_size
        self.image.clip_composite_draw(self.frame.x * head_origin_size.width, self.image.h - head_origin_size.height - 24 * self.frame.y,
                                       head_origin_size.width, head_origin_size.height,
                                       self.rad, self.flip,
                                       self.pivot.x, self.pivot.y + 0.5 * head_origin_size.height * self.image_multiple_size + head_interval,
                                       head_origin_size.width * self.image_multiple_size, head_origin_size.height * self.image_multiple_size)


player = Player()
dagger = Dagger_Attack()
x = 400
frame1 = 0
frame3 = 0
is_up = True
running = True


def handle_events():
    global running
    global player
    global dagger
    events = pico2d.get_events()
    for event in events:
        if event.type == pico2d.SDL_QUIT:
            running = False
        elif event.type == pico2d.SDL_KEYDOWN:
            if event.key == pico2d.SDLK_ESCAPE:
                running = False

            elif event.key == pico2d.SDLK_w:
                player.jump('w')
            elif event.key == pico2d.SDLK_a:
                player.jump('a')
            elif event.key == pico2d.SDLK_s:
                player.jump('s')
            elif event.key == pico2d.SDLK_d:
                player.jump('d')

            if event.key == pico2d.SDLK_LEFT:
                dagger.attack_direction('LEFT')
            elif event.key == pico2d.SDLK_RIGHT:
                dagger.attack_direction('RIGHT')
            elif event.key == pico2d.SDLK_UP:
                dagger.attack_direction('UP')
            elif event.key == pico2d.SDLK_DOWN:
                dagger.attack_direction('DOWN')


while running:
    pico2d.clear_canvas()

    handle_events()

    player.draw()
    player.update()

    dagger.draw()
    dagger.update()

    pico2d.update_canvas()

    pico2d.delay(0.1)
    # pico2d.get_events()

pico2d.close_canvas()
