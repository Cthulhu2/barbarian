from dataclasses import dataclass, field
from os.path import join
from typing import Dict, List, Callable, Tuple

from pygame import Surface, image, Rect, Sound, Color
from pygame.transform import scale, rotate, flip

from barbariantuw import OPTS
from barbariantuw.settings import IMG_PATH, SCALE_X, SCALE_Y, CHAR_W, CHAR_H, SND_PATH

img_cache: Dict[int, Surface] = {}


def get_img(name, w=0, h=0, angle: float = 0, xflip=False,
            fill=None, blend_flags=0, color=None) -> Surface:
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
        img = scale(img, (w * SCALE_X, h * SCALE_Y))
    else:
        img = scale(img, (img.get_width() * SCALE_X, img.get_height() * SCALE_Y))
    if angle != 0:
        img = rotate(img, angle)
    if xflip:
        img = flip(img, xflip, False)
    img_cache[key_] = img
    return img


snd_cache: Dict[int, Sound] = {}


def get_snd(name: str) -> Sound:
    key_ = hash(name)

    if key_ in snd_cache:
        return snd_cache[key_]

    snd = Sound(join(SND_PATH, name))
    snd_cache[key_] = snd
    return snd


def snd_play(name: str):
    if name and OPTS.sound:
        get_snd(name).play()


Action = Callable[['AnimatedSprite'], None]


@dataclass(slots=True, frozen=True)
class Frame:
    """
    `tick` end tick. A next tick will apply a next frame.
    """
    name: str
    dx: float = 0
    dy: float = 0
    w: int = 0
    h: int = 0
    duration: int = 125
    angle: float = 0
    xflip: bool = False
    fill: Color = None  # import pygame.typing.ColorLike breaks WASM!!!
    blend_flags: int = 0
    mv: Tuple[float, float] = None
    pre_action: Action = None
    post_action: Action = None
    tick: int = -1
    colorkey: Color = None
    is_tickable: bool = field(init=False, compare=False)
    image: Surface = field(init=False, compare=False)
    rect: Rect = field(init=False, compare=False)

    def __post_init__(self):
        super(Frame, self).__setattr__('is_tickable', self.tick >= 0)
        super(Frame, self).__setattr__(
            'image', get_img(self.name, self.w, self.h, self.angle, self.xflip,
                             self.fill, self.blend_flags, self.colorkey))
        super(Frame, self).__setattr__(
            'rect', self.image.get_rect().move(self.dx, self.dy))

    def rtl(self):
        move_base = None
        if self.mv:
            move_base = (-self.mv[0], self.mv[1])

        return Frame(self.name, -self.dx, self.dy, self.w, self.h,
                     self.duration, -self.angle, not self.xflip, self.fill,
                     self.blend_flags, move_base,
                     self.pre_action, self.post_action)


@dataclass(slots=True, frozen=True)
class Act:
    act: Action
    tick: int = -1


@dataclass(slots=True, frozen=True)
class Animation:
    frames: List[Frame]
    actions: List[Act] = None


class Actions:
    snd_acts = {}

    @staticmethod
    def kill(sprite):
        sprite.kill()

    @staticmethod
    def stop(sprite):
        sprite.stopped = True

    @staticmethod
    def snd(snd: str):
        if snd in Actions.snd_acts:
            return Actions.snd_acts[snd]

        # noinspection PyUnusedLocal
        def act(sprite):
            snd_play(snd)

        Actions.snd_acts[snd] = act
        return act


def rtl_anims(animations: Dict[str, Animation]):
    rtl = {}
    for name, anim in animations.items():
        rtl[name] = Animation(frames=[f.rtl() for f in anim.frames],
                              actions=anim.actions)
    return rtl


def serpent():
    return {
        'idle': Animation(frames=[
            Frame('stage/serpent1.gif', post_action=Actions.stop),
        ]),
        'bite': Animation(frames=[
            Frame('stage/serpent1.gif'),
            Frame('stage/serpent2.gif'),
            Frame('stage/serpent3.gif'),
            Frame('stage/serpent4.gif', dx=-3 * SCALE_X, dy=-1 * SCALE_Y),
            Frame('stage/serpent3.gif'),
            Frame('stage/serpent2.gif'),
            Frame('stage/serpent1.gif', post_action=Actions.stop),
        ]),
    }


def sang_decap():
    return {
        'sang_touche': Animation(frames=[
            Frame('sprites/sang.gif', tick=11, post_action=Actions.kill),
            Frame('empty')
        ]),
        'sang': Animation(frames=[
            # @formatter:off
            # TODO: invisible tickable sprites
            Frame('empty',              tick=5),  # noqa
            Frame('sprites/gicle1.gif', tick=10, dx=CHAR_W, dy=0.8 * CHAR_H),
            Frame('sprites/gicle2.gif', tick=15, dx=CHAR_W, dy=0.8 * CHAR_H),
            Frame('sprites/gicle3.gif', tick=20, dx=CHAR_W, dy=0.8 * CHAR_H),
            Frame('empty',              tick=40),
            Frame('sprites/gicle1.gif', tick=45, dx=3 * CHAR_W, dy=(2 + 0.7) * CHAR_H),
            Frame('sprites/gicle2.gif', tick=50, dx=3 * CHAR_W, dy=(2 + 0.7) * CHAR_H),
            Frame('sprites/gicle3.gif', tick=55, dx=3 * CHAR_W, dy=(2 + 0.7) * CHAR_H),
            Frame('empty',              tick=56, post_action=Actions.kill),
            # @formatter:on
        ]),
        'sang_rtl': Animation(frames=[
            # @formatter:off
            Frame('empty',              tick=5),  # noqa
            Frame('sprites/gicle1.gif', tick=10, dx=0.5 * CHAR_W, dy=0.8 * CHAR_H),
            Frame('sprites/gicle2.gif', tick=15, dx=0.5 * CHAR_W, dy=0.8 * CHAR_H),
            Frame('sprites/gicle3.gif', tick=20, dx=0.5 * CHAR_W, dy=0.8 * CHAR_H),
            Frame('empty',              tick=40),  # noqa
            Frame('sprites/gicle1.gif', tick=45, dx=-1.75 * CHAR_W, dy=(2 + 0.7) * CHAR_H),
            Frame('sprites/gicle2.gif', tick=50, dx=-1.75 * CHAR_W, dy=(2 + 0.7) * CHAR_H),
            Frame('sprites/gicle3.gif', tick=55, dx=-1.75 * CHAR_W, dy=(2 + 0.7) * CHAR_H),
            Frame('empty', tick=56, post_action=Actions.kill),
            # @formatter:om
        ])
    }


