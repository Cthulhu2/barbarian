from os.path import join
from typing import Dict, List

from pygame import Surface, image
from pygame.transform import scale, rotate, flip

from settings import IMG_PATH, SCALE, CHAR_W, CHAR_H

img_cache: Dict[int, Surface] = {}


def get_img(name, w=0, h=0, angle=0, xflip=False, fill=None, blend_flags=0,
            color=None) -> Surface:
    key_ = sum((hash(name), hash(w), hash(h), hash(angle), hash(xflip),
                hash(fill), hash(blend_flags), hash(color)))

    if key_ in img_cache:
        return img_cache[key_]

    img: Surface
    if name == 'empty':
        img = Surface((0, 0))
    elif name == 'fill':
        img = Surface((1, 1))
        if fill:
            img = img.copy()
            img.fill(fill)
    elif color:
        img = image.load(join(IMG_PATH, name))
        img.set_colorkey(color)
        img = img.convert_alpha()
    else:
        img = image.load(join(IMG_PATH, name)).convert_alpha()
    #
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


def rtl_anims(anims: Dict[str, List[Frame]]):
    rtl = {}
    for anim, frames in anims.items():
        rtl[anim] = [f.rtl() for f in frames]
    return rtl


def serpent():
    return {
        'idle': [
            Frame('stage/serpent1.gif', post_action='stop'),
        ],
        'bite': [
            Frame('stage/serpent1.gif'),
            Frame('stage/serpent2.gif'),
            Frame('stage/serpent3.gif'),
            Frame('stage/serpent4.gif', dx=-3 * SCALE, dy=-1 * SCALE),
            Frame('stage/serpent3.gif'),
            Frame('stage/serpent2.gif'),
            Frame('stage/serpent1.gif', post_action='stop'),
        ],
    }


def sang_decap():
    return {
        'sang_touche': [
            Frame('sprites/sang.gif', tick=11, post_action='kill'),
            Frame('empty')
        ],
        'sang': [
            # @formatter:off
            # TODO: invisible tickable sprites
            Frame('empty',              tick=5),  # noqa
            Frame('sprites/gicle1.gif', tick=10, dx=CHAR_W * SCALE, dy=0.8 * CHAR_H * SCALE),
            Frame('sprites/gicle2.gif', tick=15, dx=CHAR_W * SCALE, dy=0.8 * CHAR_H * SCALE),
            Frame('sprites/gicle3.gif', tick=20, dx=CHAR_W * SCALE, dy=0.8 * CHAR_H * SCALE),
            Frame('empty',              tick=40),
            Frame('sprites/gicle1.gif', tick=45, dx=3 * CHAR_W * SCALE, dy=(2 + 0.7) * CHAR_H * SCALE),
            Frame('sprites/gicle2.gif', tick=50, dx=3 * CHAR_W * SCALE, dy=(2 + 0.7) * CHAR_H * SCALE),
            Frame('sprites/gicle3.gif', tick=55, dx=3 * CHAR_W * SCALE, dy=(2 + 0.7) * CHAR_H * SCALE),
            Frame('empty',              tick=56, post_action='kill'),
            # @formatter:on
        ],
        'sang_rtl': [
            # @formatter:off
            Frame('empty',              tick=5),  # noqa
            Frame('sprites/gicle1.gif', tick=10, dx=0.5 * CHAR_W * SCALE, dy=0.8 * CHAR_H * SCALE),
            Frame('sprites/gicle2.gif', tick=15, dx=0.5 * CHAR_W * SCALE, dy=0.8 * CHAR_H * SCALE),
            Frame('sprites/gicle3.gif', tick=20, dx=0.5 * CHAR_W * SCALE, dy=0.8 * CHAR_H * SCALE),
            Frame('empty',              tick=40),  # noqa
            Frame('sprites/gicle1.gif', tick=45, dx=-1.75 * CHAR_W * SCALE, dy=(2 + 0.7) * CHAR_H * SCALE),
            Frame('sprites/gicle2.gif', tick=50, dx=-1.75 * CHAR_W * SCALE, dy=(2 + 0.7) * CHAR_H * SCALE),
            Frame('sprites/gicle3.gif', tick=55, dx=-1.75 * CHAR_W * SCALE, dy=(2 + 0.7) * CHAR_H * SCALE),
            Frame('empty', tick=56, post_action='kill'),
            # @formatter:om
        ]
    }


