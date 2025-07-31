import enum
import os
import sys
from optparse import Values

__version__ = '0.1.0'
PROG = 'barbariantuw'

OPTS = Values()
BASE_PATH = os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else
                            __file__)
FONT_PATH = os.path.abspath(BASE_PATH + '/fnt') + '/'
IMG_PATH = os.path.abspath(BASE_PATH + '/img') + '/'
SND_PATH = os.path.abspath(BASE_PATH + '/snd') + '/'
FRAME_RATE = 60
FONT = FONT_PATH + 'PressStart2P-Regular.ttf'


class Theme:
    DEBUG = (38, 213, 255)  # cyan
    OPTS_TITLE = (255, 238, 0)
    OPTS_TXT = (255, 255, 255)  # white
    MENU_TXT = (187, 102, 0)
    BACK = (0, 0, 0)  # black
    TXT = (0, 0, 0)  # black
    LEADER_TXT = (128, 128, 128)
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
    country = 'Europe'  # USA, Europe
    decor = 'foret'  # foret, plaine, trone, arene
    partie = Partie.solo
    ia = 0
    scoreA = 0
    scoreB = 0
    scx = 1 if sys.platform == 'emscripten' else 3  # scale X
    scy = 1 if sys.platform == 'emscripten' else 3  # scale y
    screen = (320 * scx, 200 * scy)
    chw = int(320 / 40 * scx)  # character width, 24
    chh = int(200 / 25 * scy)  # character height, 24

    @staticmethod
    def get_hiscores():
        # TODO: Store/Load hiscores
        return [('RL', 10000),
                ('SB', 5000),
                ('GC', 4000),
                ('JW', 3000),
                ('RJ', 2000),
                ('KC', 1000)]


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
