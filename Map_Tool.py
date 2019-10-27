import pico2d
import ctypes
import enum

CANVAS_WIDTH, CANVAS_HEIGHT = 1280, 720

pico2d.open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT, False, False)
map_data_file = open("map_data.txt", 'w')
black_background = pico2d.load_image('resource\\black_background.jpg')


# Frame 구조체
class Point(ctypes.Structure):
    _fields_ = [("x", ctypes.c_int),
                ("y", ctypes.c_int)]


class Image_Origin_Size(ctypes.Structure):
    _fields_ = [("width", ctypes.c_int),
                ("height", ctypes.c_int)]


class Rectangle(ctypes.Structure):
    _fields_ = [("left", ctypes.c_int), ("bottom", ctypes.c_int),
                ("right", ctypes.c_int), ("top", ctypes.c_int)]


class Block_Type(enum.Enum):
    BLOCK_NULL = -1
    BLOCK_BASIC_STRONG_COLOR = 0
    BLOCK_BASIC_WEAK_COLOR = 1
    BLOCK_CYAN_COLOR = 2
    BLOCK_PINK_COLOR = 3
    BLOCK_STAIR_CLOSED = 4
    BLOCK_STAIR_OPENED = 5


class Block:
    def __init__(self, selected_block=None, px=None, py=None):
        self.image = pico2d.load_image('resource\\Block_Floors.png')
        if px is None and py is None:
            self.pivot = Point(500, 500)
            self.camera_pivot = Point(500, 500)
        else:
            self.pivot = Point(px, py)
            self.camera_pivot = Point(px, py)

        self.image_multiple_size = 2
        if selected_block is None:
            self.value = Block_Type.BLOCK_BASIC_STRONG_COLOR
        else:
            self.value = selected_block

    def update(self):
        pass

    def get_pivot(self):
        return self.pivot

    def set_pivot(self, pivot_data):
        self.camera_pivot = pivot_data
        pass

    def draw(self):
        block_origin_size = Image_Origin_Size(26, 26)
        image_start_point = Point(0, self.image.h - 26)
        if self.value == Block_Type.BLOCK_BASIC_STRONG_COLOR:
            image_start_point = Point(0, self.image.h - 26)
        elif self.value == Block_Type.BLOCK_BASIC_WEAK_COLOR:
            image_start_point = Point(26 * 2, self.image.h - 26)

        self.image.clip_draw(image_start_point.x, image_start_point.y,
                             block_origin_size.width, block_origin_size.height,
                             self.camera_pivot.x, self.camera_pivot.y,
                             (block_origin_size.width - 1) * self.image_multiple_size, (block_origin_size.height - 1) * self.image_multiple_size)
        pass


class Wall:
    pass


class Camera:
    def __init__(self):
        self.camera_rect = Rectangle(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT)
        pass

    def update(self):
        pass

    def move(self, key):
        moving_interval = 100
        if key == 'w':
            self.camera_rect.top += moving_interval
            self.camera_rect.bottom += moving_interval
        elif key == 'a':
            self.camera_rect.left -= moving_interval
            self.camera_rect.right -= moving_interval
        elif key == 's':
            self.camera_rect.top -= moving_interval
            self.camera_rect.bottom -= moving_interval
        elif key == 'd':
            self.camera_rect.left += moving_interval
            self.camera_rect.right += moving_interval
        pass

    def trans_point_object_to_camera(self, object_x, object_y):
        return Point(object_x - self.camera_rect.left, object_y - self.camera_rect.bottom)

    pass


canvas_camera = Camera()
block = [Block()]
running = True
check_simultaneous_key_buffer_dic = {'ctrl': False, 'key_s': False}
select_block_value = Block_Type.BLOCK_BASIC_STRONG_COLOR


def handle_events():
    global running
    global canvas_camera
    global block
    global check_simultaneous_key_buffer_dic
    global select_block_value
    events = pico2d.get_events()

    # simultaneous = 동시에 일어나는

    for event in events:
        if event.type == pico2d.SDL_QUIT:
            running = False
        elif event.type == pico2d.SDL_KEYDOWN:
            if event.key == pico2d.SDLK_ESCAPE:
                running = False
            elif event.key == pico2d.SDLK_w:
                canvas_camera.move('w')

            elif event.key == pico2d.SDLK_a:
                canvas_camera.move('a')

            elif event.key == pico2d.SDLK_s:
                canvas_camera.move('s')
                check_simultaneous_key_buffer_dic['key_s'] = True

            elif event.key == pico2d.SDLK_d:
                canvas_camera.move('d')

            elif event.key == pico2d.SDLK_LCTRL:
                check_simultaneous_key_buffer_dic['ctrl'] = True
                continue

            elif event.key == pico2d.SDLK_1:
                select_block_value = Block_Type.BLOCK_BASIC_STRONG_COLOR
            elif event.key == pico2d.SDLK_2:
                select_block_value = Block_Type.BLOCK_BASIC_WEAK_COLOR

        elif event.type == pico2d.SDL_KEYUP:
            if event.key == pico2d.SDLK_s:
                check_simultaneous_key_buffer_dic['key_s'] = False
                continue
            elif event.key == pico2d.SDLK_LCTRL:
                check_simultaneous_key_buffer_dic['ctrl'] = False
                continue

        elif event.type == pico2d.SDL_MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.x, CANVAS_HEIGHT - 1 - event.y

            click_area = Rectangle(mouse_x - mouse_x % 50, mouse_y - mouse_y % 50, mouse_x - mouse_x % 50 + 50, mouse_y - mouse_y % 50 + 50)

            if abs(mouse_x - click_area.left) <= abs(mouse_x - click_area.right):
                mouse_x = click_area.left
            else:
                mouse_x = click_area.right

            if abs(mouse_y - click_area.bottom) <= abs(mouse_y - click_area.top):
                mouse_y = click_area.bottom
            else:
                mouse_y = click_area.top

            mouse_point = Point(mouse_x + canvas_camera.camera_rect.left, mouse_y + canvas_camera.camera_rect.bottom)
            # duplication = 중복
            check_duplication = False
            for duplication in block:
                if duplication.pivot.x == mouse_point.x and duplication.pivot.y == mouse_point.y:
                    check_duplication = True
                    break

            if check_duplication is False:
                block.append(Block(select_block_value, mouse_point.x, mouse_point.y))
            pass
    pass


while running:
    pico2d.clear_canvas()
    handle_events()

    canvas_camera.update()
    for i in block:
        val = canvas_camera.trans_point_object_to_camera(i.get_pivot().x, i.get_pivot().y)
        i.set_pivot(val)

    black_background.draw(CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2)
    cnt = 0
    for i in block:
        i.draw()
        if check_simultaneous_key_buffer_dic['ctrl'] is True and check_simultaneous_key_buffer_dic['key_s'] is True:
            if cnt == 0:
                map_data_file.write(" -----------------------------------------\n ")

            cnt += 1
            map_data_file.write(str(cnt) + "번 째 블럭 : " + "< " + str(i.pivot.x) + ", " + str(i.pivot.y) + " > \n")
            pass

    pico2d.draw_rectangle(CANVAS_WIDTH - 350, CANVAS_HEIGHT - 100, CANVAS_WIDTH, CANVAS_HEIGHT)
    pico2d.update_canvas()

    pico2d.delay(0.1)
    # pico2d.get_events()

map_data_file.close()
pico2d.close_canvas()
