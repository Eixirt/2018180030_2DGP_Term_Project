import pico2d
import ctypes
import enum

import GameWorldManager
import BlockSet
import Monster
import MainState
import Dropped_Item


class Point(ctypes.Structure):
    _fields_ = [("x", ctypes.c_int),
                ("y", ctypes.c_int)]


Block_Type_Keys = ['BLOCK_NULL',
                   'BLOCK_BASIC_STRONG_COLOR_1', 'BLOCK_BASIC_WEAK_COLOR_1',
                   'BLOCK_BASIC_STRONG_COLOR_2', 'BLOCK_BASIC_WEAK_COLOR_2',
                   'BLOCK_CYAN_COLOR', 'BLOCK_PINK_COLOR', 'BLOCK_STAIR_CLOSED', 'BLOCK_STAIR_OPENED']
Block_Type_Values = list(range(len(Block_Type_Keys)))
Block_Type = dict(zip(Block_Type_Keys, Block_Type_Values))


Wall_Type_Keys = ['WALL_NULL', 'WALL_BASIC_1', 'WALL_BASIC_2', 'WALL_VINE', 'WALL_STONE',
                  'WALL_STONE_DAMAGED', 'WALL_SKULL_1', 'WALL_SKULL_2', 'WALL_SKULL_3']
Wall_Type_Values = list(range(len(Wall_Type_Keys)))
Wall_Type = dict(zip(Wall_Type_Keys, Wall_Type_Values))


Monster_Type_Keys = ['MONSTER_NULL',
                     'MONSTER_SLIME_GREEN', 'MONSTER_SLIME_BLUE',
                     'MONSTER_SKULL_WHITE', 'MONSTER_BAT_BASIC',
                     'MONSTER_BANSHEE', 'MONSTER_SKELETON_KNIGHT']

Monster_Type_Values = list(range(len(Monster_Type_Keys)))
Monster_Type = dict(zip(Monster_Type_Keys, Monster_Type_Values))


# layer 0: Background Objects
# layer 1: Map Objects
# layer 2: Monster Objects
# layer 3: Player Objects
# layer 4: Map-UnderWall Objects
# layer 5: UI Objects
# layer 6: Hit Image and Message


class FirstStage:

    def __init__(self):
        self.block_list = []
        self.wall_list = []
        # Monster.Bat_Basic(700, 350 + 20)
        self.monster_list = [Monster.Slime_Green(600, 350 + 10), Monster.Slime_Green(600, 300 + 10),
                             Monster.Bat_Basic(700, 350 + 20), Monster.Bat_Basic(700, 400 + 20), Monster.Bat_Basic(700, 450 + 20),
                             Monster.Bat_Basic(650, 450 + 20), Monster.Skeleton_Knight(900, 100 - 5),
                             Monster.Skeleton_Knight(350, -700 - 5), Monster.Slime_Green(750, -100 + 10), Monster.Slime_Green(500, -200 + 10), Monster.Slime_Green(500, -250 + 10),
                             Monster.Bat_Basic(250, -550 + 20), Monster.Bat_Basic(350, -550 + 20), Monster.Bat_Basic(250, -450 + 20), Monster.Bat_Basic(350, -450 + 20),
                             Monster.Banshee(0, -400 + 20), Monster.Slime_Green(950, 650 + 10)]

        self.chest_list = [BlockSet.Chest(BlockSet.Block_Type['BLOCK_RED_CHEST'], Dropped_Item.DroppedItem_Type['ITEM_TORCH_NORMAL'], 750, 100),
                           BlockSet.Chest(BlockSet.Block_Type['BLOCK_RED_CHEST'], Dropped_Item.DroppedItem_Type['ITEM_TORCH_BASIC'], 950, 700),
                           BlockSet.Chest(BlockSet.Block_Type['BLOCK_BLACK_CHEST'], Dropped_Item.DroppedItem_Type['ITEM_TORCH_BLUE'], 500, 500),
                           BlockSet.Chest(BlockSet.Block_Type['BLOCK_BLACK_CHEST'], Dropped_Item.DroppedItem_Type['ITEM_HEAL'], 450, -450)]

        self.item_list = []

        self.init_map_objects()

        for block_object in self.block_list:
            GameWorldManager.add_object(block_object, MainState.LAYER_MAP)
        for wall_object in self.wall_list:
            GameWorldManager.add_object(wall_object, MainState.LAYER_MAP)
        for monster_object in self.monster_list:
            GameWorldManager.add_object(monster_object, MainState.LAYER_MONSTER)
        for chest_object in self.chest_list:
            GameWorldManager.add_object(chest_object, MainState.LAYER_ITEM)

        self.next_floor = BlockSet.NextFloor(False, 0, -450)
        GameWorldManager.add_object(self.next_floor, MainState.LAYER_EXIT)

        self.stage1_bgm = pico2d.load_wav('resource\\sound\\stage1_bgm.wav')
        self.stage1_bgm.set_volume(35)
        self.stage1_bgm.repeat_play()
        pass

    def init_map_objects(self):

        for block_object in self.block_list:
            GameWorldManager.remove_object(block_object, MainState.LAYER_MAP)
        for wall_object in self.wall_list:
            GameWorldManager.remove_object(wall_object, MainState.LAYER_MAP)

        self.block_list.clear()
        self.wall_list.clear()

        map_data_load_file = open("map_data_load.txt", 'r')
        read_database = map_data_load_file.read()
        split_data = read_database.split()

        for curr_reading_data_idx, curr_reading_data_val in enumerate(split_data):
            if split_data[curr_reading_data_idx] == 'Block':
                str_to_enum_val = str(split_data[curr_reading_data_idx + 1])
                str_to_enum_val = str_to_enum_val.replace('Block_Type.', "")
                self.block_list.append(BlockSet.Block(Block_Type[str_to_enum_val], int(split_data[curr_reading_data_idx + 2]), int(split_data[curr_reading_data_idx + 3])))
                pass

            elif split_data[curr_reading_data_idx] == 'Wall':
                str_to_enum_val = str(split_data[curr_reading_data_idx + 1])
                str_to_enum_val = str_to_enum_val.replace('Wall_Type.', "")
                self.wall_list.append(BlockSet.Wall(Wall_Type[str_to_enum_val], int(split_data[curr_reading_data_idx + 2]), int(split_data[curr_reading_data_idx + 3])))
                pass

            curr_reading_data_idx += 3

        map_data_load_file.close()
        pass

    def update(self):
        for monster_object in self.monster_list:
            if monster_object.curr_hp <= 0:
                monster_object.death_sound.play()
                if monster_object.type == Monster.Monster_Type['MONSTER_BANSHEE']:
                    self.next_floor.door_open()
                    pass

                if monster_object.type == Monster.Monster_Type['MONSTER_BANSHEE']:
                    MainState.player_cadence.holding_gold += 90
                    MainState.player_cadence.holding_diamond += 3
                    pass
                elif monster_object.type == Monster.Monster_Type['MONSTER_SKELETON_KNIGHT']:
                    MainState.player_cadence.holding_gold += 20
                    MainState.player_cadence.holding_diamond += 1

                self.monster_list.remove(monster_object)
                GameWorldManager.remove_object(monster_object)

                MainState.player_cadence.holding_gold += 10

        if MainState.player_cadence.curr_hp <= 0:
            self.stage1_bgm.set_volume(20)
        pass

    def draw(self):
        pass
    pass


