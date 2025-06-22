# -*- coding: utf-8 -*-
import enum
from os.path import join
from typing import Tuple, Dict

from pygame import image, Rect
from pygame.font import Font
from pygame.mixer import Sound
from pygame.sprite import DirtySprite, AbstractGroup
from pygame.surface import Surface
from pygame.time import get_ticks
from pygame.transform import scale, rotate, flip

from settings import IMG_PATH, SCALE, FONT, SND_PATH

snd_cache: Dict[int, Sound] = {}
img_cache: Dict[str, Surface] = {}


def get_snd(name) -> Sound:
    key_ = hash(name)

    if key_ in snd_cache:
        return snd_cache[key_]

    snd = Sound(join(SND_PATH, name))
    snd_cache[key_] = snd
    return snd


def get_img(name, w=0, h=0, angle=0, xflip=False, fill=None, blend_flags=0,
            color=None) -> Surface:
    key_ = sum((hash(name), hash(w), hash(h), hash(angle), hash(xflip),
                hash(fill), hash(blend_flags), hash(color)))

    if key_ in img_cache:
        return img_cache[key_]

    img: Surface

    if color:
        img = image.load(join(IMG_PATH, name))
        img.set_colorkey(color)
        img = img.convert_alpha()
    else:
        img = image.load(join(IMG_PATH, name)).convert_alpha()
    if fill and blend_flags:
        img = img.copy()
        img.fill(fill, special_flags=blend_flags)
    if w > 0 or h > 0:
        img = scale(img, (w * SCALE, h * SCALE))
    else:
        img = scale(img, (img.get_width() * SCALE, img.get_height() * SCALE))
    if angle != 0:
        img = rotate(img, angle)
    if xflip:
        img = flip(img, xflip, False)
    img_cache[key_] = img
    return img


def pix_to_loc(x: int) -> int:
    """
    Convert scaled pixel to character location X 40x25 (320x200 mode, 8x8 font).
    :param x: 0..959
    :return: 1..40
    """
    return int(((x / SCALE) / 8) + 1)


def loc_to_pix(x: int) -> int:
    """
    Convert character location X 40x25 (320x200 mode, 8x8 font) to scaled pixel.
    :param x: 1..40
    :return:
    """
    return (x - 1) * 8 * SCALE


def loc(x: int, y: int) -> Tuple[int, int]:
    """
    Convert character location 40x25 (320x200 mode, 8x8 font) to scaled pixel.
    :param x: 1..40
    :param y: 1..25
    :return:
    """
    return loc_to_pix(x), loc_to_pix(y)


class Txt(DirtySprite):
    font_cache = {}
    cache = {}

    def __init__(self,
                 size: int,
                 msg: str,
                 color: Tuple[int, int, int],
                 loc: Tuple[int, int],
                 fnt: str = FONT,
                 cached: bool = True,
                 *groups):
        super(Txt, self).__init__(*groups)
        self._x = loc[0]
        self._y = loc[1]
        self._msg = msg
        self._size = size
        self._font = fnt
        self._color = color
        self._cached = cached
        self.image, self.rect = self._update_image()

    @property
    def msg(self):
        return self._msg

    @msg.setter
    def msg(self, msg):
        if self._msg != msg:
            self._msg = msg
            self.image, self.rect = self._update_image()
            self.dirty = 1

    @property
    def color(self):
        return self._msg

    @color.setter
    def color(self, color):
        if self._color != color:
            self._color = color
            self.image, self.rect = self._update_image()
            self.dirty = 1

    def _update_image(self):
        font_key = hash(self._font) + hash(self._size)
        if font_key in Txt.font_cache:
            font_ = Txt.font_cache[font_key]
        else:
            font_ = Font(self._font, self._size)
            Txt.font_cache[font_key] = font_

        if not self._cached:
            img = font_.render(str(self.msg), True, self._color)
            rect = img.get_rect(topleft=(self._x, self._y))
        else:
            key_ = font_key + hash(self.msg) + hash(self._color)
            if key_ in Txt.cache:
                img = Txt.cache[key_]
            else:
                img = font_.render(str(self.msg), True, self._color)
                Txt.cache[key_] = img
            rect = img.get_rect(topleft=(self._x, self._y))
        return img, rect


class StaticSprite(DirtySprite):
    def __init__(self,
                 loc: Tuple[int, int],
                 img: str,
                 color: Tuple[int, int, int] = None,
                 *groups: AbstractGroup):
        super().__init__(*groups)
        self.image = get_img(img, color=color)
        self.rect = self.image.get_rect()
        self.rect.move_ip(loc[0], loc[1])


