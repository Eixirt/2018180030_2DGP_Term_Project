import pico2d
import ctypes

import MainState


class Point(ctypes.Structure):
    _fields_ = [("x", ctypes.c_int),
                ("y", ctypes.c_int)]


Monster_Type_Keys = ['MONSTER_NULL',
                   'MONSTER_SLIME_GREEN', 'MONSTER_SLIME_BLUE',
                   'MONSTER_SKULL_WHITE', 'MONSTER_BAT_BASIC',
                   'MONSTER_BANSHEE']
Monster_Type_Values = list(range(len(Monster_Type_Keys)))
Monster_Type = dict(zip(Monster_Type_Keys, Monster_Type_Values))

