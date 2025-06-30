# -*- coding: utf-8 -*-
import enum
from os.path import join
from typing import Tuple, Dict

from pygame import image, Rect
from pygame.font import Font
from pygame.mixer import Sound
from pygame.sprite import DirtySprite, AbstractGroup, Group
from pygame.surface import Surface
from pygame.time import get_ticks
from pygame.transform import scale, rotate, flip

from settings import IMG_PATH, SCALE, FONT, SND_PATH, Theme, CHAR_W

snd_cache: Dict[int, Sound] = {}
img_cache: Dict[int, Surface] = {}


def get_snd(name: str) -> Sound:
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


def px2loc(x: int) -> int:
    """
    Convert scaled pixel to character location X 40x25 (320x200 mode, 8x8 font).
    :param x: 0..959
    :return: 1..40
    """
    return int(((x / SCALE) / CHAR_W) + 1)


def loc2px(x: int) -> int:
    """
    Convert character location X 40x25 (320x200 mode, 8x8 font) to scaled pixel.
    :param x: 1..40
    :return:
    """
    return (x - 1) * CHAR_W * SCALE


def loc(x: int, y: int) -> Tuple[int, int]:
    """
    Convert character location 40x25 (320x200 mode, 8x8 font) to scaled pixel.
    :param x: 1..40
    :param y: 1..25
    :return:
    """
    return loc2px(x), loc2px(y)


class Rectangle(Group):
    def __init__(self,
                 x, y, w, h,
                 color: Tuple[int, int, int],
                 border_width=1,
                 lbl='',
                 *groups: AbstractGroup):
        super().__init__(*groups)
        self.border_width = border_width
        self.img = Surface((self.border_width, self.border_width))
        self.img.fill(color, self.img.get_rect())
        #
        self.left = DirtySprite(self)
        self.left.rect = Rect(0, 0, self.border_width, 0)
        #
        self.right = DirtySprite(self)
        self.right.rect = Rect(0, 0, self.border_width, 0)
        #
        self.top = DirtySprite(self)
        self.top.rect = Rect(0, 0, 0, self.border_width)
        #
        self.bottom = DirtySprite(self)
        self.bottom.rect = Rect(0, 0, 0, self.border_width)
        self.rect = Rect(x, y, w, h)
        #
        self.lbl = Txt(int(h) - self.border_width * 2 - 1, lbl, color, (0, 0), self)
        self.apply(self.rect)

    def _apply(self, sprite: DirtySprite, topleft, size):
        sprite.rect.topleft = topleft
        if sprite.rect.size != size:
            sprite.rect.size = size
            sprite.image = scale(self.img, size)
        sprite.dirty = 1

    def apply(self, r: Rect):
        self.rect = r
        if self.left.rect.topleft != r.topleft or self.left.rect.h != r.h:
            self.lbl.rect.topleft = (r.x + self.border_width + 1,
                                     r.y + self.border_width + 1)
            self.lbl.dirty = 1
            self._apply(self.left, (r.x, r.y), (self.border_width, r.h))

        x = r.x + r.w - self.border_width
        if self.right.rect.topleft != (x, r.y) or self.right.rect.h != r.h:
            self._apply(self.right, (x, r.y), (self.border_width, r.h))

        if self.top.rect.topleft != (r.x, r.y) or self.top.rect.w != r.w:
            self._apply(self.top, (r.x, r.y), (r.w, self.border_width))

        y = r.y + r.h - self.border_width
        if self.bottom.rect.topleft != (r.x, y) or self.bottom.rect.w != r.w:
            self._apply(self.bottom, (r.x, y), (r.w, self.border_width))

    def move_to(self, x, y):
        self.apply(self.rect.move_to(x=x, y=y))


class Txt(DirtySprite):
    font_cache = {}
    cache = {}

    def __init__(self,
                 size: int,
                 msg: str,
                 color: Tuple[int, int, int],
                 loc: Tuple[int, int],
                 *groups,
                 fnt: str = FONT,
                 cached: bool = True):
        super(Txt, self).__init__(*groups)
        self._x = loc[0]
        self._y = loc[1]
        self._msg = msg
        self._size = size
        self._font = fnt
        self._color = color
        self._cached = cached
        self.image, self.rect = self._update_image()

    @staticmethod
    def Debug(x, y, msg='') -> 'Txt':
        return Txt(8, msg, Theme.DEBUG, (x, y), cached=False)

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
                 'pre_action', 'post_action', 'tick', 'is_tickable')

    def __init__(self, name, dx=0, dy=0, w=0, h=0,
                 duration=125, angle=0, xflip=False,
                 fill=None, blend_flags=None, mv=None,
                 pre_action=None, post_action=None, tick=-1):
        """
        `tick` end tick. A next tick will apply a next frame.
        """
        self.duration = duration
        self.tick = tick
        self.is_tickable = (tick >= 0)
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
        super().__init__(*groups)
        self.anims = animations
        self.animTimer = get_ticks()
        self.animTick = 0
        self._speed = 1.0
        self._is_stopped = False

        self.anim = next(iter(self.anims))
        self.frames = self.anims[self.anim]
        self.frameNum = 0
        self.frame = self.frames[self.frameNum]
        self.frame_duration = self.frame.duration
        self.frame_tick = self.frame.tick

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
        self.frame_tick = self._calc_frame_tick(self.frame.tick)

    @property
    def is_stopped(self):
        return self._is_stopped

    @is_stopped.setter
    def is_stopped(self, stopped: bool):
        self._is_stopped = stopped

    def animate(self, anim: str, tick=0):
        if anim in self.anims:
            self.is_stopped = False
            self.anim = anim
            self.frames = self.anims[anim]
            self.animTimer = get_ticks()
            self.animTick = tick
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
            self.animTick += 1
            if not self.frame.is_tickable:
                passed = current_time - self.animTimer
                while passed > self.frame_duration:
                    # TODO: Rewind mixed frame types
                    passed -= self.frame_duration
                    self.animTimer = current_time
                    self.next_frame()
            else:
                while self.animTick > self.frame_tick:
                    self.animTimer = current_time
                    self.next_frame()

    def _calc_duration(self, duration):
        if self.speed == 0 or self.speed == 1:
            return duration
        else:
            return duration / self.speed

    def _calc_frame_tick(self, tick):
        if self.speed == 0 or self.speed == 1:
            return tick
        else:
            return tick / self.speed

    def on_pre_action(self, anim, action):
        pass

    def on_post_action(self, anim, action):
        if action == 'stop':
            self.is_stopped = True

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
            if self.frame.is_tickable:
                self.frame_tick = self._calc_frame_tick(self.frame.tick)
            else:
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
            self.animTick = 0
        next_ = self.frames[self.frameNum]
        if self.frame != next_:
            if self.frame and self.frame.post_action:
                cur_anim = self.anim
                self.on_post_action(self.anim, self.frame.post_action)
                if cur_anim != self.anim or self.is_stopped:
                    # Animation changed or stopped, don't process next frame
                    return

            self.frame = next_
            if self.frame.is_tickable:
                self.frame_tick = self._calc_frame_tick(self.frame.tick)
            else:
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
            Frame('stage/serpent1.gif', post_action='stop'),
        ]
    }