def tete_decap(subdir: str):
    return {
        'teteagauche': [
            # @formatter:off
            Frame(f'{subdir}/tetedecap1.gif', tick=4,  dx=1.2 * CHAR_W * SCALE, dy=11 * SCALE),  # noqa
            Frame(f'{subdir}/tetedecap2.gif', tick=8,  dx=  0 * CHAR_W * SCALE, dy=11 * SCALE),  # noqa
            Frame(f'{subdir}/tetedecap3.gif', tick=12, dx= -1 * CHAR_W * SCALE, dy=11 * SCALE),  # noqa
            Frame(f'{subdir}/tetedecap4.gif', tick=16, dx= -2 * CHAR_W * SCALE, dy=18 * SCALE),  # noqa
            Frame(f'{subdir}/tetedecap5.gif', tick=20, dx= -3 * CHAR_W * SCALE, dy=25 * SCALE),  # noqa
            Frame(f'{subdir}/tetedecap6.gif', tick=24, dx= -4 * CHAR_W * SCALE, dy=25 * SCALE),  # noqa
            Frame(f'{subdir}/tetedecap1.gif', tick=28, dx= -5 * CHAR_W * SCALE, dy=39 * SCALE),  # noqa
            Frame(f'{subdir}/tetedecap2.gif', tick=32, dx= -6 * CHAR_W * SCALE, dy=59 * SCALE),  # noqa snd
            Frame(f'{subdir}/tetedecap3.gif', tick=36, dx= -7 * CHAR_W * SCALE, dy=59 * SCALE),  # noqa
            Frame(f'{subdir}/tetedecap4.gif', tick=40, dx= -8 * CHAR_W * SCALE, dy=59 * SCALE),  # noqa
            Frame(f'{subdir}/tetedecap5.gif', tick=44, dx= -9 * CHAR_W * SCALE, dy=59 * SCALE),  # noqa
            Frame(f'{subdir}/tetedecap6.gif', tick=48, dx=-10 * CHAR_W * SCALE, dy=57 * SCALE),  # noqa snd
            Frame(f'{subdir}/tetedecap1.gif', tick=52, dx=-11 * CHAR_W * SCALE, dy=59 * SCALE),  # noqa
            Frame(f'{subdir}/tetedecap2.gif', tick=56, dx=-12 * CHAR_W * SCALE, dy=57 * SCALE),  # noqa
            Frame(f'{subdir}/tetedecap3.gif', tick=57, dx=-13 * CHAR_W * SCALE, dy=65 * SCALE, post_action='stop'),
            # @formatter:on
        ],
        'teteadroite': [
            # @formatter:off
            Frame(f'{subdir}/tetedecap1.gif', tick=4,  dx=1.4 * CHAR_W * SCALE, dy=11 * SCALE),  # noqa
            Frame(f'{subdir}/tetedecap2.gif', tick=8,  dx=  2 * CHAR_W * SCALE, dy=11 * SCALE),  # noqa
            Frame(f'{subdir}/tetedecap3.gif', tick=12, dx=  3 * CHAR_W * SCALE, dy=11 * SCALE),  # noqa
            Frame(f'{subdir}/tetedecap4.gif', tick=16, dx=  4 * CHAR_W * SCALE, dy=18 * SCALE),  # noqa
            Frame(f'{subdir}/tetedecap5.gif', tick=20, dx=  5 * CHAR_W * SCALE, dy=25 * SCALE),  # noqa
            Frame(f'{subdir}/tetedecap6.gif', tick=24, dx=  6 * CHAR_W * SCALE, dy=25 * SCALE),  # noqa
            Frame(f'{subdir}/tetedecap1.gif', tick=28, dx=  7 * CHAR_W * SCALE, dy=39 * SCALE),  # noqa
            Frame(f'{subdir}/tetedecap2.gif', tick=32, dx=  8 * CHAR_W * SCALE, dy=59 * SCALE),  # noqa snd
            Frame(f'{subdir}/tetedecap3.gif', tick=36, dx=  9 * CHAR_W * SCALE, dy=59 * SCALE),  # noqa
            Frame(f'{subdir}/tetedecap4.gif', tick=40, dx= 10 * CHAR_W * SCALE, dy=59 * SCALE),  # noqa
            Frame(f'{subdir}/tetedecap5.gif', tick=44, dx= 11 * CHAR_W * SCALE, dy=59 * SCALE),  # noqa
            Frame(f'{subdir}/tetedecap6.gif', tick=48, dx= 12 * CHAR_W * SCALE, dy=57 * SCALE),  # noqa snd
            Frame(f'{subdir}/tetedecap1.gif', tick=52, dx= 13 * CHAR_W * SCALE, dy=59 * SCALE),  # noqa
            Frame(f'{subdir}/tetedecap2.gif', tick=56, dx= 14 * CHAR_W * SCALE, dy=57 * SCALE),  # noqa
            Frame(f'{subdir}/tetedecap3.gif', tick=57, dx= 15 * CHAR_W * SCALE, dy=65 * SCALE, post_action='stop'),  # noqa
            # @formatter:on
        ],
        'teteagauche_rtl': [
            # @formatter:off
            Frame(f'{subdir}/tetedecap1.gif', xflip=True, tick=4,  dx=0.7 * CHAR_W * SCALE, dy=11 * SCALE),  # noqa
            Frame(f'{subdir}/tetedecap2.gif', xflip=True, tick=8,  dx=  0 * CHAR_W * SCALE, dy=11 * SCALE),  # noqa
            Frame(f'{subdir}/tetedecap3.gif', xflip=True, tick=12, dx= -1 * CHAR_W * SCALE, dy=11 * SCALE),  # noqa
            Frame(f'{subdir}/tetedecap4.gif', xflip=True, tick=16, dx= -2 * CHAR_W * SCALE, dy=18 * SCALE),  # noqa
            Frame(f'{subdir}/tetedecap5.gif', xflip=True, tick=20, dx= -3 * CHAR_W * SCALE, dy=25 * SCALE),  # noqa
            Frame(f'{subdir}/tetedecap6.gif', xflip=True, tick=24, dx= -4 * CHAR_W * SCALE, dy=25 * SCALE),  # noqa
            Frame(f'{subdir}/tetedecap1.gif', xflip=True, tick=28, dx= -5 * CHAR_W * SCALE, dy=39 * SCALE),  # noqa
            Frame(f'{subdir}/tetedecap2.gif', xflip=True, tick=32, dx= -6 * CHAR_W * SCALE, dy=59 * SCALE),  # noqa snd
            Frame(f'{subdir}/tetedecap3.gif', xflip=True, tick=36, dx= -7 * CHAR_W * SCALE, dy=59 * SCALE),  # noqa
            Frame(f'{subdir}/tetedecap4.gif', xflip=True, tick=40, dx= -8 * CHAR_W * SCALE, dy=59 * SCALE),  # noqa
            Frame(f'{subdir}/tetedecap5.gif', xflip=True, tick=44, dx= -9 * CHAR_W * SCALE, dy=59 * SCALE),  # noqa
            Frame(f'{subdir}/tetedecap6.gif', xflip=True, tick=48, dx=-10 * CHAR_W * SCALE, dy=57 * SCALE),  # noqa snd
            Frame(f'{subdir}/tetedecap1.gif', xflip=True, tick=52, dx=-11 * CHAR_W * SCALE, dy=59 * SCALE),  # noqa
            Frame(f'{subdir}/tetedecap2.gif', xflip=True, tick=56, dx=-12 * CHAR_W * SCALE, dy=57 * SCALE),  # noqa
            Frame(f'{subdir}/tetedecap3.gif', xflip=True, tick=57, dx=-13 * CHAR_W * SCALE, dy=65 * SCALE, post_action='stop'),  # noqa
            # @formatter:on
        ],
        'teteadroite_rtl': [
            # @formatter:off
            Frame(f'{subdir}/tetedecap1.gif', xflip=True, tick=4,  dx= 1 * CHAR_W * SCALE, dy=11 * SCALE),  # noqa
            Frame(f'{subdir}/tetedecap2.gif', xflip=True, tick=8,  dx= 2 * CHAR_W * SCALE, dy=11 * SCALE),  # noqa
            Frame(f'{subdir}/tetedecap3.gif', xflip=True, tick=12, dx= 3 * CHAR_W * SCALE, dy=11 * SCALE),  # noqa
            Frame(f'{subdir}/tetedecap4.gif', xflip=True, tick=16, dx= 4 * CHAR_W * SCALE, dy=18 * SCALE),  # noqa
            Frame(f'{subdir}/tetedecap5.gif', xflip=True, tick=20, dx= 5 * CHAR_W * SCALE, dy=25 * SCALE),  # noqa
            Frame(f'{subdir}/tetedecap6.gif', xflip=True, tick=24, dx= 6 * CHAR_W * SCALE, dy=25 * SCALE),  # noqa
            Frame(f'{subdir}/tetedecap1.gif', xflip=True, tick=28, dx= 7 * CHAR_W * SCALE, dy=39 * SCALE),  # noqa
            Frame(f'{subdir}/tetedecap2.gif', xflip=True, tick=32, dx= 8 * CHAR_W * SCALE, dy=59 * SCALE),  # noqa snd
            Frame(f'{subdir}/tetedecap3.gif', xflip=True, tick=36, dx= 9 * CHAR_W * SCALE, dy=59 * SCALE),  # noqa
            Frame(f'{subdir}/tetedecap4.gif', xflip=True, tick=40, dx=10 * CHAR_W * SCALE, dy=59 * SCALE),  # noqa
            Frame(f'{subdir}/tetedecap5.gif', xflip=True, tick=44, dx=11 * CHAR_W * SCALE, dy=59 * SCALE),  # noqa
            Frame(f'{subdir}/tetedecap6.gif', xflip=True, tick=48, dx=12 * CHAR_W * SCALE, dy=57 * SCALE),  # noqa snd
            Frame(f'{subdir}/tetedecap1.gif', xflip=True, tick=52, dx=13 * CHAR_W * SCALE, dy=59 * SCALE),  # noqa
            Frame(f'{subdir}/tetedecap2.gif', xflip=True, tick=56, dx=14 * CHAR_W * SCALE, dy=57 * SCALE),  # noqa
            Frame(f'{subdir}/tetedecap3.gif', xflip=True, tick=57, dx=15 * CHAR_W * SCALE, dy=65 * SCALE, post_action='stop'),  # noqa
            # @formatter:on
        ],
        'football': [
            # @formatter:off
            Frame(f'{subdir}/tetedecap3.gif', tick=  4, mv=(CHAR_W * SCALE, 0), dy=-2 * 0.6 * CHAR_H * SCALE),  # noqa
            Frame(f'{subdir}/tetedecap2.gif', tick=  7, mv=(CHAR_W * SCALE, 0), dy=-2 * 0.7 * CHAR_H * SCALE),  # noqa
            Frame(f'{subdir}/tetedecap1.gif', tick= 15, mv=(CHAR_W * SCALE, 0), dy=-2 * 0.9 * CHAR_H * SCALE),  # noqa
            Frame(f'{subdir}/tetedecap6.gif', tick= 22, mv=(CHAR_W * SCALE, 0), dy=-2 * 0.8 * CHAR_H * SCALE),  # noqa
            Frame(f'{subdir}/tetedecap5.gif', tick= 30, mv=(CHAR_W * SCALE, 0), dy=-2 * 0.4 * CHAR_H * SCALE),  # noqa
            Frame(f'{subdir}/tetedecap4.gif', tick= 37, mv=(CHAR_W * SCALE, 0), dy=-2 * 0   * CHAR_H * SCALE),  # noqa
            Frame(f'{subdir}/tetedecap3.gif', tick= 45, mv=(CHAR_W * SCALE, 0), dy=-2 * 0.1 * CHAR_H * SCALE),  # noqa snd
            Frame(f'{subdir}/tetedecap2.gif', tick= 52, mv=(CHAR_W * SCALE, 0), dy=-2 * 0.3 * CHAR_H * SCALE),  # noqa
            Frame(f'{subdir}/tetedecap1.gif', tick= 60, mv=(CHAR_W * SCALE, 0), dy=-2 * 0.5 * CHAR_H * SCALE),  # noqa
            Frame(f'{subdir}/tetedecap6.gif', tick= 67, mv=(CHAR_W * SCALE, 0), dy=-2 * 0.3 * CHAR_H * SCALE),  # noqa
            Frame(f'{subdir}/tetedecap5.gif', tick= 75, mv=(CHAR_W * SCALE, 0), dy=-2 * 0.1 * CHAR_H * SCALE),  # noqa
            Frame(f'{subdir}/tetedecap4.gif', tick= 82, mv=(CHAR_W * SCALE, 0), dy=-2 * 0   * CHAR_H * SCALE),  # noqa
            Frame(f'{subdir}/tetedecap3.gif', tick= 90, mv=(CHAR_W * SCALE, 0), dy=-2 * 0.1 * CHAR_H * SCALE),  # noqa snd
            Frame(f'{subdir}/tetedecap2.gif', tick= 97, mv=(CHAR_W * SCALE, 0), dy=-2 * 0.4 * CHAR_H * SCALE),  # noqa
            Frame(f'{subdir}/tetedecap1.gif', tick=105, mv=(CHAR_W * SCALE, 0), dy=-2 * 0.1 * CHAR_H * SCALE),  # noqa
            Frame(f'{subdir}/tetedecap3.gif', tick=112, mv=(CHAR_W * SCALE, 0), dy=-2 * 0   * CHAR_H * SCALE, post_action='stop'),  # noqa
            # @formatter:on
        ],
    }


