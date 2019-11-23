import pico2d
import ctypes
import enum

import GameFrameWork
import GameWorldManager

CANVAS_WIDTH, CANVAS_HEIGHT = 1280, 720

pico2d.open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT, False, False)

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
    BLOCK_NULL = enum.auto()
    BLOCK_BASIC_STRONG_COLOR_1 = enum.auto()
    BLOCK_BASIC_WEAK_COLOR_1 = enum.auto()
    BLOCK_BASIC_STRONG_COLOR_2 = enum.auto()
    BLOCK_BASIC_WEAK_COLOR_2 = enum.auto()
    BLOCK_CYAN_COLOR = enum.auto()
    BLOCK_PINK_COLOR = enum.auto()
    BLOCK_STAIR_CLOSED = enum.auto()
    BLOCK_STAIR_OPENED = enum.auto()


class Wall_Type(enum.Enum):
    WALL_NULL = enum.auto()
    WALL_BASIC_1 = enum.auto()
    WALL_BASIC_2 = enum.auto()
    WALL_VINE = enum.auto()
    WALL_STONE = enum.auto()
    WALL_STONE_DAMAGED = enum.auto()
    WALL_SKULL_1 = enum.auto()
    WALL_SKULL_2 = enum.auto()
    WALL_SKULL_3 = enum.auto()


class Monster_Type(enum.Enum):
    MONSTER_NULL = enum.auto()
    MONSTER_SLIME_GREEN = enum.auto()
    MONSTER_SLIME_BLUE = enum.auto()
    MONSTER_SKULL_WHITE = enum.auto()
    MONSTER_BAT_BASIC = enum.auto()
    MONSTER_BANSHEE = enum.auto()


class Block:
    image = None

    def __init__(self, selected_block=None, px=None, py=None):
        if Block.image is None:
            Block.image = pico2d.load_image('resource\\Block_Floors.png')
        if px is None and py is None:
            self.pivot = Point(500, 500)
            self.camera_pivot = Point(500, 500)
        else:
            self.pivot = Point(px, py)
            self.camera_pivot = Point(px, py)

        self.image_scale = 2
        if selected_block is None:
            self.value = Block_Type.BLOCK_BASIC_STRONG_COLOR_1
        else:
            self.value = selected_block

    def update(self):
        pass

    def set_pivot_from_camera(self, pivot_data):
        self.camera_pivot = pivot_data
        pass

    def draw(self):
        block_origin_size = Image_Origin_Size(26, 26)
        image_start_point = Point(0, self.image.h - 26)
        if self.value == Block_Type.BLOCK_BASIC_STRONG_COLOR_1:
            image_start_point = Point(0, self.image.h - 26)
        elif self.value == Block_Type.BLOCK_BASIC_WEAK_COLOR_1:
            image_start_point = Point(26 * 2, self.image.h - 26)

        self.image.clip_draw(image_start_point.x, image_start_point.y,
                             block_origin_size.width, block_origin_size.height,
                             self.camera_pivot.x, self.camera_pivot.y,
                             (block_origin_size.width - 1) * self.image_scale, (block_origin_size.height - 1) * self.image_scale)
        pass


class Wall:
    image = None

    def __init__(self, selected_wall=None, px=None, py=None):
        if Wall.image is None:
            Wall.image = pico2d.load_image('resource\\Block_Walls.png')
        if px is None and py is None:
            self.pivot = Point(400, 500)
            self.camera_pivot = Point(400, 500)
        else:
            self.pivot = Point(px, py)
            self.camera_pivot = Point(px, py)

        self.image_scale = 2
        if selected_wall is None:
            self.value = Wall_Type.WALL_BASIC_1
        else:
            self.value = selected_wall

    def update(self):
        pass

    def set_pivot_from_camera(self, pivot_data):
        self.camera_pivot = pivot_data
        pass

    def draw(self):
        wall_origin_size = Image_Origin_Size(24, 40)
        image_start_point = Point(0, self.image.h - 40)
        if self.value == Wall_Type.WALL_BASIC_1:
            image_start_point = Point(0, self.image.h - 40)
        elif self.value == Wall_Type.WALL_BASIC_2:
            image_start_point = Point(24 * 1, self.image.h - 40)
        elif self.value == Wall_Type.WALL_VINE:
            image_start_point = Point(24 * 2, self.image.h - 40)
        elif self.value == Wall_Type.WALL_STONE:
            image_start_point = Point(24 * 29, self.image.h - 40)
        elif self.value == Wall_Type.WALL_STONE_DAMAGED:
            image_start_point = Point(24 * 30, self.image.h - 40)
        elif self.value == Wall_Type.WALL_SKULL_1:
            image_start_point = Point(24 * 7, self.image.h - 40)
        elif self.value == Wall_Type.WALL_SKULL_2:
            image_start_point = Point(24 * 8, self.image.h - 40)
        elif self.value == Wall_Type.WALL_SKULL_3:
            image_start_point = Point(24 * 9, self.image.h - 40)

        self.image.clip_draw(image_start_point.x, image_start_point.y,
                             wall_origin_size.width, wall_origin_size.height,
                             self.camera_pivot.x, self.camera_pivot.y,
                             (wall_origin_size.width + 1) * self.image_scale, (wall_origin_size.height - 1) * self.image_scale)
        pass