def barb_anims(subdir: str):
    return {
        'debout': [
            Frame(f'{subdir}/debout.gif'),
        ],
        'attente': [
            Frame(f'{subdir}/attente1.gif', tick=15),
            Frame(f'{subdir}/attente2.gif', tick=23),
            Frame(f'{subdir}/attente3.gif', tick=30),
            Frame(f'{subdir}/attente2.gif', tick=37),
            Frame(f'{subdir}/attente1.gif', tick=50),
        ],
        'avance': [
            # @formatter:off
            Frame(f'{subdir}/marche1.gif', tick=9,  mv=(CHAR_W * SCALE, 0)),
            Frame(f'{subdir}/marche2.gif', tick=17, mv=(CHAR_W * SCALE, 0)),
            Frame(f'{subdir}/marche3.gif', tick=27, mv=(CHAR_W * SCALE, 0)),
            Frame(f'{subdir}/debout.gif',  tick=36, mv=(CHAR_W * SCALE, 0)),
            Frame(f'{subdir}/debout.gif',  tick=37),
            # @formatter:on
        ],
        'recule': [
            # @formatter:off
            Frame(f'{subdir}/marche3.gif', tick=9,  mv=(-CHAR_W * SCALE, 0)),
            Frame(f'{subdir}/marche2.gif', tick=18, mv=(-CHAR_W * SCALE, 0)),
            Frame(f'{subdir}/marche1.gif', tick=26, mv=(-CHAR_W * SCALE, 0)),
            Frame(f'{subdir}/debout.gif',  tick=36, mv=(-CHAR_W * SCALE, 0)),
            Frame(f'{subdir}/debout.gif',  tick=37),
            # @formatter:on
        ],
        'saute': [
            # @formatter:off
            Frame(f'{subdir}/saut1.gif',  tick=13),
            Frame(f'{subdir}/saut2.gif',  tick=30),
            Frame(f'{subdir}/saut1.gif',  tick=40),
            Frame(f'{subdir}/debout.gif', tick=46),
            # @formatter:on
        ],
        'assis': [
            Frame(f'{subdir}/assis1.gif'),
            Frame(f'{subdir}/assis2.gif'),
        ],
        'releve': [
            Frame(f'{subdir}/assis1.gif'),
        ],
        'rouladeAV': [
            # @formatter:off
            Frame(f'{subdir}/roulade1.gif',             tick=4,  mv=(CHAR_W * SCALE, 0)),  # noqa
            Frame(f'{subdir}/roulade1.gif',             tick=7,  mv=(CHAR_W * SCALE, 0)),  # noqa
            Frame(f'{subdir}/roulade2.gif',             tick=10, mv=(CHAR_W * SCALE, 0)),  # noqa
            Frame(f'{subdir}/roulade2.gif',             tick=13, mv=(CHAR_W * SCALE, 0)),  # noqa
            Frame(f'{subdir}/roulade3.gif',             tick=16, mv=(CHAR_W * SCALE, 0)),  # noqa
            Frame(f'{subdir}/roulade3.gif',             tick=19, mv=(CHAR_W * SCALE, 0)),  # noqa
            Frame(f'{subdir}/roulade2.gif', xflip=True, tick=22, mv=(CHAR_W * SCALE, 0)),  # noqa
            Frame(f'{subdir}/roulade2.gif', xflip=True, tick=25, mv=(CHAR_W * SCALE, 0)),  # noqa
            Frame(f'{subdir}/roulade5.gif',             tick=28, mv=(CHAR_W * SCALE, 0)),  # noqa
            Frame(f'{subdir}/roulade5.gif',             tick=30, mv=(CHAR_W * SCALE, 0)),  # noqa
            Frame(f'{subdir}/roulade1.gif', xflip=True, tick=34, mv=(CHAR_W * SCALE, 0)),  # noqa
            # @formatter:on
        ],
        'rouladeAR': [
            # @formatter:off
            Frame(f'{subdir}/roulade1.gif', xflip=True, tick=2,                         ),  # noqa
            Frame(f'{subdir}/roulade1.gif', xflip=True, tick=5,  mv=(-CHAR_W * SCALE, 0)),  # noqa
            Frame(f'{subdir}/roulade5.gif',             tick=8,  mv=(-CHAR_W * SCALE, 0)),  # noqa
            Frame(f'{subdir}/roulade2.gif', xflip=True, tick=11, mv=(-CHAR_W * SCALE, 0)),  # noqa
            Frame(f'{subdir}/roulade2.gif', xflip=True, tick=14, mv=(-CHAR_W * SCALE, 0)),  # noqa
            Frame(f'{subdir}/roulade3.gif',             tick=17, mv=(-CHAR_W * SCALE, 0)),  # noqa
            Frame(f'{subdir}/roulade3.gif',             tick=20, mv=(-CHAR_W * SCALE, 0)),  # noqa
            Frame(f'{subdir}/roulade2.gif',             tick=23, mv=(-CHAR_W * SCALE, 0)),  # noqa
            Frame(f'{subdir}/roulade2.gif',             tick=26, mv=(-CHAR_W * SCALE, 0)),  # noqa
            Frame(f'{subdir}/roulade1.gif',             tick=29, mv=(-CHAR_W * SCALE, 0)),  # noqa
            Frame(f'{subdir}/roulade1.gif',             tick=34, mv=(-CHAR_W * SCALE, 0)),  # noqa
            # @formatter:on
        ],
        'protegeH': [
            # @formatter:off
            Frame(f'{subdir}/marche1.gif',  tick=5, mv=(-CHAR_W * SCALE, 0)),
            Frame(f'{subdir}/protegeH.gif', tick=9),
            # @formatter:on
        ],
        'protegeD': [
            Frame(f'{subdir}/protegeH.gif', tick=5),
            Frame(f'{subdir}/protegeD.gif', tick=9),
        ],
        'cou': [
            # @formatter:off
            Frame(f'{subdir}/protegeH.gif', tick=15),
            Frame(f'{subdir}/cou2.gif',     tick=30),
            Frame(f'{subdir}/cou3.gif',     tick=46),
            # @formatter:on
        ],
        'devant': [
            # @formatter:off
            Frame(f'{subdir}/devant1.gif', tick=10),
            Frame(f'{subdir}/devant2.gif', tick=20),
            Frame(f'{subdir}/devant3.gif', tick=30),
            Frame(f'{subdir}/devant2.gif', tick=46),
            # @formatter:on
        ],
        'genou': [
            # @formatter:off
            Frame(f'{subdir}/genou1.gif', tick=10, dx=CHAR_W * SCALE / 4),
            Frame(f'{subdir}/assis2.gif', tick=20),
            Frame(f'{subdir}/genou3.gif', tick=30, dx=CHAR_W * SCALE / 4),
            Frame(f'{subdir}/assis2.gif', tick=46),
            # @formatter:on
        ],
        'araignee': [
            # @formatter:off
            Frame(f'{subdir}/toile1.gif', tick=7),
            Frame(f'{subdir}/toile2.gif', tick=12),
            Frame(f'{subdir}/toile3.gif', tick=18),
            Frame(f'{subdir}/toile4.gif', tick=25),
            # @formatter:on
        ],
        'coupdepied': [
            # @formatter:off
            Frame(f'{subdir}/pied1.gif',  tick=15),
            Frame(f'{subdir}/pied2.gif',  tick=30),
            Frame(f'{subdir}/pied1.gif',  tick=45),
            Frame(f'{subdir}/debout.gif', tick=51),
            # @formatter:on
        ],
        'coupdetete': [
            # @formatter:off
            Frame(f'{subdir}/tete1.gif', tick=18),
            Frame(f'{subdir}/tete2.gif', tick=28, mv=( CHAR_W * SCALE, 0)),  # noqa
            Frame(f'{subdir}/tete1.gif', tick=38, mv=(-CHAR_W * SCALE, 0)),  # noqa
            # @formatter:on
        ],
        'decapite': [
            # @formatter:off
            Frame(f'{subdir}/retourne1.gif', tick=4,  mv=(CHAR_W * SCALE, 0)),  # noqa
            Frame(f'{subdir}/retourne1.gif', tick=5,  mv=(CHAR_W * SCALE, 0)),  # noqa
            Frame(f'{subdir}/retourne2.gif', tick=9,                        ),  # noqa
            Frame(f'{subdir}/retourne2.gif', tick=14, mv=(CHAR_W * SCALE, 0)),  # noqa
            Frame(f'{subdir}/retourne3.gif', tick=15,                       ),  # noqa
            Frame(f'{subdir}/retourne3.gif', tick=19, mv=(CHAR_W * SCALE, 0)),  # noqa
            Frame(f'{subdir}/retourne3.gif', tick=24, mv=(CHAR_W * SCALE, 0)),  # noqa
            Frame(f'{subdir}/retourne3.gif', tick=29,                       ),  # noqa
            Frame(f'{subdir}/protegeH.gif',  tick=33,                       ),  # noqa
            Frame(f'{subdir}/cou2.gif',      tick=39,                       ),  # noqa
            Frame(f'{subdir}/cou3.gif',      tick=51,                       ),  # noqa
            Frame(f'{subdir}/cou2.gif',      tick=60,                       ),  # noqa
            # @formatter:on
        ],
        'front': [
            Frame(f'{subdir}/front1.gif', tick=5),
            Frame(f'{subdir}/front2.gif', tick=23),
            Frame(f'{subdir}/front3.gif', tick=30),
            Frame(f'{subdir}/front2.gif', tick=46),
        ],
        'retourne': [
            Frame(f'{subdir}/retourne1.gif', tick=5),
            Frame(f'{subdir}/retourne2.gif', tick=10),
            Frame(f'{subdir}/retourne3.gif', tick=16),
        ],
        'vainqueur': [
            Frame(f'{subdir}/vainqueur1.gif', xflip=True, tick=18),
            Frame(f'{subdir}/vainqueur2.gif', xflip=True, tick=35),
            Frame(f'{subdir}/vainqueur3.gif', xflip=True, tick=85),
            Frame(f'{subdir}/vainqueur2.gif', xflip=True, tick=100),
            Frame(f'{subdir}/vainqueur1.gif', xflip=True, tick=101),
        ],
    }