def teteombre_decap():
    return {
        'teteagauche': [
            # @formatter:off
            Frame('spritesA/teteombre.gif', tick=4,  dx=  1 * CHAR_W * SCALE, dy=71 * SCALE),  # noqa
            Frame('spritesA/teteombre.gif', tick=8,  dx=  0 * CHAR_W * SCALE, dy=71 * SCALE),  # noqa
            Frame('spritesA/teteombre.gif', tick=12, dx= -1 * CHAR_W * SCALE, dy=71 * SCALE),  # noqa
            Frame('spritesA/teteombre.gif', tick=16, dx= -2 * CHAR_W * SCALE, dy=71 * SCALE),  # noqa
            Frame('spritesA/teteombre.gif', tick=20, dx= -3 * CHAR_W * SCALE, dy=71 * SCALE),  # noqa
            Frame('spritesA/teteombre.gif', tick=24, dx= -4 * CHAR_W * SCALE, dy=71 * SCALE),  # noqa
            Frame('spritesA/teteombre.gif', tick=28, dx= -5 * CHAR_W * SCALE, dy=71 * SCALE),  # noqa
            Frame('spritesA/teteombre.gif', tick=32, dx= -6 * CHAR_W * SCALE, dy=71 * SCALE),  # noqa snd
            Frame('spritesA/teteombre.gif', tick=36, dx= -7 * CHAR_W * SCALE, dy=71 * SCALE),  # noqa
            Frame('spritesA/teteombre.gif', tick=40, dx= -8 * CHAR_W * SCALE, dy=71 * SCALE),  # noqa
            Frame('spritesA/teteombre.gif', tick=44, dx= -9 * CHAR_W * SCALE, dy=71 * SCALE),  # noqa
            Frame('spritesA/teteombre.gif', tick=48, dx=-10 * CHAR_W * SCALE, dy=71 * SCALE),  # noqa snd
            Frame('spritesA/teteombre.gif', tick=52, dx=-11 * CHAR_W * SCALE, dy=71 * SCALE),  # noqa
            Frame('spritesA/teteombre.gif', tick=56, dx=-12 * CHAR_W * SCALE, dy=71 * SCALE),  # noqa
            Frame('spritesA/teteombre.gif', tick=57, dx=-13 * CHAR_W * SCALE, dy=71 * SCALE, post_action='stop'),
            # @formatter:on
        ],
        'teteadroite': [
            # @formatter:off
            Frame('spritesA/teteombre.gif', tick=4,  dx=1.4 * CHAR_W * SCALE, dy=71 * SCALE),  # noqa
            Frame('spritesA/teteombre.gif', tick=8,  dx=  2 * CHAR_W * SCALE, dy=71 * SCALE),  # noqa
            Frame('spritesA/teteombre.gif', tick=12, dx=  3 * CHAR_W * SCALE, dy=71 * SCALE),  # noqa
            Frame('spritesA/teteombre.gif', tick=16, dx=  4 * CHAR_W * SCALE, dy=71 * SCALE),  # noqa
            Frame('spritesA/teteombre.gif', tick=20, dx=  5 * CHAR_W * SCALE, dy=71 * SCALE),  # noqa
            Frame('spritesA/teteombre.gif', tick=24, dx=  6 * CHAR_W * SCALE, dy=71 * SCALE),  # noqa
            Frame('spritesA/teteombre.gif', tick=28, dx=  7 * CHAR_W * SCALE, dy=71 * SCALE),  # noqa
            Frame('spritesA/teteombre.gif', tick=32, dx=  8 * CHAR_W * SCALE, dy=71 * SCALE),  # noqa snd
            Frame('spritesA/teteombre.gif', tick=36, dx=  9 * CHAR_W * SCALE, dy=71 * SCALE),  # noqa
            Frame('spritesA/teteombre.gif', tick=40, dx= 10 * CHAR_W * SCALE, dy=71 * SCALE),  # noqa
            Frame('spritesA/teteombre.gif', tick=44, dx= 11 * CHAR_W * SCALE, dy=71 * SCALE),  # noqa
            Frame('spritesA/teteombre.gif', tick=48, dx= 12 * CHAR_W * SCALE, dy=71 * SCALE),  # noqa snd
            Frame('spritesA/teteombre.gif', tick=52, dx= 13 * CHAR_W * SCALE, dy=71 * SCALE),  # noqa
            Frame('spritesA/teteombre.gif', tick=56, dx= 14 * CHAR_W * SCALE, dy=71 * SCALE),  # noqa
            Frame('spritesA/teteombre.gif', tick=57, dx= 15 * CHAR_W * SCALE, dy=71 * SCALE, post_action='stop'),  # noqa
            # @formatter:on
        ],
        'football': [
            # @formatter:off
            Frame(f'spritesA/teteombre.gif', tick=4,   mv=(CHAR_W * SCALE, 0)),  # noqa
            Frame(f'spritesA/teteombre.gif', tick=7,   mv=(CHAR_W * SCALE, 0)),  # noqa
            Frame(f'spritesA/teteombre.gif', tick=15,  mv=(CHAR_W * SCALE, 0)),  # noqa
            Frame(f'spritesA/teteombre.gif', tick=22,  mv=(CHAR_W * SCALE, 0)),  # noqa
            Frame(f'spritesA/teteombre.gif', tick=30,  mv=(CHAR_W * SCALE, 0)),  # noqa
            Frame(f'spritesA/teteombre.gif', tick=37,  mv=(CHAR_W * SCALE, 0)),  # noqa
            Frame(f'spritesA/teteombre.gif', tick=45,  mv=(CHAR_W * SCALE, 0)),  # noqa snd
            Frame(f'spritesA/teteombre.gif', tick=52,  mv=(CHAR_W * SCALE, 0)),  # noqa
            Frame(f'spritesA/teteombre.gif', tick=60,  mv=(CHAR_W * SCALE, 0)),  # noqa
            Frame(f'spritesA/teteombre.gif', tick=67,  mv=(CHAR_W * SCALE, 0)),  # noqa
            Frame(f'spritesA/teteombre.gif', tick=75,  mv=(CHAR_W * SCALE, 0)),  # noqa
            Frame(f'spritesA/teteombre.gif', tick=82,  mv=(CHAR_W * SCALE, 0)),  # noqa
            Frame(f'spritesA/teteombre.gif', tick=90,  mv=(CHAR_W * SCALE, 0)),  # noqa snd
            Frame(f'spritesA/teteombre.gif', tick=97,  mv=(CHAR_W * SCALE, 0)),  # noqa
            Frame(f'spritesA/teteombre.gif', tick=105, mv=(CHAR_W * SCALE, 0)),  # noqa
            Frame(f'spritesA/teteombre.gif', tick=112, mv=(CHAR_W * SCALE, 0), post_action='stop'),  # noqa
            # @formatter:on
        ],
    }