def tete_decap(subdir: str):
    return {
        'teteagauche': Animation(frames=[
            # @formatter:off
            Frame(f'{subdir}/tetedecap1.gif', tick=4,  dx=1.2 * CHAR_W, dy=11 * SCALE_Y),  # noqa
            Frame(f'{subdir}/tetedecap2.gif', tick=8,  dx=  0 * CHAR_W, dy=11 * SCALE_Y),  # noqa
            Frame(f'{subdir}/tetedecap3.gif', tick=12, dx= -1 * CHAR_W, dy=11 * SCALE_Y),  # noqa
            Frame(f'{subdir}/tetedecap4.gif', tick=16, dx= -2 * CHAR_W, dy=18 * SCALE_Y),  # noqa
            Frame(f'{subdir}/tetedecap5.gif', tick=20, dx= -3 * CHAR_W, dy=25 * SCALE_Y),  # noqa
            Frame(f'{subdir}/tetedecap6.gif', tick=24, dx= -4 * CHAR_W, dy=25 * SCALE_Y),  # noqa
            Frame(f'{subdir}/tetedecap1.gif', tick=28, dx= -5 * CHAR_W, dy=39 * SCALE_Y),  # noqa
            Frame(f'{subdir}/tetedecap2.gif', tick=32, dx= -6 * CHAR_W, dy=59 * SCALE_Y),  # noqa
            Frame(f'{subdir}/tetedecap3.gif', tick=36, dx= -7 * CHAR_W, dy=59 * SCALE_Y),  # noqa
            Frame(f'{subdir}/tetedecap4.gif', tick=40, dx= -8 * CHAR_W, dy=59 * SCALE_Y),  # noqa
            Frame(f'{subdir}/tetedecap5.gif', tick=44, dx= -9 * CHAR_W, dy=59 * SCALE_Y),  # noqa
            Frame(f'{subdir}/tetedecap6.gif', tick=48, dx=-10 * CHAR_W, dy=57 * SCALE_Y),  # noqa
            Frame(f'{subdir}/tetedecap1.gif', tick=52, dx=-11 * CHAR_W, dy=59 * SCALE_Y),  # noqa
            Frame(f'{subdir}/tetedecap2.gif', tick=56, dx=-12 * CHAR_W, dy=57 * SCALE_Y),  # noqa
            Frame(f'{subdir}/tetedecap3.gif', tick=57, dx=-13 * CHAR_W, dy=65 * SCALE_Y),
            # @formatter:on
        ], actions=[
            Act(tick=29, act=Actions.snd('tete.ogg')),
            Act(tick=45, act=Actions.snd('tete.ogg')),
            Act(tick=58, act=Actions.stop),
        ]),
        'teteadroite': Animation(frames=[
            # @formatter:off
            Frame(f'{subdir}/tetedecap1.gif', tick=4,  dx=1.4 * CHAR_W, dy=11 * SCALE_Y),  # noqa
            Frame(f'{subdir}/tetedecap2.gif', tick=8,  dx=  2 * CHAR_W, dy=11 * SCALE_Y),  # noqa
            Frame(f'{subdir}/tetedecap3.gif', tick=12, dx=  3 * CHAR_W, dy=11 * SCALE_Y),  # noqa
            Frame(f'{subdir}/tetedecap4.gif', tick=16, dx=  4 * CHAR_W, dy=18 * SCALE_Y),  # noqa
            Frame(f'{subdir}/tetedecap5.gif', tick=20, dx=  5 * CHAR_W, dy=25 * SCALE_Y),  # noqa
            Frame(f'{subdir}/tetedecap6.gif', tick=24, dx=  6 * CHAR_W, dy=25 * SCALE_Y),  # noqa
            Frame(f'{subdir}/tetedecap1.gif', tick=28, dx=  7 * CHAR_W, dy=39 * SCALE_Y),  # noqa
            Frame(f'{subdir}/tetedecap2.gif', tick=32, dx=  8 * CHAR_W, dy=59 * SCALE_Y),  # noqa
            Frame(f'{subdir}/tetedecap3.gif', tick=36, dx=  9 * CHAR_W, dy=59 * SCALE_Y),  # noqa
            Frame(f'{subdir}/tetedecap4.gif', tick=40, dx= 10 * CHAR_W, dy=59 * SCALE_Y),  # noqa
            Frame(f'{subdir}/tetedecap5.gif', tick=44, dx= 11 * CHAR_W, dy=59 * SCALE_Y),  # noqa
            Frame(f'{subdir}/tetedecap6.gif', tick=48, dx= 12 * CHAR_W, dy=57 * SCALE_Y),  # noqa
            Frame(f'{subdir}/tetedecap1.gif', tick=52, dx= 13 * CHAR_W, dy=59 * SCALE_Y),  # noqa
            Frame(f'{subdir}/tetedecap2.gif', tick=56, dx= 14 * CHAR_W, dy=57 * SCALE_Y),  # noqa
            Frame(f'{subdir}/tetedecap3.gif', tick=57, dx= 15 * CHAR_W, dy=65 * SCALE_Y),  # noqa
            # @formatter:on
        ], actions=[
            Act(tick=29, act=Actions.snd('tete.ogg')),
            Act(tick=45, act=Actions.snd('tete.ogg')),
            Act(tick=58, act=Actions.stop),
        ]),
        'teteagauche_rtl': Animation(frames=[
            # @formatter:off
            Frame(f'{subdir}/tetedecap1.gif', xflip=True, tick=4,  dx=0.7 * CHAR_W, dy=11 * SCALE_Y),  # noqa
            Frame(f'{subdir}/tetedecap2.gif', xflip=True, tick=8,  dx=  0 * CHAR_W, dy=11 * SCALE_Y),  # noqa
            Frame(f'{subdir}/tetedecap3.gif', xflip=True, tick=12, dx= -1 * CHAR_W, dy=11 * SCALE_Y),  # noqa
            Frame(f'{subdir}/tetedecap4.gif', xflip=True, tick=16, dx= -2 * CHAR_W, dy=18 * SCALE_Y),  # noqa
            Frame(f'{subdir}/tetedecap5.gif', xflip=True, tick=20, dx= -3 * CHAR_W, dy=25 * SCALE_Y),  # noqa
            Frame(f'{subdir}/tetedecap6.gif', xflip=True, tick=24, dx= -4 * CHAR_W, dy=25 * SCALE_Y),  # noqa
            Frame(f'{subdir}/tetedecap1.gif', xflip=True, tick=28, dx= -5 * CHAR_W, dy=39 * SCALE_Y),  # noqa
            Frame(f'{subdir}/tetedecap2.gif', xflip=True, tick=32, dx= -6 * CHAR_W, dy=59 * SCALE_Y),  # noqa
            Frame(f'{subdir}/tetedecap3.gif', xflip=True, tick=36, dx= -7 * CHAR_W, dy=59 * SCALE_Y),  # noqa
            Frame(f'{subdir}/tetedecap4.gif', xflip=True, tick=40, dx= -8 * CHAR_W, dy=59 * SCALE_Y),  # noqa
            Frame(f'{subdir}/tetedecap5.gif', xflip=True, tick=44, dx= -9 * CHAR_W, dy=59 * SCALE_Y),  # noqa
            Frame(f'{subdir}/tetedecap6.gif', xflip=True, tick=48, dx=-10 * CHAR_W, dy=57 * SCALE_Y),  # noqa
            Frame(f'{subdir}/tetedecap1.gif', xflip=True, tick=52, dx=-11 * CHAR_W, dy=59 * SCALE_Y),  # noqa
            Frame(f'{subdir}/tetedecap2.gif', xflip=True, tick=56, dx=-12 * CHAR_W, dy=57 * SCALE_Y),  # noqa
            Frame(f'{subdir}/tetedecap3.gif', xflip=True, tick=57, dx=-13 * CHAR_W, dy=65 * SCALE_Y),  # noqa
            # @formatter:on
        ], actions=[
            Act(tick=29, act=Actions.snd('tete.ogg')),
            Act(tick=45, act=Actions.snd('tete.ogg')),
            Act(tick=58, act=Actions.stop),
        ]),
        'teteadroite_rtl': Animation(frames=[
            # @formatter:off
            Frame(f'{subdir}/tetedecap1.gif', xflip=True, tick=4,  dx= 1 * CHAR_W, dy=11 * SCALE_Y),  # noqa
            Frame(f'{subdir}/tetedecap2.gif', xflip=True, tick=8,  dx= 2 * CHAR_W, dy=11 * SCALE_Y),  # noqa
            Frame(f'{subdir}/tetedecap3.gif', xflip=True, tick=12, dx= 3 * CHAR_W, dy=11 * SCALE_Y),  # noqa
            Frame(f'{subdir}/tetedecap4.gif', xflip=True, tick=16, dx= 4 * CHAR_W, dy=18 * SCALE_Y),  # noqa
            Frame(f'{subdir}/tetedecap5.gif', xflip=True, tick=20, dx= 5 * CHAR_W, dy=25 * SCALE_Y),  # noqa
            Frame(f'{subdir}/tetedecap6.gif', xflip=True, tick=24, dx= 6 * CHAR_W, dy=25 * SCALE_Y),  # noqa
            Frame(f'{subdir}/tetedecap1.gif', xflip=True, tick=28, dx= 7 * CHAR_W, dy=39 * SCALE_Y),  # noqa
            Frame(f'{subdir}/tetedecap2.gif', xflip=True, tick=32, dx= 8 * CHAR_W, dy=59 * SCALE_Y),  # noqa
            Frame(f'{subdir}/tetedecap3.gif', xflip=True, tick=36, dx= 9 * CHAR_W, dy=59 * SCALE_Y),  # noqa
            Frame(f'{subdir}/tetedecap4.gif', xflip=True, tick=40, dx=10 * CHAR_W, dy=59 * SCALE_Y),  # noqa
            Frame(f'{subdir}/tetedecap5.gif', xflip=True, tick=44, dx=11 * CHAR_W, dy=59 * SCALE_Y),  # noqa
            Frame(f'{subdir}/tetedecap6.gif', xflip=True, tick=48, dx=12 * CHAR_W, dy=57 * SCALE_Y),  # noqa
            Frame(f'{subdir}/tetedecap1.gif', xflip=True, tick=52, dx=13 * CHAR_W, dy=59 * SCALE_Y),  # noqa
            Frame(f'{subdir}/tetedecap2.gif', xflip=True, tick=56, dx=14 * CHAR_W, dy=57 * SCALE_Y),  # noqa
            Frame(f'{subdir}/tetedecap3.gif', xflip=True, tick=57, dx=15 * CHAR_W, dy=65 * SCALE_Y),  # noqa
            # @formatter:on
        ], actions=[
            Act(tick=29, act=Actions.snd('tete.ogg')),
            Act(tick=45, act=Actions.snd('tete.ogg')),
            Act(tick=58, act=Actions.stop),
        ]),
        'football': Animation(frames=[
            # @formatter:off
            Frame(f'{subdir}/tetedecap3.gif', tick=  4, mv=(CHAR_W, 0), dy=-2 * 0.6 * CHAR_H),  # noqa
            Frame(f'{subdir}/tetedecap2.gif', tick=  7, mv=(CHAR_W, 0), dy=-2 * 0.7 * CHAR_H),  # noqa
            Frame(f'{subdir}/tetedecap1.gif', tick= 15, mv=(CHAR_W, 0), dy=-2 * 0.9 * CHAR_H),  # noqa
            Frame(f'{subdir}/tetedecap6.gif', tick= 22, mv=(CHAR_W, 0), dy=-2 * 0.8 * CHAR_H),  # noqa
            Frame(f'{subdir}/tetedecap5.gif', tick= 30, mv=(CHAR_W, 0), dy=-2 * 0.4 * CHAR_H),  # noqa
            Frame(f'{subdir}/tetedecap4.gif', tick= 37, mv=(CHAR_W, 0), dy=-2 * 0   * CHAR_H),  # noqa
            Frame(f'{subdir}/tetedecap3.gif', tick= 45, mv=(CHAR_W, 0), dy=-2 * 0.1 * CHAR_H),  # noqa
            Frame(f'{subdir}/tetedecap2.gif', tick= 52, mv=(CHAR_W, 0), dy=-2 * 0.3 * CHAR_H),  # noqa
            Frame(f'{subdir}/tetedecap1.gif', tick= 60, mv=(CHAR_W, 0), dy=-2 * 0.5 * CHAR_H),  # noqa
            Frame(f'{subdir}/tetedecap6.gif', tick= 67, mv=(CHAR_W, 0), dy=-2 * 0.3 * CHAR_H),  # noqa
            Frame(f'{subdir}/tetedecap5.gif', tick= 75, mv=(CHAR_W, 0), dy=-2 * 0.1 * CHAR_H),  # noqa
            Frame(f'{subdir}/tetedecap4.gif', tick= 82, mv=(CHAR_W, 0), dy=-2 * 0   * CHAR_H),  # noqa
            Frame(f'{subdir}/tetedecap3.gif', tick= 90, mv=(CHAR_W, 0), dy=-2 * 0.1 * CHAR_H),  # noqa
            Frame(f'{subdir}/tetedecap2.gif', tick= 97, mv=(CHAR_W, 0), dy=-2 * 0.4 * CHAR_H),  # noqa
            Frame(f'{subdir}/tetedecap1.gif', tick=105, mv=(CHAR_W, 0), dy=-2 * 0.1 * CHAR_H),  # noqa
            Frame(f'{subdir}/tetedecap3.gif', tick=112, mv=(CHAR_W, 0), dy=-2 * 0   * CHAR_H),  # noqa
            # @formatter:on
        ], actions=[
            Act(tick=0, act=Actions.snd('tete2.ogg')),
            Act(tick=38, act=Actions.snd('tete.ogg')),
            Act(tick=83, act=Actions.snd('tete.ogg')),
            Act(tick=113, act=Actions.stop),
        ]),
    }


