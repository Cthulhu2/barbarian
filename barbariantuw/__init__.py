import enum
import os
import sys
from optparse import Values

OPTS = Values()
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


class Partie(enum.Enum):
    demo = enum.auto()
    solo = enum.auto()
    vs = enum.auto()


class Game:  # Mutable options
    Country = 'Europe'  # USA, Europe
    Decor = 'foret'  # foret, plaine, trone, arene
    Partie = Partie.solo
    IA = 0
    ScoreA = 0
    ScoreB = 0


class Levier(enum.Enum):
    bas = enum.auto()
    basG = enum.auto()
    basD = enum.auto()
    droite = enum.auto()
    gauche = enum.auto()
    haut = enum.auto()
    hautG = enum.auto()
    hautD = enum.auto()
    neutre = enum.auto()


class State(enum.Enum):
    araignee = enum.auto()
    attente = enum.auto()
    avance = enum.auto()
    assis = enum.auto()
    assis2 = enum.auto()
    clingD = enum.auto()
    clingH = enum.auto()
    cou = enum.auto()
    coupdepied = enum.auto()
    coupdetete = enum.auto()
    debout = enum.auto()
    decapite = enum.auto()
    devant = enum.auto()
    retourne = enum.auto()
    front = enum.auto()
    genou = enum.auto()
    protegeD1 = enum.auto()
    protegeD = enum.auto()
    protegeH1 = enum.auto()
    protegeH = enum.auto()
    recule = enum.auto()
    releve = enum.auto()
    rouladeAV = enum.auto()
    rouladeAR = enum.auto()
    saute = enum.auto()
    tombe = enum.auto()
    tombe1 = enum.auto()
    touche = enum.auto()
    touche1 = enum.auto()
    #
    mort = enum.auto()
    mortdecap = enum.auto()
    vainqueur = enum.auto()
    vainqueurKO = enum.auto()
    #
    fini = enum.auto()
    sorcier = enum.auto()
    mortSORCIER = enum.auto()
    sorcierFINI = enum.auto()
