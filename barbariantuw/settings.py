# -*- coding: utf-8 -*-
import os
import sys

BASE_PATH = os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else
                            __file__)
FONT_PATH = os.path.abspath(BASE_PATH + '/fnt') + '/'
IMG_PATH = os.path.abspath(BASE_PATH + '/img') + '/'
SND_PATH = os.path.abspath(BASE_PATH + '/snd') + '/'

SCALE_X = 1 if sys.platform == 'emscripten' else 3
SCALE_Y = 1 if sys.platform == 'emscripten' else 3
SCREEN_SIZE = (320 * SCALE_X, 200 * SCALE_Y)
CHAR_W = int(320 / 40 * SCALE_X)  # 24
CHAR_H = int(200 / 25 * SCALE_Y)  # 24
FRAME_RATE = 60

FONT = FONT_PATH + 'PressStart2P-Regular.ttf'


class Theme:
    DEBUG = (38, 213, 255)  # cyan
    OPTS_TITLE = (255, 238, 0)
    OPTS_TXT = (255, 255, 255)  # white
    BACK = (0, 0, 0)  # black
    TXT = (0, 0, 0)  # black
    #
    VIEWER_BACK = (55, 55, 55)  # dark gray
    VIEWER_TXT = (225, 225, 225)  # light gray
    VIEWER_TXT_SELECTED = (78, 255, 87)  # green
    VIEWER_BORDER = (204, 0, 0)  # red
    #
    YELLOW = (241, 255, 0)
    BLUE = (80, 255, 239)
    PURPLE = (203, 0, 255)
    RED = (237, 28, 36)
    GREEN = (138, 226, 52)
    BLACK = (0, 0, 0)
