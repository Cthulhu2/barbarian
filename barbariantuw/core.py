from dataclasses import dataclass, field
from math import ceil
from os.path import join
from typing import Dict, Callable, TypedDict, Tuple, List, Optional, Iterator

from pygame import Surface, image, Sound, Rect, Font
from pygame.sprite import Group, AbstractGroup, DirtySprite
from pygame.time import get_ticks
from pygame.transform import scale, rotate, flip

from barbariantuw import IMG_PATH, Game, SND_PATH, OPTS, FONT, Theme

img_cache: Dict[int, Surface] = {}
snd_cache: Dict[int, Sound] = {}


def get_img(name, w: float = 0, h: float = 0, angle: float = 0, xflip=False,
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
        img = scale(img, (ceil(w * Game.scx), ceil(h * Game.scy)))
    else:
        img = scale(img, (ceil(img.get_width() * Game.scx),
                          ceil(img.get_height() * Game.scy)))
    if angle != 0:
        img = rotate(img, angle)
    if xflip:
        img = flip(img, xflip, False)
    img_cache[key_] = img
    return img


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


def snd_stop(name: str):
    if name and OPTS.sound:
        get_snd(name).stop()


Action = Callable[['AnimatedSprite'], None]
Action2 = Callable[['AnimatedSprite', TypedDict], None]


@dataclass(slots=True, frozen=True)
class Frame:
    """
    `tick` end tick. A next tick will apply a next frame.
    """
    name: str
    dx: float = 0
    dy: float = 0
    w: float = 0
    h: float = 0
    duration: int = 125
    angle: float = 0
    xflip: bool = False
    fill: Tuple[int, int, int] = None  # import pygame.typing.ColorLike breaks WASM!!!
    blend_flags: int = 0
    mv: Tuple[float, float] = None
    pre_action: Action = None
    post_action: Action = None
    tick: int = -1
    colorkey: Tuple[int, int, int] = None
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
                     self.pre_action, self.post_action, self.tick, self.colorkey)


class Act:
    __slots__ = ['act', 'tick', 'kwargs']

    def __init__(self, *, tick: int = -1, act: Action | Action2 = None, **kwargs):
        self.act = act
        self.tick = tick
        self.kwargs = kwargs


@dataclass(slots=True, frozen=True)
class Animation:
    frames: List[Frame]
    actions: List[Act] = None


class Actions:

    @staticmethod
    def kill(sprite):
        sprite.kill()

    @staticmethod
    def stop(sprite):
        sprite.stopped = True

    # noinspection PyUnusedLocal
    @staticmethod
    def snd(sprite, snd: str = None):
        snd_play(snd)

    @staticmethod
    def val(sprite, **kwargs):
        for k, v in kwargs:
            setattr(sprite, k, v)


def rtl_anims(animations: Dict[str, Animation]):
    rtl = {}
    for name, anim in animations.items():
        rtl[name] = Animation(frames=[f.rtl() for f in anim.frames],
                              actions=anim.actions)
    return rtl


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
                 pos: Tuple[int, int] = (0, 0),
                 *groups,
                 fnt: str = FONT,
                 cached: bool = True,
                 bgcolor: Tuple[int, int, int] = None):
        super().__init__(*groups)
        self._x = pos[0]
        self._y = pos[1]
        self._msg = msg
        self._size = size
        self._font = fnt
        self._color = color
        self._bgcolor = bgcolor
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
            img = font_.render(str(self.msg), True, self._color, self._bgcolor)
            rect = img.get_rect(topleft=(self._x, self._y))
        else:
            key_ = font_key + hash(self.msg) + hash(self._color)
            if key_ in Txt.cache:
                img = Txt.cache[key_]
            else:
                img = font_.render(str(self.msg), True, self._color, self._bgcolor)
                Txt.cache[key_] = img
            rect = img.get_rect(topleft=(self._x, self._y))
        return img, rect


class StaticSprite(DirtySprite):
    def __init__(self,
                 pos: Tuple[int, int],
                 img: str,
                 w=0, h=0, fill=None,
                 color: Tuple[int, int, int] = None,
                 *groups: AbstractGroup):
        super().__init__(*groups)
        self.image = get_img(img, w=w, h=h, fill=fill, color=color)
        self.rect = self.image.get_rect()
        self.rect.move_ip(pos[0], pos[1])