class Frame(object):
    __slots__ = ('rect', 'duration', 'image', 'move_base', 'name',
                 'dx', 'dy', 'w', 'h', 'angle',
                 'xflip', 'fill', 'blend_flags',
                 'pre_action', 'post_action')

    def __init__(self, name, dx=0, dy=0, w=0, h=0,
                 duration=125, angle=0, xflip=False,
                 fill=None, blend_flags=None, mv=None,
                 pre_action=None, post_action=None):
        self.duration = duration
        self.image = get_img(name, w, h, angle, xflip,
                             fill, blend_flags)
        self.rect = self.image.get_rect().move(dx, dy)
        self.move_base = mv
        #
        self.name = name
        self.dx = dx
        self.dy = dy
        self.w = w
        self.h = h
        self.angle = angle
        self.xflip = xflip
        self.fill = fill
        self.blend_flags = blend_flags
        self.pre_action = pre_action
        self.post_action = post_action

    def rtl(self):
        move_base = None
        if self.move_base:
            move_base = (-self.move_base[0], self.move_base[1])

        return Frame(self.name, -self.dx, self.dy, self.w, self.h,
                     self.duration, -self.angle, not self.xflip, self.fill,
                     self.blend_flags, move_base,
                     self.pre_action, self.post_action)


class AnimatedSprite(DirtySprite):
    def __init__(self, top_left: Tuple[int, int], animations, *groups):
        super(AnimatedSprite, self).__init__(*groups)
        self.anims = animations
        self.animTimer = get_ticks()
        self._speed = 1.0
        self._is_stopped = False

        self.anim = next(iter(self.anims))
        self.frames = self.anims[self.anim]
        self.frameNum = 0
        self.frame = self.frames[self.frameNum]
        self.frame_duration = self.frame.duration / self._speed

        self.image = self.frame.image
        self.rect = Rect(0, 0, 0, 0)
        self.top_left = top_left
        self._update_rect()

    @property
    def x(self):
        return self.top_left[0]

    @x.setter
    def x(self, x):
        self.top_left = (x, self.top_left[1])
        self._update_rect()

    @property
    def y(self) -> int:
        return self.top_left[1]

    @y.setter
    def y(self, y: int):
        self.top_left = (self.top_left[0], y)
        self._update_rect()

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, speed: float):
        self._speed = round(min(3.0, max(0.0, speed)), 3)
        self.frame_duration = self._calc_duration(self.frame.duration)

    @property
    def is_stopped(self):
        return self._is_stopped

    @is_stopped.setter
    def is_stopped(self, stopped: bool):
        self._is_stopped = stopped

    def select_anim(self, anim: str):
        if anim in self.anims:
            self.is_stopped = False
            self.anim = anim
            self.frames = self.anims[anim]
            self.animTimer = get_ticks()
            self.frameNum = -1
            self.frame = None
            self.next_frame()
            self.visible = True
        else:
            self.visible = False

    def set_anim_frame(self, anim: str, frame: int = 0):
        if not self.is_stopped:
            self.is_stopped = True
        if not self.visible:
            self.visible = True
        self.anim = anim
        self.frames = self.anims[anim]
        self.frameNum = frame - 1
        self.next_frame()

    def update(self, current_time, *args):
        if self.visible and not self.is_stopped and self.speed > 0:
            passed = current_time - self.animTimer
            while passed > self.frame_duration:
                passed -= self.frame_duration
                self.animTimer = current_time
                self.next_frame()

    def _calc_duration(self, duration):
        if self.speed > 0:
            return duration / self.speed
        else:
            return duration

    def on_pre_action(self, anim, action):
        pass

    def on_post_action(self, anim, action):
        pass

    def prev_frame(self):
        self.frameNum -= 1
        if self.frameNum == -1:
            self.frameNum = len(self.frames) - 1

        prev = self.frames[self.frameNum]
        if self.frame != prev:
            if self.frame.post_action:
                self.on_post_action(self.anim, self.frame.post_action)
            if self.frame.move_base:  # Undo the current frame move_base
                dx, dy = self.available_move(-self.frame.move_base[0],
                                             -self.frame.move_base[1])
                self.move(dx, dy)
            self.frame = prev
            self.frame_duration = self._calc_duration(self.frame.duration)
            self.image = self.frame.image

            self._update_rect()
            if self.frame.pre_action:
                self.on_pre_action(self.anim, self.frame.pre_action)
            self.dirty = 1

    def next_frame(self):
        self.frameNum += 1
        if self.frameNum == len(self.frames):
            self.frameNum = 0
        next_ = self.frames[self.frameNum]
        if self.frame != next_:
            if self.frame and self.frame.post_action:
                cur_anim = self.anim
                self.on_post_action(self.anim, self.frame.post_action)
                if cur_anim != self.anim or self.is_stopped:
                    # Animation changed or stopped, don't process next frame
                    return

            self.frame = next_
            self.frame_duration = self._calc_duration(self.frame.duration)
            self.image = self.frame.image
            if self.frame.move_base:
                dx, dy = self.available_move(self.frame.move_base[0],
                                             self.frame.move_base[1])
                self.move(dx, dy)
            self._update_rect()
            if self.frame.pre_action:
                self.on_pre_action(self.anim, self.frame.pre_action)
            self.dirty = 1

    def _update_rect(self):
        self.rect.size = self.frame.rect.size
        self.rect.topleft = self.top_left
        self.rect.move_ip(self.frame.rect.x, self.frame.rect.y)

    @staticmethod
    def available_move(dx, dy):
        return dx, dy

    def move(self, dx, dy):
        self.top_left = (self.top_left[0] + dx, self.top_left[1] + dy)
        self.rect.move_ip(dx, dy)
        self.dirty = 1