class Monster:
    image = None

    def __init__(self, selected_mob=None, px=None, py=None):
        if Monster.image is None:
            Monster.image = pico2d.load_image('resource\\Block_Walls.png')
        if px is None and py is None:
            self.pivot = Point(400, 500)
            self.camera_pivot = Point(400, 500)
        else:
            self.pivot = Point(px, py)
            self.camera_pivot = Point(px, py)

        self.image_scale = 2
        if selected_mob is None:
            self.value = Monster_Type.MONSTER_SLIME_GREEN
        else:
            self.value = selected_mob
        pass

    def update(self):
        pass

    def set_pivot(self, mob_type):
        pass

    def draw(self):
        pass

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
block_list = [Block()]
wall_list = [Wall()]
running = True
check_simultaneous_key_buffer_dic = {'ctrl': False, 'key_s': False}
select_block_value = Block_Type.BLOCK_BASIC_STRONG_COLOR_1
select_wall_value = Wall_Type.WALL_BASIC_1
curr_selected_object = 'Block'  # Block / Wall / Monster / Delete_Object


def handle_events():
    global running
    global canvas_camera
    global block_list
    global wall_list
    global check_simultaneous_key_buffer_dic
    global select_block_value
    global select_wall_value
    global curr_selected_object
    events = pico2d.get_events()

    # simultaneous = 동시에 일어나는

    for event in events:
        if event.type == pico2d.SDL_QUIT:
            running = False
        elif event.type == pico2d.SDL_KEYDOWN:
            if event.key == pico2d.SDLK_ESCAPE:
                running = False
                #카메라 움직임
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

            # 블럭 선택
            elif event.key == pico2d.SDLK_1:
                select_block_value = Block_Type.BLOCK_BASIC_STRONG_COLOR_1
                curr_selected_object = 'Block'
            elif event.key == pico2d.SDLK_2:
                select_block_value = Block_Type.BLOCK_BASIC_WEAK_COLOR_1
                curr_selected_object = 'Block'
            elif event.key == pico2d.SDLK_3:
                select_wall_value = Wall_Type.WALL_BASIC_1
                curr_selected_object = 'Wall'
            elif event.key == pico2d.SDLK_4:
                select_wall_value = Wall_Type.WALL_BASIC_2
                curr_selected_object = 'Wall'
            elif event.key == pico2d.SDLK_5:
                select_wall_value = Wall_Type.WALL_VINE
                curr_selected_object = 'Wall'
            elif event.key == pico2d.SDLK_6:
                select_wall_value = Wall_Type.WALL_STONE
                curr_selected_object = 'Wall'
            elif event.key == pico2d.SDLK_7:
                select_wall_value = Wall_Type.WALL_STONE_DAMAGED
                curr_selected_object = 'Wall'
            elif event.key == pico2d.SDLK_8:
                select_wall_value = Wall_Type.WALL_SKULL_1
                curr_selected_object = 'Wall'
            elif event.key == pico2d.SDLK_9:
                select_wall_value = Wall_Type.WALL_SKULL_2
                curr_selected_object = 'Wall'
            elif event.key == pico2d.SDLK_0:
                select_wall_value = Wall_Type.WALL_SKULL_3
                curr_selected_object = 'Wall'

            # 몬스터 선택
            elif event.key == pico2d.SDLK_y:
                select_wall_value = Monster_Type.MONSTER_SLIME_GREEN
                curr_selected_object = 'Monster'
            elif event.key == pico2d.SDLK_u:
                select_wall_value = Monster_Type.MONSTER_SLIME_BLUE
                curr_selected_object = 'Monster'
            elif event.key == pico2d.SDLK_i:
                select_wall_value = Monster_Type.MONSTER_SKULL_WHITE
                curr_selected_object = 'Monster'
            elif event.key == pico2d.SDLK_o:
                select_wall_value = Monster_Type.MONSTER_BAT_BASIC
                curr_selected_object = 'Monster'
            elif event.key == pico2d.SDLK_p:
                select_wall_value = Monster_Type.MONSTER_BANSHEE
                curr_selected_object = 'Monster'

            elif event.key == pico2d.SDLK_DELETE:
                curr_selected_object = 'Delete_Object'
            elif event.key == pico2d.SDLK_r:
                block_list.clear()
                wall_list.clear()
                map_data_load_file = open("map_data_load.txt", 'r')
                read_database = map_data_load_file.read()
                split_data = read_database.split()
                for curr_reading_data_idx, curr_reading_data_val in enumerate(split_data):
                    if split_data[curr_reading_data_idx] == 'Block':
                        str_to_enum_val = str(split_data[curr_reading_data_idx + 1])
                        str_to_enum_val = str_to_enum_val.replace('Block_Type.', "")
                        block_list.append(Block(Block_Type[str_to_enum_val], int(split_data[curr_reading_data_idx+2]), int(split_data[curr_reading_data_idx+3])))
                        pass
                    elif split_data[curr_reading_data_idx] == 'Wall':

                        str_to_enum_val = str(split_data[curr_reading_data_idx + 1])
                        str_to_enum_val = str_to_enum_val.replace('Wall_Type.', "")
                        wall_list.append(Wall(Wall_Type[str_to_enum_val], int(split_data[curr_reading_data_idx + 2]), int(split_data[curr_reading_data_idx + 3])))
                        pass
                    curr_reading_data_idx += 3
                map_data_load_file.close()
                pass

        elif event.type == pico2d.SDL_KEYUP:
            if event.key == pico2d.SDLK_s:
                check_simultaneous_key_buffer_dic['key_s'] = False
                continue
            elif event.key == pico2d.SDLK_LCTRL:
                check_simultaneous_key_buffer_dic['ctrl'] = False
                continue
        
        # 마우스로 블럭 생성하기 위한 마우스 위치 조정
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
            # duplication = 중복 / 중복 체크
            check_duplication = False
            for duplication in block_list:
                if duplication.pivot.x == mouse_point.x and duplication.pivot.y == mouse_point.y:
                    check_duplication = True
                    if curr_selected_object == 'Delete_Object':
                        del block_list[block_list.index(duplication)]
                    break
            for duplication in wall_list:
                if duplication.pivot.x == mouse_point.x and duplication.pivot.y == mouse_point.y:
                    check_duplication = True
                    if curr_selected_object == 'Delete_Object':
                        del wall_list[wall_list.index(duplication)]
                    break
            # 중복되지 않았다면 블럭 생성
            if check_duplication is False:
                if curr_selected_object == 'Block':
                    block_list.append(Block(select_block_value, mouse_point.x, mouse_point.y))
                elif curr_selected_object == 'Wall':
                    wall_list.append(Wall(select_wall_value, mouse_point.x, mouse_point.y))
            pass
    pass