def vie():
    return {
        'vie': [
            # @formatter:off
            Frame('fill', w=1,            h=1.2 * CHAR_H, fill=(0, 0, 0), dx=0, post_action='stop'),  # noqa
            Frame('fill', w=0.7 * CHAR_W, h=1.2 * CHAR_H, fill=(0, 0, 0), dx=-0.7 * CHAR_W * SCALE),  # noqa
            Frame('fill', w=2   * CHAR_W, h=1.2 * CHAR_H, fill=(0, 0, 0), dx=-2   * CHAR_W * SCALE),  # noqa
            Frame('fill', w=2.7 * CHAR_W, h=1.2 * CHAR_H, fill=(0, 0, 0), dx=-2.7 * CHAR_W * SCALE),  # noqa
            Frame('fill', w=4   * CHAR_W, h=1.2 * CHAR_H, fill=(0, 0, 0), dx=-4   * CHAR_W * SCALE),  # noqa
            Frame('fill', w=4.7 * CHAR_W, h=1.2 * CHAR_H, fill=(0, 0, 0), dx=-4.7 * CHAR_W * SCALE),  # noqa
            Frame('fill', w=6   * CHAR_W, h=1.2 * CHAR_H, fill=(0, 0, 0), dx=-6   * CHAR_W * SCALE),  # noqa
            # @formatter:on
        ],
        'vie_rtl': [
            # @formatter:off
            Frame('fill', w=1,            h=1.2 * CHAR_H, fill=(0, 0, 0), post_action='stop'),  # noqa
            Frame('fill', w=0.8 * CHAR_W, h=1.2 * CHAR_H, fill=(0, 0, 0)),  # noqa
            Frame('fill', w=2   * CHAR_W, h=1.2 * CHAR_H, fill=(0, 0, 0)),  # noqa
            Frame('fill', w=2.8 * CHAR_W, h=1.2 * CHAR_H, fill=(0, 0, 0)),  # noqa
            Frame('fill', w=4   * CHAR_W, h=1.2 * CHAR_H, fill=(0, 0, 0)),  # noqa
            Frame('fill', w=4.8 * CHAR_W, h=1.2 * CHAR_H, fill=(0, 0, 0)),  # noqa
            Frame('fill', w=6   * CHAR_W, h=1.2 * CHAR_H, fill=(0, 0, 0)),  # noqa
            # @formatter:on
        ],
    }


