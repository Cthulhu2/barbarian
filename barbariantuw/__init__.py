__version__ = '0.1.0'

import enum
import os
import sys
from argparse import Namespace
from pathlib import Path
from typing import List, Tuple, Union

PROG = 'barbariantuw'

OPTS = Namespace()
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


def appdata(file: str) -> Union[Path, str]:
    if sys.platform == 'emscripten':
        return f'{PROG}/{file}'

    if sys.platform == 'windows':
        return Path(os.getenv('LOCALAPPDATA')) / f'{PROG}/{file}'

    return Path.home() / f'.local/share/{PROG}/{file}'


class Game:  # Mutable options
    country = 'EUROPE'
    fullscreen = False
    #
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
    def load_options():
        opts = ''
        try:
            fOptions = appdata('options.dat')
            if sys.platform == 'emscripten':
                # noinspection PyUnresolvedReferences
                from platform import window
                opts = window.localStorage.getItem(f'{fOptions}')
            elif fOptions.is_file():
                opts = fOptions.read_text()

            for line in opts.split(os.linesep):
                opt, val = line.split('=', maxsplit=1) if '=' in line else ('', '')
                if opt.strip().lower() == 'country' and val:
                    Game.country = 'USA' if val.strip().upper() == 'USA' else 'EUROPE'
                elif opt.strip().lower() == 'fullscreen' and val:
                    Game.fullscreen = (val.strip().upper() == 'TRUE')
        except Exception as ex:
            print(f'load_options error: {ex}')

    @staticmethod
    def save_options():
        opts = os.linesep.join((f'country={Game.country.upper()}',
                                f'fullscreen={Game.fullscreen}'))
        try:
            fOptions = appdata('options.dat')
            if sys.platform == 'emscripten':
                # noinspection PyUnresolvedReferences
                from platform import window
                window.localStorage.setItem(fOptions, opts)
            else:
                if not fOptions.exists():
                    fOptions.parent.mkdir(parents=True, exist_ok=True)
                fOptions.write_text(opts)
        except Exception as ex:
            print(f'save_options error: {ex}')

    @staticmethod
    def load_hiscores() -> List[Tuple[int, str]]:
        hiscores = None
        try:
            fScores = appdata('hiscores.dat')
            if sys.platform == 'emscripten':
                # noinspection PyUnresolvedReferences
                from platform import window
                hiscores = window.localStorage.getItem(f'{fScores}')
            elif fScores.is_file():
                hiscores = fScores.read_text()

            if hiscores:
                scores = []

                for line in hiscores.split(os.linesep):
                    if line:
                        score, name = line.split(' ', maxsplit=1)
                        scores.append((min(99999, int(score)), name[0:3]))
                if scores:
                    return scores  #
        except Exception as ex:
            print(f'load_hiscores error: {ex}')

        return [(10000, 'RL'),
                (5000, 'SB'),
                (4000, 'GC'),
                (3000, 'JW'),
                (2000, 'RJ'),
                (1000, 'KC')]

    @staticmethod
    def save_hiscores(hiscores: List[Tuple[int, str]]):
        hiscores = os.linesep.join([f'{score} {name}'
                                    for score, name in hiscores])
        #
        try:
            fScores = appdata('hiscores.dat')
            if sys.platform == 'emscripten':
                # noinspection PyUnresolvedReferences
                from platform import window
                window.localStorage.setItem(fScores, hiscores)
            else:
                if not fScores.exists():
                    fScores.parent.mkdir(parents=True, exist_ok=True)
                fScores.write_text(hiscores)
        except Exception as ex:
            print(f'save_hiscores error: {ex}')


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