def rtl_anims(anims):
    rtl = {}
    for anim, frames in anims.items():
        rtl[anim] = [f.rtl() for f in frames]
    return rtl


def serpent_anims():
    return {
        'idle': [
            Frame('stage/serpent1.gif'),
        ],
        'bite': [
            Frame('stage/serpent1.gif'),
            Frame('stage/serpent2.gif'),
            Frame('stage/serpent3.gif'),
            Frame('stage/serpent4.gif', dx=-3 * SCALE, dy=-1 * SCALE),
            Frame('stage/serpent3.gif'),
            Frame('stage/serpent2.gif'),
            Frame('stage/serpent1.gif', duration=100000),
        ]
    }


def barb_anims(subdir: str):
    return {
        'debout': [
            Frame(f'{subdir}/debout.gif'),
        ],
        'attente': [
            Frame(f'{subdir}/attente1.gif', pre_action='attente1'),
            Frame(f'{subdir}/attente2.gif'),
            Frame(f'{subdir}/attente3.gif'),
            Frame(f'{subdir}/attente2.gif'),
        ],
        'avance': [
            Frame(f'{subdir}/marche1.gif', mv=(8 * SCALE, 0)),
            Frame(f'{subdir}/marche2.gif', mv=(8 * SCALE, 0)),
            Frame(f'{subdir}/marche3.gif', mv=(8 * SCALE, 0)),
            Frame(f'{subdir}/marche2.gif', mv=(8 * SCALE, 0)),
        ],
    }


def sorcier_anims():
    return {
        'debout': [
            Frame(f'sprites/drax1.gif'),
        ],
        'attaque': [
            Frame(f'sprites/drax2.gif'),
        ],
    }


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
    avance1 = enum.auto()
    avance2 = enum.auto()
    avance3 = enum.auto()
    avance4 = enum.auto()
    assis = enum.auto()
    assis2 = enum.auto()
    cou = enum.auto()
    coupdepied = enum.auto()
    coupdetete = enum.auto()
    debout = enum.auto()
    decapite = enum.auto()
    devant = enum.auto()
    finderoulade = enum.auto()
    front = enum.auto()
    genou = enum.auto()
    protegeD = enum.auto()
    protegeD1 = enum.auto()
    protegeH = enum.auto()
    protegeH1 = enum.auto()
    recule1 = enum.auto()
    recule2 = enum.auto()
    recule3 = enum.auto()
    recule4 = enum.auto()
    releve = enum.auto()
    roulade = enum.auto()
    rouladeAV = enum.auto()
    rouladeAR = enum.auto()
    saute = enum.auto()
    #
    mortSORCIER = enum.auto()
    sorcierFINI = enum.auto()


