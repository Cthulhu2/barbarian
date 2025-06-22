# -*- coding: utf-8 -*-
import os

BASE_PATH = os.path.abspath(os.path.dirname(__file__))
FONT_PATH = os.path.abspath(BASE_PATH + '/../resources/font') + '/'
IMG_PATH = os.path.abspath(BASE_PATH + '/../resources/img') + '/'
SND_PATH = os.path.abspath(BASE_PATH + '/../resources/snd') + '/'

SCALE = 3
SCREEN_SIZE = (320 * SCALE, 200 * SCALE)

FONT = FONT_PATH + 'PressStart2P-Regular.ttf'


class Theme:
    DEBUG = (38, 213, 255)  # cyan
    OPTS_TITLE = (255, 238, 0)
    OPTS_TXT = (255, 255, 255)  # white
    BACK = (0, 0, 0)  # black
    TXT = (0, 0, 0)  # black