def teteombre_decap():
    return {
        'teteagauche': Animation(frames=[
            # @formatter:off
            Frame('spritesA/teteombre.gif', tick=4,  dx=  1 * CHAR_W, dy=71 * SCALE_Y),  # noqa
            Frame('spritesA/teteombre.gif', tick=8,  dx=  0 * CHAR_W, dy=71 * SCALE_Y),  # noqa
            Frame('spritesA/teteombre.gif', tick=12, dx= -1 * CHAR_W, dy=71 * SCALE_Y),  # noqa
            Frame('spritesA/teteombre.gif', tick=16, dx= -2 * CHAR_W, dy=71 * SCALE_Y),  # noqa
            Frame('spritesA/teteombre.gif', tick=20, dx= -3 * CHAR_W, dy=71 * SCALE_Y),  # noqa
            Frame('spritesA/teteombre.gif', tick=24, dx= -4 * CHAR_W, dy=71 * SCALE_Y),  # noqa
            Frame('spritesA/teteombre.gif', tick=28, dx= -5 * CHAR_W, dy=71 * SCALE_Y),  # noqa
            Frame('spritesA/teteombre.gif', tick=32, dx= -6 * CHAR_W, dy=71 * SCALE_Y),  # noqa
            Frame('spritesA/teteombre.gif', tick=36, dx= -7 * CHAR_W, dy=71 * SCALE_Y),  # noqa
            Frame('spritesA/teteombre.gif', tick=40, dx= -8 * CHAR_W, dy=71 * SCALE_Y),  # noqa
            Frame('spritesA/teteombre.gif', tick=44, dx= -9 * CHAR_W, dy=71 * SCALE_Y),  # noqa
            Frame('spritesA/teteombre.gif', tick=48, dx=-10 * CHAR_W, dy=71 * SCALE_Y),  # noqa
            Frame('spritesA/teteombre.gif', tick=52, dx=-11 * CHAR_W, dy=71 * SCALE_Y),  # noqa
            Frame('spritesA/teteombre.gif', tick=56, dx=-12 * CHAR_W, dy=71 * SCALE_Y),  # noqa
            Frame('spritesA/teteombre.gif', tick=57, dx=-13 * CHAR_W, dy=71 * SCALE_Y, post_action=Actions.stop),
            # @formatter:on
        ]),
        'teteadroite': Animation(frames=[
            # @formatter:off
            Frame('spritesA/teteombre.gif', tick=4,  dx=1.4 * CHAR_W, dy=71 * SCALE_Y),  # noqa
            Frame('spritesA/teteombre.gif', tick=8,  dx=  2 * CHAR_W, dy=71 * SCALE_Y),  # noqa
            Frame('spritesA/teteombre.gif', tick=12, dx=  3 * CHAR_W, dy=71 * SCALE_Y),  # noqa
            Frame('spritesA/teteombre.gif', tick=16, dx=  4 * CHAR_W, dy=71 * SCALE_Y),  # noqa
            Frame('spritesA/teteombre.gif', tick=20, dx=  5 * CHAR_W, dy=71 * SCALE_Y),  # noqa
            Frame('spritesA/teteombre.gif', tick=24, dx=  6 * CHAR_W, dy=71 * SCALE_Y),  # noqa
            Frame('spritesA/teteombre.gif', tick=28, dx=  7 * CHAR_W, dy=71 * SCALE_Y),  # noqa
            Frame('spritesA/teteombre.gif', tick=32, dx=  8 * CHAR_W, dy=71 * SCALE_Y),  # noqa
            Frame('spritesA/teteombre.gif', tick=36, dx=  9 * CHAR_W, dy=71 * SCALE_Y),  # noqa
            Frame('spritesA/teteombre.gif', tick=40, dx= 10 * CHAR_W, dy=71 * SCALE_Y),  # noqa
            Frame('spritesA/teteombre.gif', tick=44, dx= 11 * CHAR_W, dy=71 * SCALE_Y),  # noqa
            Frame('spritesA/teteombre.gif', tick=48, dx= 12 * CHAR_W, dy=71 * SCALE_Y),  # noqa
            Frame('spritesA/teteombre.gif', tick=52, dx= 13 * CHAR_W, dy=71 * SCALE_Y),  # noqa
            Frame('spritesA/teteombre.gif', tick=56, dx= 14 * CHAR_W, dy=71 * SCALE_Y),  # noqa
            Frame('spritesA/teteombre.gif', tick=57, dx= 15 * CHAR_W, dy=71 * SCALE_Y, post_action=Actions.stop),  # noqa
            # @formatter:on
        ]),
        'football': Animation(frames=[
            # @formatter:off
            Frame(f'spritesA/teteombre.gif', tick=4,   mv=(CHAR_W, 0)),  # noqa
            Frame(f'spritesA/teteombre.gif', tick=7,   mv=(CHAR_W, 0)),  # noqa
            Frame(f'spritesA/teteombre.gif', tick=15,  mv=(CHAR_W, 0)),  # noqa
            Frame(f'spritesA/teteombre.gif', tick=22,  mv=(CHAR_W, 0)),  # noqa
            Frame(f'spritesA/teteombre.gif', tick=30,  mv=(CHAR_W, 0)),  # noqa
            Frame(f'spritesA/teteombre.gif', tick=37,  mv=(CHAR_W, 0)),  # noqa
            Frame(f'spritesA/teteombre.gif', tick=45,  mv=(CHAR_W, 0)),  # noqa
            Frame(f'spritesA/teteombre.gif', tick=52,  mv=(CHAR_W, 0)),  # noqa
            Frame(f'spritesA/teteombre.gif', tick=60,  mv=(CHAR_W, 0)),  # noqa
            Frame(f'spritesA/teteombre.gif', tick=67,  mv=(CHAR_W, 0)),  # noqa
            Frame(f'spritesA/teteombre.gif', tick=75,  mv=(CHAR_W, 0)),  # noqa
            Frame(f'spritesA/teteombre.gif', tick=82,  mv=(CHAR_W, 0)),  # noqa
            Frame(f'spritesA/teteombre.gif', tick=90,  mv=(CHAR_W, 0)),  # noqa
            Frame(f'spritesA/teteombre.gif', tick=97,  mv=(CHAR_W, 0)),  # noqa
            Frame(f'spritesA/teteombre.gif', tick=105, mv=(CHAR_W, 0)),  # noqa
            Frame(f'spritesA/teteombre.gif', tick=112, mv=(CHAR_W, 0), post_action=Actions.stop),  # noqa
            # @formatter:on
        ]),
    }


def vie():
    return {
        'vie': Animation(frames=[
            # @formatter:off
            Frame('fill', w=1,    h=10, fill=(0, 0, 0), dx=0, post_action=Actions.stop),  # noqa
            Frame('fill', w=6,    h=10, fill=(0, 0, 0), dx=-5    * SCALE_X),  # noqa
            Frame('fill', w=17,   h=10, fill=(0, 0, 0), dx=-16   * SCALE_X),  # noqa
            Frame('fill', w=22,   h=10, fill=(0, 0, 0), dx=-21   * SCALE_X),  # noqa
            Frame('fill', w=27.1, h=10, fill=(0, 0, 0), dx=-26.1 * SCALE_X),  # noqa
            Frame('fill', w=38,   h=10, fill=(0, 0, 0), dx=-37   * SCALE_X),  # noqa
            Frame('fill', w=43.1, h=10, fill=(0, 0, 0), dx=-42.1 * SCALE_X),  # noqa
            # @formatter:on
        ]),
        'vie_rtl': Animation(frames=[
            # @formatter:off
            Frame('fill', w=1,    h=10, fill=(0, 0, 0), post_action=Actions.stop),  # noqa
            Frame('fill', w=6,    h=10, fill=(0, 0, 0)),  # noqa
            Frame('fill', w=17,   h=10, fill=(0, 0, 0)),  # noqa
            Frame('fill', w=22,   h=10, fill=(0, 0, 0)),  # noqa
            Frame('fill', w=27.1, h=10, fill=(0, 0, 0)),  # noqa
            Frame('fill', w=38,   h=10, fill=(0, 0, 0)),  # noqa
            Frame('fill', w=43.1, h=10, fill=(0, 0, 0)),  # noqa
            # @formatter:on
        ]),
    }