def barb(subdir: str):
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
            Frame(f'{subdir}/roulade1.gif',             tick=10, mv=(CHAR_W * SCALE, 0)),  # noqa
            Frame(f'{subdir}/roulade2.gif',             tick=13, mv=(CHAR_W * SCALE, 0)),  # noqa
            Frame(f'{subdir}/roulade3.gif',             tick=16, mv=(CHAR_W * SCALE, 0)),  # noqa
            Frame(f'{subdir}/roulade3.gif',             tick=19, mv=(CHAR_W * SCALE, 0)),  # noqa
            Frame(f'{subdir}/roulade2.gif', xflip=True, tick=22, mv=(CHAR_W * SCALE, 0)),  # noqa
            Frame(f'{subdir}/roulade2.gif', xflip=True, tick=25, mv=(CHAR_W * SCALE, 0)),  # noqa
            Frame(f'{subdir}/roulade5.gif',             tick=28, mv=(CHAR_W * SCALE, 0)),  # noqa
            Frame(f'{subdir}/roulade5.gif',             tick=30, mv=(CHAR_W * SCALE, 0)),  # noqa
            Frame(f'{subdir}/roulade1.gif', xflip=True, tick=34, mv=(CHAR_W * SCALE, 0)),  # noqa
            Frame(f'{subdir}/debout.gif',               tick=39,                       ),  # noqa
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
            Frame(f'{subdir}/protegeH.gif', tick=5, dx=-2 * SCALE),
            Frame(f'{subdir}/protegeD.gif', tick=9, dx=-2 * SCALE),
        ],
        'cou': [
            # @formatter:off
            Frame(f'{subdir}/protegeH.gif', tick=15, dx=-2 * SCALE),
            Frame(f'{subdir}/cou2.gif',     tick=30, dx=-4 * SCALE),
            Frame(f'{subdir}/cou3.gif',     tick=46, dx=-1 * SCALE),
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
            Frame(f'{subdir}/pied1.gif',  tick=9),
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
            Frame(f'{subdir}/front1.gif', tick=5, dx=-1 * SCALE),
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
            Frame(f'{subdir}/vainqueur1.gif', xflip=True, tick=101, post_action='stop'),
        ],
        'vainqueurKO': [
            # @formatter:off
            Frame(f'{subdir}/retourne1.gif',              tick=15),  # noqa
            Frame(f'{subdir}/retourne2.gif',              tick=23),  # noqa
            Frame(f'{subdir}/retourne3.gif',              tick=30),  # noqa
            Frame(f'{subdir}/debout.gif',                 tick=40),  # noqa
            Frame(f'{subdir}/marche3.gif',                tick=40),  # noqa optional frame, see gestion on tick 35
            Frame(f'{subdir}/marche3.gif',    xflip=True, tick=40),  # noqa optional frame, see gestion on tick 35
            Frame(f'{subdir}/debout.gif',                 tick=55),  # noqa
            Frame(f'{subdir}/pied1.gif',                  tick=70),  # noqa
            Frame(f'{subdir}/pied2.gif',                  tick=75),  # noqa
            Frame(f'{subdir}/pied1.gif',                  tick=100),  # noqa
            Frame(f'{subdir}/debout.gif',                 tick=105),  # noqa
            Frame(f'{subdir}/vainqueur1.gif', xflip=True, tick=123),  # noqa
            Frame(f'{subdir}/vainqueur2.gif', xflip=True, tick=140),  # noqa
            Frame(f'{subdir}/vainqueur3.gif', xflip=True, tick=195),  # noqa
            Frame(f'{subdir}/vainqueur2.gif', xflip=True, tick=205),  # noqa
            Frame(f'{subdir}/vainqueur1.gif', xflip=True, tick=231, post_action='stop'),  # noqa
            # @formatter:on
        ],
        'touche1': [
            # @formatter:off
            Frame(f'{subdir}/touche2.gif', tick=1),
            Frame(f'{subdir}/touche2.gif', tick=5,  mv=(-CHAR_W * SCALE,     0)),  # noqa
            Frame(f'{subdir}/touche1.gif', tick=10, mv=(-2 * CHAR_W * SCALE, 0)),  # noqa
            Frame(f'{subdir}/touche2.gif', tick=20, mv=(-CHAR_W * SCALE,     0)),  # noqa
            Frame(f'{subdir}/debout.gif',  tick=21),
            # @formatter:on
        ],
        'tombe1': [
            # @formatter:off
            Frame(f'{subdir}/tombe1.gif', tick=1,                           dx=-2 * CHAR_W * SCALE),  # noqa
            Frame(f'{subdir}/tombe1.gif', tick=9,  mv=(-CHAR_W * SCALE, 0), dx=-2 * CHAR_W * SCALE),  # noqa
            Frame(f'{subdir}/tombe2.gif', tick=15, mv=(-CHAR_W * SCALE, 0), dx=-3 * CHAR_W * SCALE),  # noqa
            Frame(f'{subdir}/tombe3.gif', tick=25,                          dx=-3 * CHAR_W * SCALE),  # noqa
            Frame(f'{subdir}/debout.gif', tick=27, mv=(-CHAR_W * SCALE, 0)),
            # @formatter:on
        ],
        'mort': [
            # @formatter:off
            Frame(f'{subdir}/assis1.gif', tick=15),
            Frame(f'{subdir}/mort2.gif',  tick=17, post_action='stop'),
            Frame(f'{subdir}/mort3.gif',  tick=18, dx=-1 * CHAR_W * SCALE),  # manual, see vainqueurKO
            Frame(f'{subdir}/mort4.gif',  tick=19, dx=-3 * CHAR_W * SCALE),  # manual, see vainqueurKO
            # @formatter:on
        ],
        'mortdecap': [
            # @formatter:off
            Frame(f'{subdir}/decap1.gif', tick=35),
            Frame(f'{subdir}/decap2.gif', tick=70, dx=2 * CHAR_W * SCALE),
            Frame(f'{subdir}/decap3.gif', tick=80, dx=2 * CHAR_W * SCALE),
            Frame(f'{subdir}/decap4.gif', tick=82, dx=2 * CHAR_W * SCALE, post_action='stop'),
            # @formatter:on
        ],
        'mortgnome': [
            Frame(f'{subdir}/mort4.gif', tick=1, mv=((CHAR_W / 12) * SCALE, 0)),
        ],
        'mortdecapgnome': [
            Frame(f'{subdir}/decap4.gif', tick=1, mv=((CHAR_W / 12) * SCALE, 0)),
        ],
    }