class Barbarian(AnimatedSprite):
    def __init__(self, x, y, subdir: str, rtl=False, anim='debout'):
        super(Barbarian, self).__init__(
            (x, y),
            rtl_anims(barb_anims(subdir)) if rtl else barb_anims(subdir))
        self.rtl = rtl
        self.select_anim(anim)
        self.ltr_anims = self.anims
        self.rtl_anims = rtl_anims(self.anims)
        #
        self.clavierX = 7
        self.clavierY = 7
        self.attaque = False
        #
        self.yAtt = 17
        self.xAtt = 27 if rtl else 15
        self.yF = 15  # front
        self.yT = 16  # tete
        self.yM = 18  # corps
        self.yG = 20  # genou
        self.xF = pix_to_loc(self.x) if rtl else pix_to_loc(self.x) + 4
        self.xT = pix_to_loc(self.x) if rtl else pix_to_loc(self.x) + 4
        self.xM = pix_to_loc(self.x) if rtl else pix_to_loc(self.x) + 4
        self.xG = pix_to_loc(self.x) if rtl else pix_to_loc(self.x) + 4
        #
        self.reftemps = 0
        self.sang = False
        self.attente = 1
        self.occupe = False
        self.sortie = False
        self.levier: Levier = Levier.neutre
        self.state: State = State.debout
        self.infoCoup = 0
        self.infoDegatF = 0
        self.infoDegatG = 0
        self.infoDegatT = 0
        self.bonus = False

    def x_loc(self):
        return pix_to_loc(self.x)

    def turn_around(self, rtl):
        self.anims = self.rtl_anims if rtl else self.ltr_anims
        self.select_anim(self.anim)
        self.rtl = rtl

    def inc_clavier_x(self):
        if self.clavierX < 9:
            self.clavierX += 1

    def dec_clavier_x(self):
        if self.clavierX > 5:
            self.clavierX -= 1

    def inc_clavier_y(self):
        if self.clavierY < 9:
            self.clavierY += 1

    def dec_clavier_y(self):
        if self.clavierY > 5:
            self.clavierY -= 1

    def clavier(self):
        if self.clavierX <= 6 and self.clavierY <= 6:
            self.levier = Levier.hautD if self.rtl else Levier.hautG
        if self.clavierX >= 8 and self.clavierY <= 6:
            self.levier = Levier.hautG if self.rtl else Levier.hautD
        if self.clavierX <= 6 and self.clavierY >= 8:
            self.levier = Levier.basD if self.rtl else Levier.basG
        if self.clavierX >= 8 and self.clavierY >= 8:
            self.levier = Levier.basG if self.rtl else Levier.basD

        if self.clavierX <= 6 and self.clavierY == 7:
            self.levier = Levier.gauche
        if self.clavierX >= 8 and self.clavierY == 7:
            self.levier = Levier.droite
        if self.clavierX == 7 and self.clavierY >= 8:
            self.levier = Levier.bas
        if self.clavierX == 7 and self.clavierY <= 6:
            self.levier = Levier.haut

    def on_pre_action(self, anim, action):
        if anim == 'attente':
            if action == 'attente1':
                get_snd('attente.ogg').play()


class Sorcier(AnimatedSprite):
    def __init__(self, x, y, rtl=False, anim='idle'):
        super(Sorcier, self).__init__(
            (x, y),
            rtl_anims(sorcier_anims()) if rtl else sorcier_anims())
        self.rtl = rtl
        self.select_anim(anim)
        self.ltr_anims = self.anims
        self.rtl_anims = rtl_anims(self.anims)
        #
        self.clavierX = 7
        self.clavierY = 7
        self.attaque = False
        #
        self.yAtt = 17
        self.xAtt = 27 if rtl else 15
        self.yF = 15  # front
        self.yT = 16  # tete
        self.yM = 18  # corps
        self.yG = 20  # genou
        self.xF = pix_to_loc(self.x) if rtl else pix_to_loc(self.x) + 4
        self.xT = pix_to_loc(self.x) if rtl else pix_to_loc(self.x) + 4
        self.xM = pix_to_loc(self.x) if rtl else pix_to_loc(self.x) + 4
        self.xG = pix_to_loc(self.x) if rtl else pix_to_loc(self.x) + 4
        #
        self.reftemps = 0
        self.sang = False
        self.attente = 1
        self.occupe = False
        self.sortie = False
        self.levier: Levier = Levier.neutre
        self.state: State = State.debout
        self.infoDegatG = 0
        self.infoDegatT = 0
        self.bonus = False

    def x_loc(self):
        return pix_to_loc(self.x)

    def clavier(self):
        pass

    def on_pre_action(self, anim, action):
        pass
