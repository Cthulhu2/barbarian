# -*- coding: utf-8 -*-
import os


BASE_PATH = os.path.abspath(os.path.dirname(__file__))
FONT_PATH = os.path.abspath(BASE_PATH + '/../resources/font') + '/'
IMG_PATH = os.path.abspath(BASE_PATH + '/../resources/img') + '/'
SND_PATH = os.path.abspath(BASE_PATH + '/../resources/snd') + '/'

SCREEN_SIZE = (640, 400)

FONT = FONT_PATH + 'PressStart2P-Regular.ttf'


class Colors:
    DEBUG = (237, 28, 36)  # red
    BACK = (0, 0, 0)  # black