while running:
    pico2d.clear_canvas()
    handle_events()

    canvas_camera.update()
    for i in block_list:
        val = canvas_camera.trans_point_object_to_camera(i.pivot.x, i.pivot.y)
        i.set_pivot_from_camera(val)

    for i in wall_list:
        val = canvas_camera.trans_point_object_to_camera(i.pivot.x, i.pivot.y)
        i.set_pivot_from_camera(val)

    black_background.draw(CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2)
    cnt = 0
    for i in block_list:
        i.draw()
        if check_simultaneous_key_buffer_dic['ctrl'] is True and check_simultaneous_key_buffer_dic['key_s'] is True:
            if cnt == 0:
                map_data_file = open("map_data_save.txt", 'w')
                map_data_view_file = open("map_data_view.txt", 'w')

                map_data_view_file.write(" -----------------------------------------\n ")

            cnt += 1
            map_data_file.write("Block" + " " + str(i.value) + " " + str(i.pivot.x) + " " + str(i.pivot.y) + "\n")
            map_data_view_file.write(str(cnt) + "번 째 블럭 : " + "< " + str(i.pivot.x) + ", " + str(i.pivot.y) + " > \n")

            if block_list.index(i) == (len(block_list) - 1):
                map_data_file.close()
                map_data_view_file.close()
                pass
            pass
    cnt = 0
    for i in wall_list:
        i.draw()
        if check_simultaneous_key_buffer_dic['ctrl'] is True and check_simultaneous_key_buffer_dic['key_s'] is True:
            if cnt == 0:
                map_data_file = open("map_data_save.txt", 'a')
                map_data_view_file = open("map_data_view.txt", 'a')
                map_data_view_file.write(" -----------------------------------------\n ")
                pico2d.delay(1)

            cnt += 1
            map_data_file.write("Wall" + " " + str(i.value) + " " + str(i.pivot.x) + " " + str(i.pivot.y) + "\n")
            map_data_view_file.write(str(cnt) + "번 째 벽 : " + "< " + str(i.pivot.x) + ", " + str(i.pivot.y) + " > \n")

            if wall_list.index(i) == (len(wall_list) - 1):
                map_data_file.close()
                map_data_view_file.close()
                pass
        pass

    pico2d.update_canvas()

    pico2d.delay(0.1)
    # pico2d.get_events()

pico2d.close_canvas()