def barb(subdir: str):
    return {
        'debout': Animation(frames=[
            Frame(f'{subdir}/debout.gif'),
        ]),
        'attente': Animation(frames=[
            Frame(f'{subdir}/attente1.gif', tick=15),
            Frame(f'{subdir}/attente2.gif', tick=23),
            Frame(f'{subdir}/attente3.gif', tick=30),
            Frame(f'{subdir}/attente2.gif', tick=37),
            Frame(f'{subdir}/attente1.gif', tick=50),
        ], actions=[
            Act(tick=8, act=Actions.snd('attente.ogg'))
        ]),
        'avance': Animation(frames=[
            # @formatter:off
            Frame(f'{subdir}/marche1.gif', tick=9,  mv=(CHAR_W, 0)),
            Frame(f'{subdir}/marche2.gif', tick=17, mv=(CHAR_W, 0)),
            Frame(f'{subdir}/marche3.gif', tick=27, mv=(CHAR_W, 0)),
            Frame(f'{subdir}/debout.gif',  tick=36, mv=(CHAR_W, 0)),
            Frame(f'{subdir}/debout.gif',  tick=37),
            # @formatter:on
        ]),
        'recule': Animation(frames=[
            # @formatter:off
            Frame(f'{subdir}/marche3.gif', tick=9,  mv=(-CHAR_W, 0)),
            Frame(f'{subdir}/marche2.gif', tick=18, mv=(-CHAR_W, 0)),
            Frame(f'{subdir}/marche1.gif', tick=26, mv=(-CHAR_W, 0)),
            Frame(f'{subdir}/debout.gif',  tick=36, mv=(-CHAR_W, 0)),
            Frame(f'{subdir}/debout.gif',  tick=37),
            # @formatter:on
        ]),
        'saute': Animation(frames=[
            # @formatter:off
            Frame(f'{subdir}/saut1.gif',  tick=13),
            Frame(f'{subdir}/saut2.gif',  tick=30),
            Frame(f'{subdir}/saut1.gif',  tick=40),
            Frame(f'{subdir}/debout.gif', tick=47),
            # @formatter:on
        ]),
        'assis': Animation(frames=[
            Frame(f'{subdir}/assis1.gif'),
            Frame(f'{subdir}/assis2.gif'),
        ]),
        'releve': Animation(frames=[
            Frame(f'{subdir}/assis1.gif'),
        ]),
        'rouladeAV': Animation(frames=[
            # @formatter:off
            Frame(f'{subdir}/roulade1.gif',             tick=4,  mv=(CHAR_W, 0)),  # noqa
            Frame(f'{subdir}/roulade1.gif',             tick=7,  mv=(CHAR_W, 0)),  # noqa
            Frame(f'{subdir}/roulade1.gif',             tick=10, mv=(CHAR_W, 0)),  # noqa
            Frame(f'{subdir}/roulade2.gif',             tick=13, mv=(CHAR_W, 0)),  # noqa
            Frame(f'{subdir}/roulade3.gif',             tick=16, mv=(CHAR_W, 0)),  # noqa
            Frame(f'{subdir}/roulade3.gif',             tick=19, mv=(CHAR_W, 0)),  # noqa
            Frame(f'{subdir}/roulade2.gif', xflip=True, tick=22, mv=(CHAR_W, 0)),  # noqa
            Frame(f'{subdir}/roulade2.gif', xflip=True, tick=25, mv=(CHAR_W, 0)),  # noqa
            Frame(f'{subdir}/roulade5.gif',             tick=28, mv=(CHAR_W, 0)),  # noqa
            Frame(f'{subdir}/roulade5.gif',             tick=30, mv=(CHAR_W, 0)),  # noqa
            Frame(f'{subdir}/roulade1.gif', xflip=True, tick=34, mv=(CHAR_W, 0)),  # noqa
            Frame(f'{subdir}/debout.gif',               tick=40,               ),  # noqa
            # @formatter:on
        ], actions=[
            Act(tick=2, act=Actions.snd('roule.ogg'))
        ]),
        'rouladeAV-out': Animation(frames=[
            # non-movable roulade out
            # @formatter:off
            Frame(f'{subdir}/roulade3.gif',             tick=16),  # noqa
            Frame(f'{subdir}/roulade3.gif',             tick=19),  # noqa
            Frame(f'{subdir}/roulade2.gif', xflip=True, tick=22),  # noqa
            Frame(f'{subdir}/roulade2.gif', xflip=True, tick=25),  # noqa
            Frame(f'{subdir}/roulade5.gif',             tick=28),  # noqa
            Frame(f'{subdir}/roulade5.gif',             tick=30),  # noqa
            Frame(f'{subdir}/roulade1.gif', xflip=True, tick=34),  # noqa
            Frame(f'{subdir}/debout.gif',               tick=40),  # noqa
            # @formatter:on
        ]),
        'rouladeAR': Animation(frames=[
            # @formatter:off
            Frame(f'{subdir}/roulade1.gif', xflip=True, tick=5,  mv=(-CHAR_W, 0)),  # noqa
            Frame(f'{subdir}/roulade5.gif',             tick=8,  mv=(-CHAR_W, 0)),  # noqa
            Frame(f'{subdir}/roulade2.gif', xflip=True, tick=11, mv=(-CHAR_W, 0)),  # noqa
            Frame(f'{subdir}/roulade2.gif', xflip=True, tick=14, mv=(-CHAR_W, 0)),  # noqa
            Frame(f'{subdir}/roulade3.gif',             tick=17, mv=(-CHAR_W, 0)),  # noqa
            Frame(f'{subdir}/roulade3.gif',             tick=20, mv=(-CHAR_W, 0)),  # noqa
            Frame(f'{subdir}/roulade2.gif',             tick=23, mv=(-CHAR_W, 0)),  # noqa
            Frame(f'{subdir}/roulade2.gif',             tick=26, mv=(-CHAR_W, 0)),  # noqa
            Frame(f'{subdir}/roulade1.gif',             tick=29, mv=(-CHAR_W, 0)),  # noqa
            Frame(f'{subdir}/roulade1.gif',             tick=35, mv=(-CHAR_W, 0)),  # noqa
            # @formatter:on
        ], actions=[
            Act(tick=2, act=Actions.snd('roule.ogg'))
        ]),
        'protegeH': Animation(frames=[
            # @formatter:off
            Frame(f'{subdir}/marche1.gif',  tick=5, mv=(-CHAR_W, 0)),
            Frame(f'{subdir}/protegeH.gif', tick=9, dx=-2 * SCALE_X),
            # @formatter:on
        ], actions=[
            Act(tick=2, act=Actions.snd('protege.ogg'))
        ]),
        'protegeD': Animation(frames=[
            Frame(f'{subdir}/protegeH.gif', tick=5, dx=-2 * SCALE_X),
            Frame(f'{subdir}/protegeD.gif', tick=9, dx=-2 * SCALE_X),
        ]),
        'cou': Animation(frames=[
            # @formatter:off
            Frame(f'{subdir}/protegeH.gif', tick=15, dx=-2 * SCALE_X, post_action=Actions.snd('epee.ogg')),
            Frame(f'{subdir}/cou2.gif',     tick=30, dx=-4 * SCALE_X),
            Frame(f'{subdir}/cou3.gif',     tick=46, dx=-1 * SCALE_X),
            # @formatter:on
        ]),
        'devant': Animation(frames=[
            # @formatter:off
            Frame(f'{subdir}/devant1.gif', tick=10, post_action=Actions.snd('epee.ogg')),
            Frame(f'{subdir}/devant2.gif', tick=20),
            Frame(f'{subdir}/devant3.gif', tick=30),
            Frame(f'{subdir}/devant2.gif', tick=46),
            # @formatter:on
        ]),
        'genou': Animation(frames=[
            # @formatter:off
            Frame(f'{subdir}/genou1.gif', tick=10, dx=CHAR_W / 4, post_action=Actions.snd('epee.ogg')),
            Frame(f'{subdir}/assis2.gif', tick=20),
            Frame(f'{subdir}/genou3.gif', tick=30, dx=CHAR_W / 4),
            Frame(f'{subdir}/assis2.gif', tick=46),
            # @formatter:on
        ]),
        'araignee': Animation(frames=[
            # @formatter:off
            Frame(f'{subdir}/toile1.gif', tick=8, post_action=Actions.snd('epee.ogg')),
            Frame(f'{subdir}/toile2.gif', tick=15),
            Frame(f'{subdir}/toile3.gif', tick=20, post_action=Actions.snd('epee.ogg')),
            Frame(f'{subdir}/toile4.gif', tick=33),
            # @formatter:on
        ]),
        'coupdepied': Animation(frames=[
            # @formatter:off
            Frame(f'{subdir}/pied1.gif',  tick=9),
            Frame(f'{subdir}/pied2.gif',  tick=30),
            Frame(f'{subdir}/pied1.gif',  tick=45),
            Frame(f'{subdir}/debout.gif', tick=51),
            # @formatter:on
        ]),
        'coupdetete': Animation(frames=[
            # @formatter:off
            Frame(f'{subdir}/tete1.gif', tick=18),
            Frame(f'{subdir}/tete2.gif', tick=28, mv=( CHAR_W, 0)),  # noqa
            Frame(f'{subdir}/tete1.gif', tick=38, mv=(-CHAR_W, 0)),  # noqa
            # @formatter:on
        ]),
        'decapite': Animation(frames=[
            # @formatter:off
            Frame(f'{subdir}/retourne1.gif', tick=4,  mv=(CHAR_W, 0)),  # noqa
            Frame(f'{subdir}/retourne1.gif', tick=5,  mv=(CHAR_W, 0)),  # noqa
            Frame(f'{subdir}/retourne2.gif', tick=9,                ),  # noqa
            Frame(f'{subdir}/retourne2.gif', tick=14, mv=(CHAR_W, 0)),  # noqa
            Frame(f'{subdir}/retourne3.gif', tick=15,                 post_action=Actions.snd('decapite.ogg')),  # noqa
            Frame(f'{subdir}/retourne3.gif', tick=19, mv=(CHAR_W, 0)),  # noqa
            Frame(f'{subdir}/retourne3.gif', tick=24, mv=(CHAR_W, 0)),  # noqa
            Frame(f'{subdir}/retourne3.gif', tick=29,               ),  # noqa
            Frame(f'{subdir}/protegeH.gif',  tick=33,                               ),  # noqa
            Frame(f'{subdir}/cou2.gif',      tick=39,                dx=-2 * SCALE_X),  # noqa
            Frame(f'{subdir}/cou3.gif',      tick=51,                               ),  # noqa
            Frame(f'{subdir}/cou2.gif',      tick=60,                dx=-3 * SCALE_X),  # noqa
            # @formatter:on
        ]),
        'front': Animation(frames=[
            Frame(f'{subdir}/front1.gif', tick=5, dx=-1 * SCALE_X, post_action=Actions.snd('epee.ogg')),
            Frame(f'{subdir}/front2.gif', tick=23),
            Frame(f'{subdir}/front3.gif', tick=30),
            Frame(f'{subdir}/front2.gif', tick=46),
        ]),
        'retourne': Animation(frames=[
            Frame(f'{subdir}/retourne1.gif', tick=5,  mv=(CHAR_W, 0)),
            Frame(f'{subdir}/retourne2.gif', tick=10, mv=(CHAR_W, 0)),
            Frame(f'{subdir}/retourne3.gif', tick=18, mv=(CHAR_W, 0)),
        ]),
        'vainqueur': Animation(frames=[
            Frame(f'{subdir}/vainqueur1.gif', xflip=True, tick=18),
            Frame(f'{subdir}/vainqueur2.gif', xflip=True, tick=35),
            Frame(f'{subdir}/vainqueur3.gif', xflip=True, tick=85),
            Frame(f'{subdir}/vainqueur2.gif', xflip=True, tick=100),
            Frame(f'{subdir}/vainqueur1.gif', xflip=True, tick=101, post_action=Actions.stop),
        ]),
        'vainqueurKO': Animation(frames=[
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
            Frame(f'{subdir}/vainqueur1.gif', xflip=True, tick=231, post_action=Actions.stop),  # noqa
            # @formatter:on
        ]),
        'touche1': Animation(frames=[
            # @formatter:off
            Frame(f'{subdir}/touche2.gif', tick=1),
            Frame(f'{subdir}/touche2.gif', tick=5,  mv=(-CHAR_W,     0)),  # noqa
            Frame(f'{subdir}/touche1.gif', tick=10, mv=(-2 * CHAR_W, 0)),  # noqa
            Frame(f'{subdir}/touche2.gif', tick=20, mv=(-CHAR_W,     0)),  # noqa
            Frame(f'{subdir}/debout.gif',  tick=21),
            # @formatter:on
        ]),
        'tombe1': Animation(frames=[
            # @formatter:off
            Frame(f'{subdir}/tombe1.gif', tick=1,                   dx=-2 * CHAR_W),  # noqa
            Frame(f'{subdir}/tombe1.gif', tick=9,  mv=(-CHAR_W, 0), dx=-2 * CHAR_W),  # noqa
            Frame(f'{subdir}/tombe2.gif', tick=15, mv=(-CHAR_W, 0), dx=-3 * CHAR_W),  # noqa
            Frame(f'{subdir}/tombe3.gif', tick=25,                  dx=-3 * CHAR_W),  # noqa
            Frame(f'{subdir}/debout.gif', tick=27, mv=(-CHAR_W, 0)),
            # @formatter:on
        ]),
        'mort': Animation(frames=[
            # @formatter:off
            Frame(f'{subdir}/assis1.gif', tick=15, pre_action=Actions.snd('mortKO.ogg')),
            Frame(f'{subdir}/mort2.gif',  tick=17, post_action=Actions.stop),
            Frame(f'{subdir}/mort3.gif',  tick=18, dx=-1 * CHAR_W),  # manual, see vainqueurKO
            Frame(f'{subdir}/mort4.gif',  tick=19, dx=-3 * CHAR_W),  # manual, see vainqueurKO
            # @formatter:on
        ]),
        'mortdecap': Animation(frames=[
            # @formatter:off
            Frame(f'{subdir}/decap1.gif', tick=35, pre_action=Actions.snd('mortdecap.ogg')),
            Frame(f'{subdir}/decap2.gif', tick=70, dx=2 * CHAR_W),
            Frame(f'{subdir}/decap3.gif', tick=80, dx=2 * CHAR_W),
            Frame(f'{subdir}/decap4.gif', tick=82, dx=2 * CHAR_W, post_action=Actions.stop),
            # @formatter:on
        ]),
        'mortgnome': Animation(frames=[
            Frame(f'{subdir}/mort4.gif', tick=0, mv=(CHAR_W / 12, 0)),
        ]),
        'mortdecapgnome': Animation(frames=[
            Frame(f'{subdir}/decap4.gif', tick=0, mv=(CHAR_W / 12, 0)),
        ]),
    }