class AnimatedSprite(DirtySprite):
    actions: Optional[Iterator[Act]] = None
    act: Optional[Act] = None
    actTick: int = 0

    def __init__(self,
                 topleft: Tuple[float, float],
                 animations: Dict[str, Animation],
                 *groups):
        super().__init__(*groups)
        self.anims = animations
        self.animTimer = get_ticks()
        self.animTick = 0
        self._speed = 1.0
        self._stopped = False

        self.anim = next(iter(self.anims))
        self.frames = self.anims[self.anim].frames
        self.frameNum = 0
        self.frame = self.frames[self.frameNum]
        self.frame_duration = self.frame.duration
        self.frame_tick = self.frame.tick

        self.image = self.frame.image
        self.rect = Rect(0, 0, 0, 0)
        self._topleft = topleft
        self._update_rect()

        self.init_acts()

    def init_acts(self):
        self.actions = self.anims[self.anim].actions
        if self.actions:
            self.actions = iter(self.actions)
            self.act = next(self.actions)
            self.actTick = int(self._calc(self.act.tick))
        else:
            self.act = None
            self.actTick = 0

    def call_acts(self):
        while self.act and not self.stopped and self.animTick == self.actTick:
            if self.act.kwargs:
                self.act.act(self, **self.act.kwargs)
            else:
                self.act.act(self)
            self.act = next(self.actions, None)
            if self.act:
                self.actTick = self._calc(self.act.tick)
            else:
                self.actTick = 0

    @property
    def x(self) -> float:
        return self._topleft[0]

    @x.setter
    def x(self, x: float):
        if self._topleft[0] != x:
            self._topleft = (x, self._topleft[1])
            self._update_rect()

    @property
    def y(self) -> float:
        return self._topleft[1]

    @y.setter
    def y(self, y: float):
        if self._topleft[1] != y:
            self._topleft = (self._topleft[0], y)
            self._update_rect()

    @property
    def topleft(self) -> Tuple[float, float]:
        return self._topleft

    @topleft.setter
    def topleft(self, topleft: Tuple[float, float]):
        if self._topleft != topleft:
            self._topleft = topleft
            self._update_rect()

    @property
    def speed(self) -> float:
        return self._speed

    @speed.setter
    def speed(self, speed: float):
        self._speed = round(min(3.0, max(0.0, speed)), 3)
        self.frame_duration = self._calc(self.frame.duration)
        self.frame_tick = self._calc(self.frame.tick)

    @property
    def stopped(self) -> bool:
        return self._stopped

    @stopped.setter
    def stopped(self, stopped: bool):
        self._stopped = stopped

    def animate(self, anim: str, tick=0):
        if anim in self.anims:
            self.stopped = False
            self.anim = anim
            self.frames = self.anims[anim].frames
            self.animTimer = get_ticks()
            self.animTick = tick
            self.frameNum = -1
            self.frame = None
            self.next_frame()
            self.visible = True
            self.init_acts()
            self.call_acts()
        else:
            self.visible = False

    def set_frame(self, anim: str, frame: int = 0):
        if not self.stopped:
            self.stopped = True
        if not self.visible:
            self.visible = True
        if self.anim != anim:
            self.anim = anim
            self.frames = self.anims[anim].frames
            self.init_acts()
        self.frameNum = frame - 1
        self.next_frame()

    def update(self, current_time, *args):
        if not self.visible or self.stopped or self.speed <= 0:
            return
        self.animTick += 1
        self.call_acts()
        if self.frame.is_tickable:
            while not self.stopped and self.animTick > self.frame_tick:
                self.animTimer = current_time
                self.next_frame()
        else:
            passed = current_time - self.animTimer
            while not self.stopped and passed > self.frame_duration:
                # TODO: Rewind mixed frame types
                passed -= self.frame_duration
                self.animTimer = current_time
                self.next_frame()

    def _calc(self, time):
        if self.speed == 0 or self.speed == 1:
            return time
        else:
            return time / self.speed

    def prev_frame(self):
        self.frameNum -= 1
        if self.frameNum == -1:
            self.frameNum = len(self.frames) - 1

        prev = self.frames[self.frameNum]
        if self.frame != prev:
            if self.frame.post_action:
                self.frame.post_action(self)
            if self.frame.mv:  # Undo the current frame move_base
                self.move(-self.frame.mv[0], -self.frame.mv[1])
            self.frame = prev
            if self.frame.is_tickable:
                self.frame_tick = self._calc(self.frame.tick)
            else:
                self.frame_duration = self._calc(self.frame.duration)

            self.image = self.frame.image

            self._update_rect()
            if self.frame.pre_action:
                self.frame.pre_action(self)

    def next_frame(self):
        self.frameNum += 1
        if self.frameNum == len(self.frames):
            self.frameNum = 0
            self.animTick = 0
            self.init_acts()
        next_ = self.frames[self.frameNum]
        if self.frame != next_ or len(self.frames) == 1:
            if self.frame and self.frame.post_action and not self.stopped:
                cur_anim = self.anim
                self.frame.post_action(self)
                if cur_anim != self.anim or self.stopped:
                    # Animation changed or stopped, don't process next frame
                    return

            self.frame = next_
            if self.frame.is_tickable:
                self.frame_tick = self._calc(self.frame.tick)
            else:
                self.frame_duration = self._calc(self.frame.duration)
            self.image = self.frame.image
            if self.frame.mv:
                self.move(self.frame.mv[0], self.frame.mv[1])
            self._update_rect()
            if self.frame.pre_action:
                self.frame.pre_action(self)

    def _update_rect(self):
        self.rect.size = self.frame.rect.size
        self.rect.topleft = self.topleft
        self.rect.move_ip(self.frame.rect.x, self.frame.rect.y)
        self.dirty = 1

    def move(self, dx, dy):
        self.topleft = (self.topleft[0] + dx, self.topleft[1] + dy)
        self.rect.move_ip(dx, dy)
        self.dirty = 1