def barb_rtl(subdir: str):
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
            Frame(f'{subdir}/roulade1.gif', xflip=True, tick=10, mv=(-CHAR_W * SCALE, 0)),  # noqa
            Frame(f'{subdir}/roulade2.gif', xflip=True, tick=13, mv=(-CHAR_W * SCALE, 0)),  # noqa
            Frame(f'{subdir}/roulade3.gif',             tick=16, mv=(-CHAR_W * SCALE, 0)),  # noqa
            Frame(f'{subdir}/roulade3.gif',             tick=19, mv=(-CHAR_W * SCALE, 0)),  # noqa
            Frame(f'{subdir}/roulade2.gif',             tick=22, mv=(-CHAR_W * SCALE, 0)),  # noqa
            Frame(f'{subdir}/roulade2.gif',             tick=25, mv=(-CHAR_W * SCALE, 0)),  # noqa
            Frame(f'{subdir}/roulade5.gif',             tick=28, mv=(-CHAR_W * SCALE, 0)),  # noqa
            Frame(f'{subdir}/roulade5.gif',             tick=30, mv=(-CHAR_W * SCALE, 0)),  # noqa
            Frame(f'{subdir}/roulade1.gif',             tick=34, mv=(-CHAR_W * SCALE, 0)),  # noqa
            Frame(f'{subdir}/debout.gif',   xflip=True, tick=39,                        ),  # noqa
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
            Frame(f'{subdir}/protegeH.gif', xflip=True, tick=5, dx=(-CHAR_W + 2) * SCALE),
            Frame(f'{subdir}/protegeD.gif', xflip=True, tick=9, dx=(-CHAR_W + 2) * SCALE),
        ],
        'cou': [
            # @formatter:off
            Frame(f'{subdir}/protegeH.gif', xflip=True, tick=15, dx=(-CHAR_W + 2) * SCALE    ),  # noqa
            Frame(f'{subdir}/cou2.gif',     xflip=True, tick=30, dx=(-CHAR_W + 4) * SCALE    ),  # noqa
            Frame(f'{subdir}/cou3.gif',     xflip=True, tick=46, dx=(-4 * CHAR_W + 1) * SCALE),  # noqa
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
            Frame(f'{subdir}/pied1.gif',  xflip=True, tick=9,  dx=-CHAR_W * SCALE),
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
            Frame(f'{subdir}/front1.gif', xflip=True, tick=5,  dx=(-CHAR_W + 1) * SCALE),  # noqa
            Frame(f'{subdir}/front2.gif', xflip=True, tick=23, dx=-CHAR_W * SCALE      ),  # noqa
            Frame(f'{subdir}/front3.gif', xflip=True, tick=30, dx=-3 * CHAR_W * SCALE  ),  # noqa
            Frame(f'{subdir}/front2.gif', xflip=True, tick=46, dx=-CHAR_W * SCALE      ),  # noqa
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
            Frame(f'{subdir}/vainqueur1.gif', xflip=True, tick=101, dx=-CHAR_W * SCALE, post_action='stop'),
            # @formatter:on
        ],
        'vainqueurKO': [
            # @formatter:off
            Frame(f'{subdir}/retourne1.gif',  xflip=True, tick=15),  # noqa
            Frame(f'{subdir}/retourne2.gif',  xflip=True, tick=23),  # noqa
            Frame(f'{subdir}/retourne3.gif',  xflip=True, tick=30),  # noqa
            Frame(f'{subdir}/debout.gif',     xflip=True, tick=40),  # noqa
            Frame(f'{subdir}/marche3.gif',                tick=40),  # noqa optional frame, see gestion on tick 35
            Frame(f'{subdir}/marche3.gif',    xflip=True, tick=40),  # noqa optional frame, see gestion on tick 35
            Frame(f'{subdir}/debout.gif',     xflip=True, tick=55),  # noqa
            Frame(f'{subdir}/pied1.gif',      xflip=True, tick=70,  dx=-CHAR_W * SCALE),  # noqa
            Frame(f'{subdir}/pied2.gif',      xflip=True, tick=75,  dx=-CHAR_W * SCALE),  # noqa
            Frame(f'{subdir}/pied1.gif',      xflip=True, tick=100, dx=-CHAR_W * SCALE),  # noqa
            Frame(f'{subdir}/debout.gif',     xflip=True, tick=105),  # noqa
            Frame(f'{subdir}/vainqueur1.gif', xflip=True, tick=123, dx=-CHAR_W * SCALE),  # noqa
            Frame(f'{subdir}/vainqueur2.gif', xflip=True, tick=140, dx=-CHAR_W * SCALE),  # noqa
            Frame(f'{subdir}/vainqueur3.gif', xflip=True, tick=195, dx=-CHAR_W * SCALE),  # noqa
            Frame(f'{subdir}/vainqueur2.gif', xflip=True, tick=205, dx=-CHAR_W * SCALE),  # noqa
            Frame(f'{subdir}/vainqueur1.gif', xflip=True, tick=231, dx=-CHAR_W * SCALE, post_action='stop'),
            # @formatter:oon
        ],
        'touche1': [
            # @formatter:off
            Frame(f'{subdir}/touche2.gif', xflip=True, tick=1),
            Frame(f'{subdir}/touche2.gif', xflip=True, tick=5,  mv=(CHAR_W * SCALE,     0)),  # noqa
            Frame(f'{subdir}/touche1.gif', xflip=True, tick=10, mv=(2 * CHAR_W * SCALE, 0)),  # noqa
            Frame(f'{subdir}/touche2.gif', xflip=True, tick=20, mv=(CHAR_W * SCALE,     0)),  # noqa
            Frame(f'{subdir}/debout.gif',  xflip=True, tick=21),
            # @formatter:on
        ],
        'tombe1': [
            # @formatter:off
            Frame(f'{subdir}/tombe1.gif', xflip=True, tick=1,                          dx=CHAR_W * SCALE),  # noqa
            Frame(f'{subdir}/tombe1.gif', xflip=True, tick=9,  mv=(CHAR_W * SCALE, 0), dx=CHAR_W * SCALE),  # noqa
            Frame(f'{subdir}/tombe2.gif', xflip=True, tick=15, mv=(CHAR_W * SCALE, 0), dx=CHAR_W * SCALE),  # noqa
            Frame(f'{subdir}/tombe3.gif', xflip=True, tick=25,                         dx=CHAR_W * SCALE),  # noqa
            Frame(f'{subdir}/debout.gif', xflip=True, tick=27, mv=(CHAR_W * SCALE, 0)),
            # @formatter:on
        ],
        'mort': [
            # @formatter:off
            Frame(f'{subdir}/assis1.gif', xflip=True, tick=15),
            Frame(f'{subdir}/mort2.gif',  xflip=True, tick=17, dx=-1 * CHAR_W * SCALE, post_action='stop'),
            Frame(f'{subdir}/mort3.gif',  xflip=True, tick=18),  # manual, see vainqueurKO
            Frame(f'{subdir}/mort4.gif',  xflip=True, tick=19),  # manual, see vainqueurKO
            # @formatter:on
        ],
        'mortdecap': [
            # @formatter:off
            Frame(f'{subdir}/decap1.gif', xflip=True, tick=35, dx=-1 * CHAR_W * SCALE),
            Frame(f'{subdir}/decap2.gif', xflip=True, tick=70, dx=-3 * CHAR_W * SCALE),
            Frame(f'{subdir}/decap3.gif', xflip=True, tick=80, dx=-4 * CHAR_W * SCALE),
            Frame(f'{subdir}/decap4.gif', xflip=True, tick=82, dx=-5 * CHAR_W * SCALE, post_action='stop'),
            # @formatter:on
        ],
        'mortgnome': [
            Frame(f'{subdir}/mort4.gif', xflip=True, tick=1, mv=((CHAR_W / 12) * SCALE, 0)),
        ],
        'mortdecapgnome': [
            Frame(f'{subdir}/decap4.gif', xflip=True, tick=1, mv=((CHAR_W / 12) * SCALE, 0)),
        ],
    }


def gnome():
    return {
        'gnome': [
            Frame('sprites/gnome1.gif', tick=6, mv=(CHAR_W * SCALE, 0)),
            Frame('sprites/gnome2.gif', tick=12),
            Frame('sprites/gnome3.gif', tick=18, mv=(CHAR_W * SCALE, 0)),
            Frame('sprites/gnome4.gif', tick=24),
        ],
    }


def sorcier():
    return {
        'debout': [
            Frame('sprites/drax1.gif'),
        ],
        'attaque': [
            Frame('sprites/drax2.gif'),
        ],
    }