def barb_rtl(subdir: str):
    return {
        'debout': Animation(frames=[
            Frame(f'{subdir}/debout.gif', xflip=True),
        ]),
        'attente': Animation(frames=[
            Frame(f'{subdir}/attente1.gif', xflip=True, tick=15),
            Frame(f'{subdir}/attente2.gif', xflip=True, tick=23, dx=-CHAR_W),
            Frame(f'{subdir}/attente3.gif', xflip=True, tick=30, dx=-CHAR_W),
            Frame(f'{subdir}/attente2.gif', xflip=True, tick=37, dx=-CHAR_W),
            Frame(f'{subdir}/attente1.gif', xflip=True, tick=50),
        ], actions=[
            Act(tick=8, act=Actions.snd('attente.ogg'))
        ]),
        'avance': Animation(frames=[
            # @formatter:off
            Frame(f'{subdir}/marche1.gif', xflip=True, tick=9,  mv=(-CHAR_W, 0)),
            Frame(f'{subdir}/marche2.gif', xflip=True, tick=17, mv=(-CHAR_W, 0)),
            Frame(f'{subdir}/marche3.gif', xflip=True, tick=27, mv=(-CHAR_W, 0)),
            Frame(f'{subdir}/debout.gif',  xflip=True, tick=36, mv=(-CHAR_W, 0)),
            Frame(f'{subdir}/debout.gif',  xflip=True, tick=37),
            # @formatter:on
        ]),
        'recule': Animation(frames=[
            # @formatter:off
            Frame(f'{subdir}/marche3.gif', xflip=True, tick=9,  mv=(CHAR_W, 0)),
            Frame(f'{subdir}/marche2.gif', xflip=True, tick=18, mv=(CHAR_W, 0)),
            Frame(f'{subdir}/marche1.gif', xflip=True, tick=26, mv=(CHAR_W, 0)),
            Frame(f'{subdir}/debout.gif',  xflip=True, tick=36, mv=(CHAR_W, 0)),
            Frame(f'{subdir}/debout.gif',  xflip=True, tick=37),
            # @formatter:on
        ]),
        'saute': Animation(frames=[
            # @formatter:off
            Frame(f'{subdir}/saut1.gif',  xflip=True, tick=13, dx=-CHAR_W),
            Frame(f'{subdir}/saut2.gif',  xflip=True, tick=30, dx=-CHAR_W),
            Frame(f'{subdir}/saut1.gif',  xflip=True, tick=40, dx=-CHAR_W),
            Frame(f'{subdir}/debout.gif', xflip=True, tick=47),
            # @formatter:on
        ]),
        'assis': Animation(frames=[
            Frame(f'{subdir}/assis1.gif', xflip=True),
            Frame(f'{subdir}/assis2.gif', xflip=True),
        ]),
        'releve': Animation(frames=[
            Frame(f'{subdir}/assis1.gif', xflip=True),
        ]),
        'rouladeAV': Animation(frames=[
            # @formatter:off
            Frame(f'{subdir}/roulade1.gif', xflip=True, tick=4,  mv=(-CHAR_W, 0)),  # noqa
            Frame(f'{subdir}/roulade1.gif', xflip=True, tick=7,  mv=(-CHAR_W, 0)),  # noqa
            Frame(f'{subdir}/roulade1.gif', xflip=True, tick=10, mv=(-CHAR_W, 0)),  # noqa
            Frame(f'{subdir}/roulade2.gif', xflip=True, tick=13, mv=(-CHAR_W, 0)),  # noqa
            Frame(f'{subdir}/roulade3.gif',             tick=16, mv=(-CHAR_W, 0)),  # noqa
            Frame(f'{subdir}/roulade3.gif',             tick=19, mv=(-CHAR_W, 0)),  # noqa
            Frame(f'{subdir}/roulade2.gif',             tick=22, mv=(-CHAR_W, 0)),  # noqa
            Frame(f'{subdir}/roulade2.gif',             tick=25, mv=(-CHAR_W, 0)),  # noqa
            Frame(f'{subdir}/roulade5.gif',             tick=28, mv=(-CHAR_W, 0)),  # noqa
            Frame(f'{subdir}/roulade5.gif',             tick=30, mv=(-CHAR_W, 0)),  # noqa
            Frame(f'{subdir}/roulade1.gif',             tick=34, mv=(-CHAR_W, 0)),  # noqa
            Frame(f'{subdir}/debout.gif',   xflip=True, tick=40,                ),  # noqa
            # @formatter:on
        ], actions=[
            Act(tick=2, act=Actions.snd('roule.ogg'))
        ]),
        'rouladeAV-out': Animation(frames=[
            # non-movable roulade out
            # @formatter:off
            Frame(f'{subdir}/roulade3.gif',             tick=16),  # noqa
            Frame(f'{subdir}/roulade3.gif',             tick=19),  # noqa
            Frame(f'{subdir}/roulade2.gif',             tick=22),  # noqa
            Frame(f'{subdir}/roulade2.gif',             tick=25),  # noqa
            Frame(f'{subdir}/roulade5.gif',             tick=28),  # noqa
            Frame(f'{subdir}/roulade5.gif',             tick=30),  # noqa
            Frame(f'{subdir}/roulade1.gif',             tick=34),  # noqa
            Frame(f'{subdir}/debout.gif',   xflip=True, tick=40),  # noqa
            # @formatter:on
        ]),
        'rouladeAR': Animation(frames=[
            # @formatter:off
            Frame(f'{subdir}/roulade1.gif',             tick=5,  mv=(CHAR_W, 0)),  # noqa
            Frame(f'{subdir}/roulade5.gif',             tick=8,  mv=(CHAR_W, 0)),  # noqa
            Frame(f'{subdir}/roulade2.gif',             tick=11, mv=(CHAR_W, 0)),  # noqa
            Frame(f'{subdir}/roulade2.gif',             tick=14, mv=(CHAR_W, 0)),  # noqa
            Frame(f'{subdir}/roulade3.gif',             tick=17, mv=(CHAR_W, 0)),  # noqa
            Frame(f'{subdir}/roulade3.gif',             tick=20, mv=(CHAR_W, 0)),  # noqa
            Frame(f'{subdir}/roulade2.gif', xflip=True, tick=23, mv=(CHAR_W, 0)),  # noqa
            Frame(f'{subdir}/roulade2.gif', xflip=True, tick=26, mv=(CHAR_W, 0)),  # noqa
            Frame(f'{subdir}/roulade1.gif', xflip=True, tick=29, mv=(CHAR_W, 0)),  # noqa
            Frame(f'{subdir}/roulade1.gif', xflip=True, tick=35, mv=(CHAR_W, 0)),  # noqa
            # @formatter:on
        ], actions=[
            Act(tick=2, act=Actions.snd('roule.ogg'))
        ]),
        'protegeH': Animation(frames=[
            # @formatter:off
            Frame(f'{subdir}/marche1.gif',  xflip=True, tick=5, mv=(CHAR_W, 0)),
            Frame(f'{subdir}/protegeH.gif', xflip=True, tick=9, dx=-CHAR_W + 2 * SCALE_X),
            # @formatter:on
        ], actions=[
            Act(tick=2, act=Actions.snd('protege.ogg'))
        ]),
        'protegeD': Animation(frames=[
            Frame(f'{subdir}/protegeH.gif', xflip=True, tick=5, dx=-CHAR_W + 2 * SCALE_X),
            Frame(f'{subdir}/protegeD.gif', xflip=True, tick=9, dx=-CHAR_W + 2 * SCALE_X),
        ]),
        'cou': Animation(frames=[
            # @formatter:off
            Frame(f'{subdir}/protegeH.gif', xflip=True, tick=15, dx=-CHAR_W + 2 * SCALE_X, post_action=Actions.snd('epee.ogg')),  # noqa
            Frame(f'{subdir}/cou2.gif',     xflip=True, tick=30, dx=-CHAR_W + 4 * SCALE_X    ),  # noqa
            Frame(f'{subdir}/cou3.gif',     xflip=True, tick=46, dx=-4 * CHAR_W + 1 * SCALE_X),  # noqa
            # @formatter:on
        ]),
        'devant': Animation(frames=[
            # @formatter:off
            Frame(f'{subdir}/devant1.gif', xflip=True, tick=10, post_action=Actions.snd('epee.ogg')),
            Frame(f'{subdir}/devant2.gif', xflip=True, tick=20),
            Frame(f'{subdir}/devant3.gif', xflip=True, tick=30, dx=-3 * CHAR_W),
            Frame(f'{subdir}/devant2.gif', xflip=True, tick=46),
            # @formatter:on
        ]),
        'genou': Animation(frames=[
            # @formatter:off
            Frame(f'{subdir}/genou1.gif', xflip=True, tick=10, dx=-CHAR_W / 4, post_action=Actions.snd('epee.ogg')),
            Frame(f'{subdir}/assis2.gif', xflip=True, tick=20),
            Frame(f'{subdir}/genou3.gif', xflip=True, tick=30, dx=-CHAR_W / 4
                                                                  - 3 * CHAR_W),
            Frame(f'{subdir}/assis2.gif', xflip=True, tick=46),
            # @formatter:on
        ]),
        'araignee': Animation(frames=[
            # @formatter:off
            Frame(f'{subdir}/toile1.gif', xflip=True, tick=8,  dx=-CHAR_W, post_action=Actions.snd('epee.ogg')),
            Frame(f'{subdir}/toile2.gif', xflip=True, tick=15, dx=-CHAR_W),
            Frame(f'{subdir}/toile3.gif', xflip=True, tick=20, dx=-CHAR_W, post_action=Actions.snd('epee.ogg')),
            Frame(f'{subdir}/toile4.gif', xflip=True, tick=33, dx=-3 * CHAR_W),
            # @formatter:on
        ]),
        'coupdepied': Animation(frames=[
            # @formatter:off
            Frame(f'{subdir}/pied1.gif',  xflip=True, tick=9,  dx=-CHAR_W),
            Frame(f'{subdir}/pied2.gif',  xflip=True, tick=30, dx=-CHAR_W),
            Frame(f'{subdir}/pied1.gif',  xflip=True, tick=45, dx=-CHAR_W),
            Frame(f'{subdir}/debout.gif', xflip=True, tick=51),
            # @formatter:on
        ]),
        'coupdetete': Animation(frames=[
            # @formatter:off
            Frame(f'{subdir}/tete1.gif', xflip=True, tick=18),
            Frame(f'{subdir}/tete2.gif', xflip=True, tick=28),
            Frame(f'{subdir}/tete1.gif', xflip=True, tick=38),
            # @formatter:on
        ]),
        'decapite': Animation(frames=[
            # @formatter:off
            Frame(f'{subdir}/retourne1.gif', xflip=True, tick=4,  mv=(-CHAR_W, 0)),  # noqa
            Frame(f'{subdir}/retourne1.gif', xflip=True, tick=5,  mv=(-CHAR_W, 0)),  # noqa
            Frame(f'{subdir}/retourne2.gif', xflip=True, tick=9,                 ),  # noqa
            Frame(f'{subdir}/retourne2.gif', xflip=True, tick=14, mv=(-CHAR_W, 0)),  # noqa
            Frame(f'{subdir}/retourne3.gif', xflip=True, tick=15,                  post_action=Actions.snd('decapite.ogg')),  # noqa
            Frame(f'{subdir}/retourne3.gif', xflip=True, tick=19, mv=(-CHAR_W, 0)),  # noqa
            Frame(f'{subdir}/retourne3.gif', xflip=True, tick=24, mv=(-CHAR_W, 0)),  # noqa
            Frame(f'{subdir}/retourne3.gif', xflip=True, tick=29,                ),  # noqa
            Frame(f'{subdir}/protegeH.gif',  xflip=True, tick=33,                 dx=-CHAR_W              ),  # noqa
            Frame(f'{subdir}/cou2.gif',      xflip=True, tick=39,                 dx=-CHAR_W + 2 * SCALE_X),  # noqa
            Frame(f'{subdir}/cou3.gif',      xflip=True, tick=51,                 dx=-4 * CHAR_W          ),  # noqa
            Frame(f'{subdir}/cou2.gif',      xflip=True, tick=60,                 dx=-CHAR_W + 3 * SCALE_X),  # noqa
            # @formatter:on
        ]),
        'front': Animation(frames=[
            # @formatter:off
            Frame(f'{subdir}/front1.gif', xflip=True, tick=5,  dx=-CHAR_W + 1 * SCALE_X, post_action=Actions.snd('epee.ogg')),  # noqa
            Frame(f'{subdir}/front2.gif', xflip=True, tick=23, dx=-CHAR_W              ),  # noqa
            Frame(f'{subdir}/front3.gif', xflip=True, tick=30, dx=-3 * CHAR_W          ),  # noqa
            Frame(f'{subdir}/front2.gif', xflip=True, tick=46, dx=-CHAR_W              ),  # noqa
            # @formatter:on
        ]),
        'retourne': Animation(frames=[
            Frame(f'{subdir}/retourne1.gif', xflip=True, tick=5,  mv=(-CHAR_W, 0)),
            Frame(f'{subdir}/retourne2.gif', xflip=True, tick=10, mv=(-CHAR_W, 0)),
            Frame(f'{subdir}/retourne3.gif', xflip=True, tick=18, mv=(-CHAR_W, 0)),
        ]),
        'vainqueur': Animation(frames=[
            # @formatter:off
            Frame(f'{subdir}/vainqueur1.gif', xflip=True, tick=18,  dx=-CHAR_W),
            Frame(f'{subdir}/vainqueur2.gif', xflip=True, tick=35,  dx=-CHAR_W),
            Frame(f'{subdir}/vainqueur3.gif', xflip=True, tick=85,  dx=-CHAR_W),
            Frame(f'{subdir}/vainqueur2.gif', xflip=True, tick=100, dx=-CHAR_W),
            Frame(f'{subdir}/vainqueur1.gif', xflip=True, tick=101, dx=-CHAR_W, post_action=Actions.stop),
            # @formatter:on
        ]),
        'vainqueurKO': Animation(frames=[
            # @formatter:off
            Frame(f'{subdir}/retourne1.gif',  xflip=True, tick=15),  # noqa
            Frame(f'{subdir}/retourne2.gif',  xflip=True, tick=23),  # noqa
            Frame(f'{subdir}/retourne3.gif',  xflip=True, tick=30),  # noqa
            Frame(f'{subdir}/debout.gif',     xflip=True, tick=40),  # noqa
            Frame(f'{subdir}/marche3.gif',                tick=40),  # noqa optional frame, see gestion on tick 35
            Frame(f'{subdir}/marche3.gif',    xflip=True, tick=40),  # noqa optional frame, see gestion on tick 35
            Frame(f'{subdir}/debout.gif',     xflip=True, tick=55),  # noqa
            Frame(f'{subdir}/pied1.gif',      xflip=True, tick=70,  dx=-CHAR_W),  # noqa
            Frame(f'{subdir}/pied2.gif',      xflip=True, tick=75,  dx=-CHAR_W),  # noqa
            Frame(f'{subdir}/pied1.gif',      xflip=True, tick=100, dx=-CHAR_W),  # noqa
            Frame(f'{subdir}/debout.gif',     xflip=True, tick=105),  # noqa
            Frame(f'{subdir}/vainqueur1.gif', xflip=True, tick=123, dx=-CHAR_W),  # noqa
            Frame(f'{subdir}/vainqueur2.gif', xflip=True, tick=140, dx=-CHAR_W),  # noqa
            Frame(f'{subdir}/vainqueur3.gif', xflip=True, tick=195, dx=-CHAR_W),  # noqa
            Frame(f'{subdir}/vainqueur2.gif', xflip=True, tick=205, dx=-CHAR_W),  # noqa
            Frame(f'{subdir}/vainqueur1.gif', xflip=True, tick=231, dx=-CHAR_W, post_action=Actions.stop),
            # @formatter:oon
        ]),
        'touche1': Animation(frames=[
            # @formatter:off
            Frame(f'{subdir}/touche2.gif', xflip=True, tick=1),
            Frame(f'{subdir}/touche2.gif', xflip=True, tick=5,  mv=(CHAR_W,     0)),  # noqa
            Frame(f'{subdir}/touche1.gif', xflip=True, tick=10, mv=(2 * CHAR_W, 0)),  # noqa
            Frame(f'{subdir}/touche2.gif', xflip=True, tick=20, mv=(CHAR_W,     0)),  # noqa
            Frame(f'{subdir}/debout.gif',  xflip=True, tick=21),
            # @formatter:on
        ]),
        'tombe1': Animation(frames=[
            # @formatter:off
            Frame(f'{subdir}/tombe1.gif', xflip=True, tick=1,                  dx=CHAR_W),  # noqa
            Frame(f'{subdir}/tombe1.gif', xflip=True, tick=9,  mv=(CHAR_W, 0), dx=CHAR_W),  # noqa
            Frame(f'{subdir}/tombe2.gif', xflip=True, tick=15, mv=(CHAR_W, 0), dx=CHAR_W),  # noqa
            Frame(f'{subdir}/tombe3.gif', xflip=True, tick=25,                 dx=CHAR_W),  # noqa
            Frame(f'{subdir}/debout.gif', xflip=True, tick=27, mv=(CHAR_W, 0)),
            # @formatter:on
        ]),
        'mort': Animation(frames=[
            # @formatter:off
            Frame(f'{subdir}/assis1.gif', xflip=True, tick=15, pre_action=Actions.snd('mortKO.ogg')),
            Frame(f'{subdir}/mort2.gif',  xflip=True, tick=17, dx=-1 * CHAR_W, post_action=Actions.stop),
            Frame(f'{subdir}/mort3.gif',  xflip=True, tick=18),  # manual, see vainqueurKO
            Frame(f'{subdir}/mort4.gif',  xflip=True, tick=19),  # manual, see vainqueurKO
            # @formatter:on
        ]),
        'mortdecap': Animation(frames=[
            # @formatter:off
            Frame(f'{subdir}/decap1.gif', xflip=True, tick=35, dx=-1 * CHAR_W, pre_action=Actions.snd('mortdecap.ogg')),
            Frame(f'{subdir}/decap2.gif', xflip=True, tick=70, dx=-3 * CHAR_W),
            Frame(f'{subdir}/decap3.gif', xflip=True, tick=80, dx=-4 * CHAR_W),
            Frame(f'{subdir}/decap4.gif', xflip=True, tick=82, dx=-5 * CHAR_W, post_action=Actions.stop),
            # @formatter:on
        ]),
        'mortgnome': Animation(frames=[
            Frame(f'{subdir}/mort4.gif', xflip=True, tick=0, mv=(CHAR_W / 12, 0)),
        ]),
        'mortdecapgnome': Animation(frames=[
            Frame(f'{subdir}/decap4.gif', xflip=True, tick=0, mv=(CHAR_W / 12, 0)),
        ]),
        'mortSORCIER': Animation(frames=[
            # @formatter:off
            Frame(f'{subdir}/assis1.gif', xflip=True, tick=15),
            Frame(f'{subdir}/mort2.gif',  xflip=True, tick=70, dx=-1 * CHAR_W),
            Frame(f'{subdir}/mort3.gif',  xflip=True, tick=85),
            Frame(f'{subdir}/mort4.gif',  xflip=True, tick=87, post_action=Actions.stop),
            # @formatter:on
        ]),
    }