def barb_anims_rtl(subdir: str):
    return {
        'debout': [
            Frame(f'{subdir}/debout.gif', xflip=True),
        ],
        'attente': [
            Frame(f'{subdir}/attente1.gif', xflip=True, tick=15),
            Frame(f'{subdir}/attente2.gif', xflip=True, tick=23, dx=-CHAR_W * SCALE),
            Frame(f'{subdir}/attente3.gif', xflip=True, tick=30, dx=-CHAR_W * SCALE),
            Frame(f'{subdir}/attente2.gif', xflip=True, tick=37, dx=-CHAR_W * SCALE),
            Frame(f'{subdir}/attente1.gif', xflip=True, tick=50),
        ],
        'avance': [
            # @formatter:off
            Frame(f'{subdir}/marche1.gif', xflip=True, tick=9,  mv=(-CHAR_W * SCALE, 0)),
            Frame(f'{subdir}/marche2.gif', xflip=True, tick=17, mv=(-CHAR_W * SCALE, 0)),
            Frame(f'{subdir}/marche3.gif', xflip=True, tick=27, mv=(-CHAR_W * SCALE, 0)),
            Frame(f'{subdir}/debout.gif',  xflip=True, tick=36, mv=(-CHAR_W * SCALE, 0)),
            Frame(f'{subdir}/debout.gif',  xflip=True, tick=37),
            # @formatter:on
        ],
        'recule': [
            # @formatter:off
            Frame(f'{subdir}/marche3.gif', xflip=True, tick=9,  mv=(CHAR_W * SCALE, 0)),
            Frame(f'{subdir}/marche2.gif', xflip=True, tick=18, mv=(CHAR_W * SCALE, 0)),
            Frame(f'{subdir}/marche1.gif', xflip=True, tick=26, mv=(CHAR_W * SCALE, 0)),
            Frame(f'{subdir}/debout.gif',  xflip=True, tick=36, mv=(CHAR_W * SCALE, 0)),
            Frame(f'{subdir}/debout.gif',  xflip=True, tick=37),
            # @formatter:on
        ],
        'saute': [
            # @formatter:off
            Frame(f'{subdir}/saut1.gif',  xflip=True, tick=13, dx=-CHAR_W * SCALE),
            Frame(f'{subdir}/saut2.gif',  xflip=True, tick=30, dx=-CHAR_W * SCALE),
            Frame(f'{subdir}/saut1.gif',  xflip=True, tick=40, dx=-CHAR_W * SCALE),
            Frame(f'{subdir}/debout.gif', xflip=True, tick=46),
            # @formatter:on
        ],
        'assis': [
            Frame(f'{subdir}/assis1.gif', xflip=True),
            Frame(f'{subdir}/assis2.gif', xflip=True),
        ],
        'releve': [
            Frame(f'{subdir}/assis1.gif', xflip=True),
        ],
        'rouladeAV': [
            # @formatter:off
            Frame(f'{subdir}/roulade1.gif', xflip=True, tick=4,  mv=(-CHAR_W * SCALE, 0)),  # noqa
            Frame(f'{subdir}/roulade1.gif', xflip=True, tick=7,  mv=(-CHAR_W * SCALE, 0)),  # noqa
            Frame(f'{subdir}/roulade2.gif', xflip=True, tick=10, mv=(-CHAR_W * SCALE, 0)),  # noqa
            Frame(f'{subdir}/roulade2.gif', xflip=True, tick=13, mv=(-CHAR_W * SCALE, 0)),  # noqa
            Frame(f'{subdir}/roulade3.gif',             tick=16, mv=(-CHAR_W * SCALE, 0)),  # noqa
            Frame(f'{subdir}/roulade3.gif',             tick=19, mv=(-CHAR_W * SCALE, 0)),  # noqa
            Frame(f'{subdir}/roulade2.gif',             tick=22, mv=(-CHAR_W * SCALE, 0)),  # noqa
            Frame(f'{subdir}/roulade2.gif',             tick=25, mv=(-CHAR_W * SCALE, 0)),  # noqa
            Frame(f'{subdir}/roulade5.gif',             tick=28, mv=(-CHAR_W * SCALE, 0)),  # noqa
            Frame(f'{subdir}/roulade5.gif',             tick=30, mv=(-CHAR_W * SCALE, 0)),  # noqa
            Frame(f'{subdir}/roulade1.gif',             tick=34, mv=(-CHAR_W * SCALE, 0)),  # noqa
            # @formatter:on
        ],
        'rouladeAR': [
            # @formatter:off
            Frame(f'{subdir}/roulade1.gif',             tick=2,                        ),  # noqa
            Frame(f'{subdir}/roulade1.gif',             tick=5,  mv=(CHAR_W * SCALE, 0)),  # noqa
            Frame(f'{subdir}/roulade5.gif',             tick=8,  mv=(CHAR_W * SCALE, 0)),  # noqa
            Frame(f'{subdir}/roulade2.gif',             tick=11, mv=(CHAR_W * SCALE, 0)),  # noqa
            Frame(f'{subdir}/roulade2.gif',             tick=14, mv=(CHAR_W * SCALE, 0)),  # noqa
            Frame(f'{subdir}/roulade3.gif',             tick=17, mv=(CHAR_W * SCALE, 0)),  # noqa
            Frame(f'{subdir}/roulade3.gif',             tick=20, mv=(CHAR_W * SCALE, 0)),  # noqa
            Frame(f'{subdir}/roulade2.gif', xflip=True, tick=23, mv=(CHAR_W * SCALE, 0)),  # noqa
            Frame(f'{subdir}/roulade2.gif', xflip=True, tick=26, mv=(CHAR_W * SCALE, 0)),  # noqa
            Frame(f'{subdir}/roulade1.gif', xflip=True, tick=29, mv=(CHAR_W * SCALE, 0)),  # noqa
            Frame(f'{subdir}/roulade1.gif', xflip=True, tick=34, mv=(CHAR_W * SCALE, 0)),  # noqa
            # @formatter:on
        ],
        'protegeH': [
            # @formatter:off
            Frame(f'{subdir}/marche1.gif',  xflip=True, tick=5, mv=(CHAR_W * SCALE, 0)),
            Frame(f'{subdir}/protegeH.gif', xflip=True, tick=9, dx=-CHAR_W * SCALE),
            # @formatter:on
        ],
        'protegeD': [
            Frame(f'{subdir}/protegeH.gif', xflip=True, tick=5, dx=-CHAR_W * SCALE),
            Frame(f'{subdir}/protegeD.gif', xflip=True, tick=9, dx=-CHAR_W * SCALE),
        ],
        'cou': [
            # @formatter:off
            Frame(f'{subdir}/protegeH.gif', xflip=True, tick=15, dx=-CHAR_W * SCALE    ),  # noqa
            Frame(f'{subdir}/cou2.gif',     xflip=True, tick=30, dx=-CHAR_W * SCALE    ),  # noqa
            Frame(f'{subdir}/cou3.gif',     xflip=True, tick=46, dx=-4 * CHAR_W * SCALE),  # noqa
            # @formatter:on
        ],
        'devant': [
            # @formatter:off
            Frame(f'{subdir}/devant1.gif', xflip=True, tick=10),
            Frame(f'{subdir}/devant2.gif', xflip=True, tick=20),
            Frame(f'{subdir}/devant3.gif', xflip=True, tick=30, dx=-3 * CHAR_W * SCALE),
            Frame(f'{subdir}/devant2.gif', xflip=True, tick=46),
            # @formatter:on
        ],
        'genou': [
            # @formatter:off
            Frame(f'{subdir}/genou1.gif', xflip=True, tick=10, dx=-CHAR_W * SCALE / 4),
            Frame(f'{subdir}/assis2.gif', xflip=True, tick=20),
            Frame(f'{subdir}/genou3.gif', xflip=True, tick=30, dx=-CHAR_W * SCALE / 4
                                                                  - 3 * CHAR_W * SCALE),
            Frame(f'{subdir}/assis2.gif', xflip=True, tick=46),
            # @formatter:on
        ],
        'araignee': [
            # @formatter:off
            Frame(f'{subdir}/toile1.gif', xflip=True, tick=7,  dx=-CHAR_W * SCALE),
            Frame(f'{subdir}/toile2.gif', xflip=True, tick=12, dx=-CHAR_W * SCALE),
            Frame(f'{subdir}/toile3.gif', xflip=True, tick=18, dx=-CHAR_W * SCALE),
            Frame(f'{subdir}/toile4.gif', xflip=True, tick=25, dx=-3 * CHAR_W * SCALE),
            # @formatter:on
        ],
        'coupdepied': [
            # @formatter:off
            Frame(f'{subdir}/pied1.gif',  xflip=True, tick=15, dx=-CHAR_W * SCALE),
            Frame(f'{subdir}/pied2.gif',  xflip=True, tick=30, dx=-CHAR_W * SCALE),
            Frame(f'{subdir}/pied1.gif',  xflip=True, tick=45, dx=-CHAR_W * SCALE),
            Frame(f'{subdir}/debout.gif', xflip=True, tick=51),
            # @formatter:on
        ],
        'coupdetete': [
            # @formatter:off
            Frame(f'{subdir}/tete1.gif', xflip=True, tick=18),
            Frame(f'{subdir}/tete2.gif', xflip=True, tick=28),
            Frame(f'{subdir}/tete1.gif', xflip=True, tick=38),
            # @formatter:on
        ],
        'decapite': [
            # @formatter:off
            Frame(f'{subdir}/retourne1.gif', xflip=True, tick=4,  mv=(-CHAR_W * SCALE, 0)),  # noqa
            Frame(f'{subdir}/retourne1.gif', xflip=True, tick=5,  mv=(-CHAR_W * SCALE, 0)),  # noqa
            Frame(f'{subdir}/retourne2.gif', xflip=True, tick=9,                         ),  # noqa
            Frame(f'{subdir}/retourne2.gif', xflip=True, tick=14, mv=(-CHAR_W * SCALE, 0)),  # noqa
            Frame(f'{subdir}/retourne3.gif', xflip=True, tick=15,                        ),  # noqa
            Frame(f'{subdir}/retourne3.gif', xflip=True, tick=19, mv=(-CHAR_W * SCALE, 0)),  # noqa
            Frame(f'{subdir}/retourne3.gif', xflip=True, tick=24, mv=(-CHAR_W * SCALE, 0)),  # noqa
            Frame(f'{subdir}/retourne3.gif', xflip=True, tick=29,                        ),  # noqa
            Frame(f'{subdir}/protegeH.gif',  xflip=True, tick=33, dx=-CHAR_W * SCALE     ),  # noqa
            Frame(f'{subdir}/cou2.gif',      xflip=True, tick=39, dx=-CHAR_W * SCALE     ),  # noqa
            Frame(f'{subdir}/cou3.gif',      xflip=True, tick=51, dx=-4 * CHAR_W * SCALE ),  # noqa
            Frame(f'{subdir}/cou2.gif',      xflip=True, tick=60, dx=-CHAR_W * SCALE     ),  # noqa
            # @formatter:on
        ],
        'front': [
            # @formatter:off
            Frame(f'{subdir}/front1.gif', xflip=True, tick=5,  dx=-CHAR_W * SCALE    ),  # noqa
            Frame(f'{subdir}/front2.gif', xflip=True, tick=23, dx=-CHAR_W * SCALE    ),  # noqa
            Frame(f'{subdir}/front3.gif', xflip=True, tick=30, dx=-3 * CHAR_W * SCALE),  # noqa
            Frame(f'{subdir}/front2.gif', xflip=True, tick=46, dx=-CHAR_W * SCALE    ),  # noqa
            # @formatter:on
        ],
        'retourne': [
            Frame(f'{subdir}/retourne1.gif', xflip=True, tick=5),
            Frame(f'{subdir}/retourne2.gif', xflip=True, tick=10),
            Frame(f'{subdir}/retourne3.gif', xflip=True, tick=16),
        ],
        'vainqueur': [
            # @formatter:off
            Frame(f'{subdir}/vainqueur1.gif', xflip=True, tick=18,  dx=-CHAR_W * SCALE),
            Frame(f'{subdir}/vainqueur2.gif', xflip=True, tick=35,  dx=-CHAR_W * SCALE),
            Frame(f'{subdir}/vainqueur3.gif', xflip=True, tick=85,  dx=-CHAR_W * SCALE),
            Frame(f'{subdir}/vainqueur2.gif', xflip=True, tick=100, dx=-CHAR_W * SCALE),
            Frame(f'{subdir}/vainqueur1.gif', xflip=True, tick=101, dx=-CHAR_W * SCALE),
            # @formatter:on
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
    finderoulade = enum.auto()
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
    tombeR = enum.auto()
    touche = enum.auto()
    toucheR = enum.auto()
    #
    fini = enum.auto()
    marianna = enum.auto()
    mortSORCIER = enum.auto()
    sorcierFINI = enum.auto()


class Barbarian(AnimatedSprite):
    def __init__(self, opts, x, y, subdir: str, rtl=False, anim='debout'):
        super().__init__((x, y), barb_anims(subdir))
        self.opts = opts
        self.rtl = rtl
        self.ltr_anims = self.anims
        self.rtl_anims = barb_anims_rtl(subdir)
        self.anims = self.rtl_anims if rtl else self.ltr_anims
        self.animate(anim)
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
        self.xF = px2loc(self.x) if rtl else px2loc(self.x) + 4
        self.xT = px2loc(self.x) if rtl else px2loc(self.x) + 4
        self.xM = px2loc(self.x) if rtl else px2loc(self.x) + 4
        self.xG = px2loc(self.x) if rtl else px2loc(self.x) + 4
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
        self.assis = False
        self.protegeD = False
        self.protegeH = False
        self.sprite = ''
        self.decapite = False
        self.pressedUp = False
        self.pressedDown = False
        self.pressedLeft = False
        self.pressedRight = False
        self.pressedFire = False

    def snd_play(self, snd: str):
        if snd and self.opts.sound:
            get_snd(snd).play()

    def reset_xX(self):
        self.xF = self.x_loc() + (0 if self.rtl else 4)
        self.xT = self.x_loc() + (0 if self.rtl else 4)
        self.xM = self.x_loc() + (0 if self.rtl else 4)
        self.xG = self.x_loc() + (0 if self.rtl else 4)

    def x_loc(self):
        return px2loc(self.x)

    def turn_around(self, rtl):
        self.anims = self.rtl_anims if rtl else self.ltr_anims
        self.animate(self.anim)
        self.rtl = rtl

    def occupe_state(self, state: State, temps: int):
        self.state = state
        self.occupe = True
        self.reftemps = temps

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
        if self.pressedUp:
            self.dec_clavier_y()
        if self.pressedDown:
            self.inc_clavier_y()
        if self.pressedLeft:
            self.dec_clavier_x()
        if self.pressedRight:
            self.inc_clavier_x()
        self.attaque = self.pressedFire

        if self.clavierX <= 6 and self.clavierY <= 6:
            self.levier = Levier.hautG
        if self.clavierX >= 8 and self.clavierY <= 6:
            self.levier = Levier.hautD
        if self.clavierX <= 6 and self.clavierY >= 8:
            self.levier = Levier.basG
        if self.clavierX >= 8 and self.clavierY >= 8:
            self.levier = Levier.basD

        if self.clavierX <= 6 and self.clavierY == 7:
            self.levier = Levier.gauche
        if self.clavierX >= 8 and self.clavierY == 7:
            self.levier = Levier.droite
        if self.clavierX == 7 and self.clavierY >= 8:
            self.levier = Levier.bas
        if self.clavierX == 7 and self.clavierY <= 6:
            self.levier = Levier.haut

    # region actions
    def action_droite(self, temps):
        self.protegeD = False
        state = State.recule if self.rtl else State.avance
        attack = State.decapite if self.rtl else State.devant
        if self.state == state:
            return
        self.state = state
        self.reftemps = temps
        if self.attaque:
            self.occupe_state(attack, temps)

    def action_gauche(self, temps):
        self.protegeH = False
        state = State.avance if self.rtl else State.recule
        attack = State.devant if self.rtl else State.decapite
        if self.state == state:
            return
        self.state = state
        self.reftemps = temps
        if self.attaque and not self.sortie:
            self.occupe_state(attack, temps)

    def action_haut(self, temps):
        self.protegeD = False
        self.protegeH = False
        self.occupe_state(State.saute, temps)
        return

    # endregion actions

    def gestion_attente(self, temps):
        self.reset_xX()
        if temps > self.reftemps + 50:
            self.occupe = False
            self.attente = 1
            self.state = State.debout
        elif temps == self.reftemps + 8:
            self.animate('attente', 8)
            self.snd_play('attente.ogg')

    def gestion_protegeH(self, temps):
        self.reset_xX()
        self.xAtt = self.x_loc() + (4 if self.rtl else 0)
        self.yG = 20
        self.set_anim_frame('protegeH', 1)
        if self.attaque:
            self.occupe_state(State.araignee, temps)

    def gestion_protegeD(self, temps):
        self.xAtt = self.x_loc() + (4 if self.rtl else 0)
        self.yG = 20
        self.reset_xX()
        self.decapite = False
        self.set_anim_frame('protegeD', 1)
        if self.attaque:
            self.occupe_state(State.coupdetete, temps)

    def gestion_cou(self, temps, opponent: 'Barbarian',
                    soncling: iter, songrogne: iter):
        self.reset_xX()
        self.yG = 20
        if temps > self.reftemps + 45:
            self.occupe = False
            self.state = State.debout

        elif temps > self.reftemps + 31:
            self.xAtt = self.x_loc() + (4 if self.rtl else 0)

        elif temps == self.reftemps + 31:
            if opponent.state == State.cou:
                distance = abs(self.x_loc() - opponent.x_loc())
                if (distance < 12
                        and (15 < temps - opponent.reftemps <= 30)
                        # cycle and play cling-sound once (for one player only)
                        and not self.rtl):
                    self.snd_play(next(soncling))
            else:
                self.xT = self.x_loc() + (4 if self.rtl else 0)
                self.xAtt = self.x_loc() + (-3 if self.rtl else 7)

        elif temps == self.reftemps + 16:
            self.snd_play('epee.ogg')
            self.yAtt = self.yT

        elif temps == self.reftemps + 4:
            self.snd_play(next(songrogne))
            self.animate('cou', 4)

    def gestion_devant(self, temps, opponent: 'Barbarian',
                       soncling: iter, songrogne: iter):

        self.reset_xX()
        self.yG = 20
        if temps > self.reftemps + 45:
            self.occupe = False
            self.state = State.debout

        elif temps > self.reftemps + 21:
            self.xAtt = self.x_loc() + (4 if self.rtl else 0)

        elif temps == self.reftemps + 21:
            if (opponent.state == State.devant
                    and (20 < temps - opponent.reftemps <= 30)):
                distance = abs(self.x_loc() - opponent.x_loc())
                # cycle and play cling-sound once (for one player only)
                if distance < 10 and not self.rtl:
                    self.snd_play(next(soncling))
            else:
                self.xM = self.x_loc() + (4 if self.rtl else 0)
                self.xAtt = self.x_loc() + (-2 if self.rtl else 6)

        elif temps == self.reftemps + 11:
            self.snd_play(next(songrogne))
            self.snd_play('epee.ogg')
            self.yAtt = self.yM

        elif temps == self.reftemps:
            self.animate('devant')

    def gestion_genou(self, temps, opponent: 'Barbarian',
                      soncling: iter, songrogne: iter):
        self.xF = self.x_loc() + (4 if self.rtl else 0)
        self.xT = self.x_loc() + (4 if self.rtl else 0)
        self.xM = self.x_loc() + (4 if self.rtl else 0)
        self.xG = self.x_loc() + (0 if self.rtl else 4)
        self.yG = 20
        if temps > self.reftemps + 45:
            self.occupe = False
            self.state = State.assis2
        elif temps > self.reftemps + 21:
            self.xAtt = self.x_loc() + (4 if self.rtl else 0)
        elif temps > self.reftemps + 20:
            if opponent.state == State.genou:
                distance = abs(self.x_loc() - opponent.x_loc())
                # cycle and play cling-sound once (for one player only)
                if distance < 12 and not self.rtl:
                    self.snd_play(next(soncling))
            else:
                self.xG = self.x_loc() + (4 if self.rtl else 0)
                self.xAtt = self.x_loc() + (-3 if self.rtl else 7)
        elif temps == self.reftemps + 11:
            self.snd_play(next(songrogne))
            self.snd_play('epee.ogg')
            self.yAtt = self.yG
        elif temps == self.reftemps:
            self.animate('genou')

    def gestion_araignee(self, temps, opponent: 'Barbarian',
                         soncling: iter, songrogne: iter):
        self.xF = self.x_loc() + (0 if self.rtl else 4)
        self.xT = self.x_loc() + (0 if self.rtl else 4)
        self.xM = self.x_loc() + (4 if self.rtl else 0)
        self.xG = self.x_loc() + (0 if self.rtl else 4)
        self.yAtt = self.yG
        self.xAtt = self.x_loc() + (4 if self.rtl else 0)
        self.yG = 20
        if temps > self.reftemps + 24:
            self.occupe = False
            self.state = State.debout

        elif temps > self.reftemps + 19:
            self.xAtt = self.x_loc() + (4 if self.rtl else 0)

        elif temps > self.reftemps + 18:
            self.snd_play('epee.ogg')
            if opponent.state == State.araignee:
                distance = abs(self.x_loc() - opponent.x_loc())
                # cycle and play cling-sound once (for one player only)
                if distance < 12 and not self.rtl:
                    self.snd_play(next(soncling))
            else:
                self.xAtt = self.x_loc() + (-1 if self.rtl else 5)

        elif temps > self.reftemps + 12:
            self.xAtt = self.x_loc() + (4 if self.rtl else 0)

        elif temps == self.reftemps + 7:
            self.snd_play(next(songrogne))
            self.snd_play('epee.ogg')
            self.xAtt = self.x_loc()

        elif temps == self.reftemps:
            self.animate('araignee')

    def gestion_coupdepied(self, temps):
        self.reset_xX()
        self.yAtt = self.yG
        self.yG = 20
        if temps > self.reftemps + 50:
            self.occupe = False
            self.state = State.debout
        elif temps > self.reftemps + 16:
            self.xAtt = self.x_loc() + (4 if self.rtl else 0)
        elif temps > self.reftemps + 15:
            self.xAtt = self.x_loc() + (-1 if self.rtl else 5)
        elif temps == self.reftemps:
            self.animate('coupdepied')

    def gestion_coupdetete(self, temps):
        self.reset_xX()
        self.yG = 20
        if temps > self.reftemps + 37:
            self.occupe = False
            self.sprite = 'debout'
            self.state = State.debout
        elif temps > self.reftemps + 20:
            self.xAtt = self.x_loc() + (4 if self.rtl else 0)
        elif temps > self.reftemps + 19:
            self.xAtt = self.x_loc() + (0 if self.rtl else 4)
        elif temps > self.reftemps + 18:
            self.xAtt = self.x_loc() + (4 if self.rtl else 0)
        elif temps > self.reftemps + 9:
            self.yAtt = self.yT
        elif temps == self.reftemps:
            self.animate('coupdetete')

    def gestion_decapite(self, temps):
        self.decapite = False
        self.xF = self.x_loc() + (1 if self.rtl else 3)
        self.xT = self.x_loc() + 2
        self.xM = self.x_loc() + 2
        self.xG = self.x_loc() + (0 if self.rtl else 4)
        if temps > self.reftemps + 58:
            self.occupe = False
            self.state = State.debout
        elif temps > self.reftemps + 51:
            self.xAtt = self.x_loc() + (4 if self.rtl else 0)
        elif temps > self.reftemps + 50:
            self.xT = self.x_loc() + (4 if self.rtl else 0)
            self.xAtt = self.x_loc() + (-2 if self.rtl else 6)
        elif temps > self.reftemps + 29:
            self.yAtt = self.yT
        elif temps == self.reftemps + 15:
            self.snd_play('decapite.ogg')
        elif temps == self.reftemps + 2:
            self.animate('decapite', 2)

    def gestion_front(self, temps, opponent: 'Barbarian',
                      soncling: iter, songrogne: iter):
        self.reset_xX()
        self.yG = 20
        if temps > self.reftemps + 45:
            self.occupe = False
            self.state = State.debout

        elif temps > self.reftemps + 24:
            self.xAtt = self.x_loc() + (4 if self.rtl else 0)

        elif temps == self.reftemps + 24:
            if opponent.state == State.front:
                distance = abs(self.x_loc() - opponent.x_loc())
                # cycle and play cling-sound once (for one player only)
                if distance < 12 and not self.rtl:
                    self.snd_play(next(soncling))
            else:
                self.xF = self.x_loc() + (4 if self.rtl else 0)
                self.xAtt = self.x_loc() + (-3 if self.rtl else 7)

        elif temps == self.reftemps + 6:
            self.snd_play(next(songrogne))
            self.snd_play('epee.ogg')
            self.yAtt = self.yF

        elif temps == self.reftemps + 4:
            self.animate('front', 4)

    def gestion_retourne(self, temps):
        self.xAtt = self.x_loc()
        self.reset_xX()
        self.yAtt = 14
        if temps > self.reftemps + 15:
            self.state = State.debout
            self.occupe = False
            self.turn_around(not self.rtl)
        elif self.anim != 'retourne':
            self.animate('retourne')

    def gestion_debout(self):
        self.set_anim_frame('debout', 0)
        self.decapite = True
        self.sang = False
        self.xAtt = self.x_loc() + (0 if self.rtl else 4)
        self.yAtt = 14
        self.yF = 15
        self.yT = 16
        self.yM = 18
        self.yG = 20
        self.reset_xX()

    def gestion_vainqueur(self, temps):
        self.decapite = True
        self.sang = False
        self.xAtt = self.x_loc()
        self.yG = 20
        self.yAtt = 14
        self.reset_xX()
        if temps > self.reftemps + 100:
            self.is_stopped = True
        elif self.anim != 'vainqueur':
            self.animate('vainqueur')


class Sorcier(AnimatedSprite):
    def __init__(self, x, y, rtl=False, anim='idle'):
        super().__init__(
            (x, y),
            rtl_anims(sorcier_anims()) if rtl else sorcier_anims())
        self.rtl = rtl
        self.animate(anim)
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
        self.xF = px2loc(self.x) if rtl else px2loc(self.x) + 4
        self.xT = px2loc(self.x) if rtl else px2loc(self.x) + 4
        self.xM = px2loc(self.x) if rtl else px2loc(self.x) + 4
        self.xG = px2loc(self.x) if rtl else px2loc(self.x) + 4
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
        return px2loc(self.x)

    def clavier(self):
        pass

    def on_pre_action(self, anim, action):
        pass