def gnome():
    return {
        'gnome': Animation(frames=[
            Frame('sprites/gnome1.gif', tick=6, mv=(CHAR_W, 0)),
            Frame('sprites/gnome2.gif', tick=12),
            Frame('sprites/gnome3.gif', tick=18, mv=(CHAR_W, 0)),
            Frame('sprites/gnome4.gif', tick=24),
        ]),
    }


def feu():
    return {
        'feu_low': Animation(frames=[
            # @formatter:off
            Frame('empty',            tick=55),  # loc 7
            Frame('sprites/feu1.gif', tick=56, mv=(7    * CHAR_W, 0   * CHAR_H), colorkey=(255, 0, 255)),  # noqa loc 14,    16.0
            Frame('sprites/feu1.gif', tick=57, mv=(0.75 * CHAR_W, 0.5 * CHAR_H), colorkey=(255, 0, 255)),  # noqa loc 14.75, 16.5
            Frame('sprites/feu1.gif', tick=58, mv=(0.75 * CHAR_W, 0.5 * CHAR_H), colorkey=(255, 0, 255)),  # noqa loc 15.5,  17.0
            Frame('sprites/feu1.gif', tick=59, mv=(0.75 * CHAR_W, 0.5 * CHAR_H), colorkey=(255, 0, 255)),  # noqa loc 16.25, 17.5
            Frame('sprites/feu1.gif', tick=60, mv=(0.75 * CHAR_W, 0.5 * CHAR_H), colorkey=(255, 0, 255)),  # noqa loc 17.0,  18.0
            Frame('sprites/feu2.gif', tick=61, mv=(0.75 * CHAR_W, 0.5 * CHAR_H), colorkey=(255, 0, 255)),  # noqa loc 17.75, 18.5
            Frame('sprites/feu2.gif', tick=62, mv=(0.75 * CHAR_W, 0.5 * CHAR_H), colorkey=(255, 0, 255)),  # noqa loc 18.5,  19.0
            Frame('sprites/feu2.gif', tick=63, mv=(0.75 * CHAR_W, 0.5 * CHAR_H), colorkey=(255, 0, 255)),  # noqa loc 19.25, 19.5
            Frame('sprites/feu2.gif', tick=65, mv=(0.75 * CHAR_W, 0.5 * CHAR_H), colorkey=(255, 0, 255)),  # noqa loc 20.0,  20.0
            Frame('sprites/feu3.gif', tick=66, mv=(0.75 * CHAR_W, 0   * CHAR_H), colorkey=(255, 0, 255)),  # noqa loc 20.75
            Frame('sprites/feu3.gif', tick=67, mv=(0.75 * CHAR_W, 0   * CHAR_H), colorkey=(255, 0, 255)),  # noqa loc 21.5
            Frame('sprites/feu3.gif', tick=68, mv=(0.75 * CHAR_W, 0   * CHAR_H), colorkey=(255, 0, 255)),  # noqa loc 22.25
            Frame('sprites/feu3.gif', tick=70, mv=(0.75 * CHAR_W, 0   * CHAR_H), colorkey=(255, 0, 255)),  # noqa loc 23.0
            Frame('sprites/feu1.gif', tick=71, mv=(0.75 * CHAR_W, 0   * CHAR_H), colorkey=(255, 0, 255)),  # noqa loc 23.75
            Frame('sprites/feu1.gif', tick=72, mv=(0.75 * CHAR_W, 0   * CHAR_H), colorkey=(255, 0, 255)),  # noqa loc 24.5
            Frame('sprites/feu1.gif', tick=73, mv=(0.75 * CHAR_W, 0   * CHAR_H), colorkey=(255, 0, 255)),  # noqa loc 25.25
            Frame('sprites/feu1.gif', tick=75, mv=(0.75 * CHAR_W, 0   * CHAR_H), colorkey=(255, 0, 255)),  # noqa loc 26.0
            Frame('sprites/feu2.gif', tick=76, mv=(0.75 * CHAR_W, 0   * CHAR_H), colorkey=(255, 0, 255)),  # noqa loc 26.75
            Frame('sprites/feu2.gif', tick=77, mv=(0.75 * CHAR_W, 0   * CHAR_H), colorkey=(255, 0, 255)),  # noqa loc 27.5
            Frame('sprites/feu2.gif', tick=78, mv=(0.75 * CHAR_W, 0   * CHAR_H), colorkey=(255, 0, 255)),  # noqa loc 28.25
            Frame('sprites/feu2.gif', tick=80, mv=(0.75 * CHAR_W, 0   * CHAR_H), colorkey=(255, 0, 255)),  # noqa loc 29.0
            Frame('sprites/feu3.gif', tick=81, mv=(0.75 * CHAR_W, 0   * CHAR_H), colorkey=(255, 0, 255)),  # noqa loc 29.75
            Frame('sprites/feu3.gif', tick=82, mv=(0.75 * CHAR_W, 0   * CHAR_H), colorkey=(255, 0, 255)),  # noqa loc 30.5
            Frame('sprites/feu3.gif', tick=83, mv=(0.75 * CHAR_W, 0   * CHAR_H), colorkey=(255, 0, 255)),  # noqa loc 31.25
            Frame('sprites/feu3.gif', tick=85, mv=(0.75 * CHAR_W, 0   * CHAR_H), colorkey=(255, 0, 255)),  # noqa loc 32.0
            Frame('sprites/feu1.gif', tick=86, mv=(0.75 * CHAR_W, 0   * CHAR_H), colorkey=(255, 0, 255)),  # noqa loc 32.75
            Frame('sprites/feu1.gif', tick=87, mv=(0.75 * CHAR_W, 0   * CHAR_H), colorkey=(255, 0, 255)),  # noqa loc 33.5
            Frame('sprites/feu1.gif', tick=88, mv=(0.75 * CHAR_W, 0   * CHAR_H), colorkey=(255, 0, 255)),  # noqa loc 34.25
            Frame('sprites/feu1.gif', tick=89, mv=(0.75 * CHAR_W, 0   * CHAR_H), colorkey=(255, 0, 255)),  # noqa loc 35.0
            Frame('sprites/feu1.gif', tick=90, mv=(0.75 * CHAR_W, 0   * CHAR_H), colorkey=(255, 0, 255)),  # noqa
            Frame('sprites/feu1.gif', tick=91, mv=(0.75 * CHAR_W, 0   * CHAR_H), colorkey=(255, 0, 255)),  # noqa
            Frame('sprites/feu1.gif', tick=92, mv=(0.75 * CHAR_W, 0   * CHAR_H), colorkey=(255, 0, 255), post_action=Actions.kill),  # noqa
            # @formatter:on
        ]),
        'feu_high': Animation(frames=[
            # @formatter:off
            Frame('empty',            tick=135),  # loc 7
            Frame('sprites/feu1.gif', tick=136, mv=(7    * CHAR_W, 0), colorkey=(255, 0, 255)),  # noqa loc 14,
            Frame('sprites/feu1.gif', tick=137, mv=(0.75 * CHAR_W, 0), colorkey=(255, 0, 255)),  # noqa loc 14.75,
            Frame('sprites/feu1.gif', tick=138, mv=(0.75 * CHAR_W, 0), colorkey=(255, 0, 255)),  # noqa loc 15.5,
            Frame('sprites/feu1.gif', tick=139, mv=(0.75 * CHAR_W, 0), colorkey=(255, 0, 255)),  # noqa loc 16.25,
            Frame('sprites/feu1.gif', tick=140, mv=(0.75 * CHAR_W, 0), colorkey=(255, 0, 255)),  # noqa loc 17.0,
            Frame('sprites/feu2.gif', tick=141, mv=(0.75 * CHAR_W, 0), colorkey=(255, 0, 255)),  # noqa loc 17.75,
            Frame('sprites/feu2.gif', tick=142, mv=(0.75 * CHAR_W, 0), colorkey=(255, 0, 255)),  # noqa loc 18.5,
            Frame('sprites/feu2.gif', tick=143, mv=(0.75 * CHAR_W, 0), colorkey=(255, 0, 255)),  # noqa loc 19.25,
            Frame('sprites/feu2.gif', tick=145, mv=(0.75 * CHAR_W, 0), colorkey=(255, 0, 255)),  # noqa loc 20.0,
            Frame('sprites/feu3.gif', tick=146, mv=(0.75 * CHAR_W, 0), colorkey=(255, 0, 255)),  # noqa loc 20.75
            Frame('sprites/feu3.gif', tick=147, mv=(0.75 * CHAR_W, 0), colorkey=(255, 0, 255)),  # noqa loc 21.5
            Frame('sprites/feu3.gif', tick=148, mv=(0.75 * CHAR_W, 0), colorkey=(255, 0, 255)),  # noqa loc 22.25
            Frame('sprites/feu3.gif', tick=150, mv=(0.75 * CHAR_W, 0), colorkey=(255, 0, 255)),  # noqa loc 23.0
            Frame('sprites/feu1.gif', tick=151, mv=(0.75 * CHAR_W, 0), colorkey=(255, 0, 255)),  # noqa loc 23.75
            Frame('sprites/feu1.gif', tick=152, mv=(0.75 * CHAR_W, 0), colorkey=(255, 0, 255)),  # noqa loc 24.5
            Frame('sprites/feu1.gif', tick=153, mv=(0.75 * CHAR_W, 0), colorkey=(255, 0, 255)),  # noqa loc 25.25
            Frame('sprites/feu1.gif', tick=155, mv=(0.75 * CHAR_W, 0), colorkey=(255, 0, 255)),  # noqa loc 26.0
            Frame('sprites/feu2.gif', tick=156, mv=(0.75 * CHAR_W, 0), colorkey=(255, 0, 255)),  # noqa loc 26.75
            Frame('sprites/feu2.gif', tick=157, mv=(0.75 * CHAR_W, 0), colorkey=(255, 0, 255)),  # noqa loc 27.5
            Frame('sprites/feu2.gif', tick=158, mv=(0.75 * CHAR_W, 0), colorkey=(255, 0, 255)),  # noqa loc 28.25
            Frame('sprites/feu2.gif', tick=160, mv=(0.75 * CHAR_W, 0), colorkey=(255, 0, 255)),  # noqa loc 29.0
            Frame('sprites/feu3.gif', tick=161, mv=(0.75 * CHAR_W, 0), colorkey=(255, 0, 255)),  # noqa loc 29.75
            Frame('sprites/feu3.gif', tick=162, mv=(0.75 * CHAR_W, 0), colorkey=(255, 0, 255)),  # noqa loc 30.5
            Frame('sprites/feu3.gif', tick=163, mv=(0.75 * CHAR_W, 0), colorkey=(255, 0, 255)),  # noqa loc 31.25
            Frame('sprites/feu3.gif', tick=165, mv=(0.75 * CHAR_W, 0), colorkey=(255, 0, 255)),  # noqa loc 32.0
            Frame('sprites/feu1.gif', tick=166, mv=(0.75 * CHAR_W, 0), colorkey=(255, 0, 255)),  # noqa loc 32.75
            Frame('sprites/feu1.gif', tick=167, mv=(0.75 * CHAR_W, 0), colorkey=(255, 0, 255)),  # noqa loc 33.5
            Frame('sprites/feu1.gif', tick=168, mv=(0.75 * CHAR_W, 0), colorkey=(255, 0, 255)),  # noqa loc 34.25
            Frame('sprites/feu1.gif', tick=169, mv=(0.75 * CHAR_W, 0), colorkey=(255, 0, 255)),  # noqa loc 35.0
            Frame('sprites/feu1.gif', tick=170, mv=(0.75 * CHAR_W, 0), colorkey=(255, 0, 255)),  # noqa
            Frame('sprites/feu1.gif', tick=171, mv=(0.75 * CHAR_W, 0), colorkey=(255, 0, 255)),  # noqa
            Frame('sprites/feu1.gif', tick=172, mv=(0.75 * CHAR_W, 0), colorkey=(255, 0, 255), post_action=Actions.kill),  # noqa
            # @formatter:on
        ]),
    }


def sorcier():
    return {
        'debout': Animation(frames=[
            Frame('sprites/drax1.gif'),
        ]),
        'attaque': Animation(frames=[
            Frame('sprites/drax1.gif', tick=50),
            Frame('sprites/drax2.gif', tick=60),
            Frame('sprites/drax1.gif', tick=130),
            Frame('sprites/drax2.gif', tick=140),
            Frame('sprites/drax1.gif', tick=141),
        ], actions=[
            Act(tick=50, act=Actions.snd('feu.ogg')),
            Act(tick=130, act=Actions.snd('feu.ogg')),
            Act(tick=141, act=Actions.stop),
        ]),
    }
