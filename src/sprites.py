# -*- coding: utf-8 -*-
import enum
from os.path import join
from typing import Tuple, Dict

from pygame import Rect
from pygame.font import Font
from pygame.mixer import Sound
from pygame.sprite import DirtySprite, AbstractGroup, Group, LayeredDirty
from pygame.surface import Surface
from pygame.time import get_ticks
from pygame.transform import scale

import anims
from anims import get_img, rtl_anims
from settings import FONT, SND_PATH, Theme, CHAR_W

snd_cache: Dict[int, Sound] = {}


def get_snd(name: str) -> Sound:
    key_ = hash(name)

    if key_ in snd_cache:
        return snd_cache[key_]

    snd = Sound(join(SND_PATH, name))
    snd_cache[key_] = snd
    return snd


def px2loc(x: int) -> int:
    """
    Convert scaled pixel to character location X 40x25 (320x200 mode, 8x8 font).
    :param x: 0..959
    :return: 1..40
    """
    return int(x / CHAR_W + 1)


def loc2px(x: int) -> int:
    """
    Convert character location X 40x25 (320x200 mode, 8x8 font) to scaled pixel.
    :param x: 1..40
    :return:
    """
    return (x - 1) * CHAR_W


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
                 loc: Tuple[int, int] = (0, 0),
                 *groups,
                 fnt: str = FONT,
                 cached: bool = True,
                 bgcolor: Tuple[int, int, int] = None):
        super().__init__(*groups)
        self._x = loc[0]
        self._y = loc[1]
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
                 loc: Tuple[int, int],
                 img: str,
                 w=0, h=0, fill=None,
                 color: Tuple[int, int, int] = None,
                 *groups: AbstractGroup):
        super().__init__(*groups)
        self.image = get_img(img, w=w, h=h, fill=fill, color=color)
        self.rect = self.image.get_rect()
        self.rect.move_ip(loc[0], loc[1])


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
        if self.top_left[0] != x:
            self.dirty = 1
            self.top_left = (x, self.top_left[1])
            self._update_rect()

    @property
    def y(self) -> int:
        return self.top_left[1]

    @y.setter
    def y(self, y: int):
        if self.top_left[1] != y:
            self.dirty = 1
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
                while not self.is_stopped and passed > self.frame_duration:
                    # TODO: Rewind mixed frame types
                    passed -= self.frame_duration
                    self.animTimer = current_time
                    self.next_frame()
            else:
                while not self.is_stopped and self.animTick > self.frame_tick:
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
        elif action == 'kill':
            self.kill()

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
            self.animTick = 1
        next_ = self.frames[self.frameNum]
        if self.frame != next_ or len(self.frames) == 1:
            if self.frame and self.frame.post_action and not self.is_stopped:
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


YF = 16
YT = 17
YM = 19
YG = 21


class Barbarian(AnimatedSprite):
    xF: int = 0
    xT: int = 0
    xM: int = 0
    xG: int = 0

    def __init__(self, opts, x, y, subdir: str, rtl=False, anim='debout'):
        super().__init__((x, y), anims.barb(subdir))
        self.opts = opts
        self.rtl = rtl
        #
        self.sangSprite = AnimatedSprite(self.top_left,
                                         anims.sang_decap())
        self.teteSprite = AnimatedSprite(self.top_left,
                                         anims.tete_decap(subdir))
        self.teteOmbreSprite = AnimatedSprite(self.top_left,
                                              anims.teteombre_decap())
        self.ltr_anims = self.anims
        self.rtl_anims = anims.barb_rtl(subdir)
        self.anims = self.rtl_anims if rtl else self.ltr_anims
        self.animate(anim)
        #
        self.clavierX = 7
        self.clavierY = 7
        self.attaque = False
        #
        self.xLocPrev = 0  # x_loc at the begin of frame
        self.yAtt = 17
        self.xAtt = 27 if rtl else 15
        self.yF = YF  # front
        self.yT = YT  # tete
        self.yM = YM  # corps
        self.yG = YG  # genou
        self.reset_xX_front()
        #
        self.reftemps = 0
        self.attente = 1
        self.vie = 12
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
        self.decapite = False
        self.pressedUp = False
        self.pressedDown = False
        self.pressedLeft = False
        self.pressedRight = False
        self.pressedFire = False

    def recule_levier(self):
        return Levier.droite if self.rtl else Levier.gauche

    def avance_levier(self):
        return Levier.gauche if self.rtl else Levier.droite

    def snd_play(self, snd: str):
        if snd and self.opts.sound:
            get_snd(snd).play()

    def reset_xX(self, offset):
        self.xF = self.x_loc() + offset
        self.xT = self.xF
        self.xM = self.xF
        self.xG = self.xF

    def reset_xX_front(self):
        self.reset_xX(0 if self.rtl else 4)

    def reset_xX_back(self):
        self.reset_xX(4 if self.rtl else 0)

    def reset_yX(self):
        self.yF = YF
        self.yT = YT
        self.yM = YM
        self.yG = YG

    def x_loc(self):
        return px2loc(self.x)

    def degat(self, opponent: 'Barbarian'):
        ltr = not self.rtl and self.x_loc() < opponent.x_loc()
        rtl = self.rtl and self.x_loc() > opponent.x_loc()
        yAtt = opponent.yAtt
        xAtt = opponent.xAtt
        if yAtt == self.yF and (ltr and xAtt <= self.xF
                                or rtl and xAtt >= self.xF):
            if self.state == State.protegeH:
                self.state = State.clingH
            else:
                self.state = State.tombe
                self.infoDegatF += 1
            return True, 0

        if yAtt == self.yT and (ltr and xAtt <= self.xT
                                or rtl and xAtt >= self.xT):
            if opponent.state == State.coupdetete:
                self.state = State.tombe
            else:
                self.state = State.touche
                self.infoDegatT += 1
            return True, 250

        if yAtt == self.yM and (ltr and xAtt <= self.xM
                                or rtl and xAtt >= self.xM):
            if self.state == State.protegeD:
                self.state = State.clingD
            else:
                self.state = State.touche
            return True, 250

        if yAtt == self.yG and (ltr and xAtt <= self.xG
                                or rtl and xAtt >= self.xG):
            if opponent.state in (State.araignee, State.rouladeAV):
                self.state = State.tombe
            elif self.state == State.protegeD:
                self.state = State.clingD
            elif opponent.state == State.coupdepied:
                self.state = State.tombe
                self.infoDegatG += 1
            else:
                self.state = State.touche
                self.infoDegatG += 1
            return True, 100
        return False, 0

    def turn_around(self, rtl):
        self.anims = self.rtl_anims if rtl else self.ltr_anims
        self.frames = self.anims[self.anim]
        self.frame = self.frames[self.frameNum]
        self.rtl = rtl
        self._update_rect()
        self.dirty = 1

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
    def action(self, temps):
        self.attente = 1

        # droite, gauche, decapite, devant
        if self.levier == Levier.droite:
            self.action_moveX(temps, self.rtl)

        elif self.levier == Levier.gauche:
            self.action_moveX(temps, not self.rtl)

        # saute, attaque cou
        elif self.levier == Levier.haut:
            self.action_haut(temps)

        # assis, attaque genou
        elif self.levier == Levier.bas:
            self.action_bas(temps)

        # roulade AV, coup de pied
        elif self.levier == Levier.basD:
            self.action_basX(temps, self.rtl)

        # roulade AR, coup sur front
        elif self.levier == Levier.basG:
            self.action_basX(temps, not self.rtl)

        # protection Haute, araignee
        elif self.levier == Levier.hautG:
            self.action_hautX(temps, not self.rtl)

        # protection devant, coup de tete
        elif self.levier == Levier.hautD:
            self.action_hautX(temps, self.rtl)

    def action_moveX(self, temps, recule):
        if recule:
            self.protegeH = False
            state, attack = State.recule, State.decapite
        else:
            self.protegeD = False
            state, attack = State.avance, State.devant
        if self.state == state:
            return
        self.state = state
        self.reftemps = temps
        if self.attaque:
            self.occupe_state(attack, temps)

    def action_haut(self, temps):
        self.protegeD = False
        self.protegeH = False
        self.occupe_state(State.saute, temps)

    def action_hautX(self, temps, recule):
        if recule:
            if self.protegeH:
                self.state = State.protegeH
                return
            self.occupe_state(State.protegeH1, temps)
            if self.attaque:
                self.occupe_state(State.araignee, temps)
        else:
            if self.protegeD:
                self.state = State.protegeD
                return
            self.occupe_state(State.protegeD1, temps)
            if self.attaque:
                self.occupe_state(State.coupdetete, temps)

    def action_bas(self, temps):
        if self.assis:
            self.state = State.assis2
            return
        self.occupe_state(State.assis, temps)

    def action_basX(self, temps, recule):
        if recule:
            self.occupe_state(State.rouladeAR, temps)
            if self.attaque:
                self.occupe_state(State.front, temps)
        else:
            self.occupe_state(State.rouladeAV, temps)
            if self.attaque:
                self.occupe_state(State.coupdepied, temps)

    # endregion actions

    # region gestions
    def gestion_attente(self, temps):
        self.reset_xX_front()
        if temps > self.reftemps + 50:
            self.occupe = False
            self.attente = 1
            self.state = State.debout
        elif temps == self.reftemps + 8:
            self.animate('attente', 8)
            self.snd_play('attente.ogg')

    def gestion_avance(self, temps, opponent: 'Barbarian',
                       soncling: iter, songrogne: iter):
        self.reset_xX_front()
        self.xAtt = self.x_loc() + (4 if self.rtl else 0)
        if self.attaque:
            self.occupe_state(State.devant, temps)
            self.gestion_devant(temps, opponent, soncling, songrogne)
        elif self.anim != 'avance':
            self.animate('avance')

    def gestion_recule(self, temps):
        self.reset_xX_front()
        self.xAtt = self.x_loc() + (4 if self.rtl else 0)
        if self.attaque:
            self.occupe_state(State.decapite, temps)
            self.gestion_decapite(temps)
        elif self.anim != 'recule':
            self.animate('recule')

    def gestion_saute(self, temps):
        self.xAtt = self.x_loc() + (4 if self.rtl else 0)
        self.reset_xX_front()
        self.decapite = False
        self.yG = self.yM
        self.yAtt = 14
        if self.attaque:
            self.occupe_state(State.cou, temps)
        elif temps > self.reftemps + 45:
            self.occupe = False
            self.state = State.debout
        elif temps > self.reftemps + 40:
            self.xM = self.x_loc() + (0 if self.rtl else 4)
            self.xG = self.x_loc() + (0 if self.rtl else 4)
        elif temps > self.reftemps + 30:
            self.xM = self.x_loc() + (0 if self.rtl else 4)
            self.xG = self.x_loc() + (3 if self.rtl else 1)
            self.decapite = True
        elif temps > self.reftemps + 13:
            self.xM = self.x_loc() + (3 if self.rtl else 1)
            self.xG = self.x_loc() + (3 if self.rtl else 1)
        elif temps > self.reftemps + 2:
            self.xM = self.x_loc() + (0 if self.rtl else 4)
            self.xG = self.x_loc() + (3 if self.rtl else 1)
        elif self.anim != 'saute':
            self.animate('saute')

    def gestion_assis(self, temps):
        self.xAtt = self.x_loc() + (4 if self.rtl else 0)
        self.xF = self.x_loc() + (4 if self.rtl else 0)
        self.xT = self.x_loc() + (4 if self.rtl else 0)
        self.xM = self.x_loc() + (4 if self.rtl else 0)
        self.xG = self.x_loc() + (0 if self.rtl else 4)
        self.yT = YM
        self.set_anim_frame('assis', 0)
        if temps > self.reftemps + 10:
            self.state = State.assis2

    def gestion_assis2(self, temps, opponent: 'Barbarian',
                       soncling: iter, songrogne: iter,
                       is_ai: bool):
        self.occupe = False
        self.assis = True
        self.xAtt = self.x_loc() + (4 if self.rtl else 0)
        self.xF = self.x_loc() + (4 if self.rtl else 0)
        self.xT = self.x_loc() + (4 if self.rtl else 0)
        self.xM = self.x_loc() + (0 if self.rtl else 4)
        self.xG = self.x_loc() + (0 if self.rtl else 4)
        self.set_anim_frame('assis', 1)
        if self.attaque and self.levier == Levier.bas:
            self.occupe_state(State.genou, temps)
            self.gestion_genou(temps, opponent, soncling, songrogne)
        elif is_ai and temps > self.reftemps + 20:
            self.occupe = False

    def gestion_releve(self, temps, opponent: 'Barbarian',
                       soncling: iter, songrogne: iter):
        self.xAtt = self.x_loc() + (4 if self.rtl else 0)
        self.yAtt = 14
        self.xF = self.x_loc() + (4 if self.rtl else 0)
        self.xT = self.x_loc() + (4 if self.rtl else 0)
        self.xM = self.x_loc() + (0 if self.rtl else 4)
        self.xG = self.x_loc() + (0 if self.rtl else 4)
        self.yT = YT
        self.set_anim_frame('releve', 0)
        if temps > self.reftemps + 10:
            self.state = State.debout
            self.occupe = False
        elif self.attaque and self.levier == Levier.bas:
            self.occupe_state(State.genou, temps)
            self.gestion_genou(temps, opponent, soncling, songrogne)

    def gestion_rouladeAV(self, temps, opponent):
        self.reset_xX_back()
        self.yG = YG
        self.yAtt = self.yG
        self.xAtt = self.x_loc() + (4 if self.rtl else 0)
        self.yT = self.yG
        if self.attaque:
            self.yT = YT
            self.occupe_state(State.coupdepied, temps)

        elif temps > self.reftemps + 38:
            self.xT = self.x_loc() + (0 if self.rtl else 4)
            self.xM = self.x_loc() + (0 if self.rtl else 4)
            self.yT = YT
            self.occupe = False
            # finderoulade
            jax = self.x_loc()
            jbx = opponent.x_loc()
            if (not self.rtl and jax >= jbx - 2) or (self.rtl and jax <= jbx + 2):
                self.occupe_state(State.retourne, temps)
                opponent.occupe_state(State.retourne, temps)
                self.yAtt = 14
                opponent.yAtt = 14
            else:
                self.state = State.debout
                self.xAtt = jax + (4 if self.rtl else 0)
                self.yAtt = 17
                self.reset_xX_front()
                self.reset_yX()

        elif temps > self.reftemps + 23:
            if self.anim == 'rouladeAV':
                if self.rtl:
                    distance = self.x_loc() - opponent.x_loc()
                else:
                    distance = opponent.x_loc() - self.x_loc()
                if 4 == distance:  # do not rollout at left half opponent
                    self.animate('rouladeAV-out', self.animTick)

        elif temps == self.reftemps + 18:
            if opponent.state in (State.tombe, State.tombe1):
                self.animate('rouladeAV-out', self.animTick)

        elif temps == self.reftemps + 17:
            self.xAtt = self.x_loc() + (-1 if self.rtl else 5)

        elif temps == self.reftemps + 15:
            if opponent.state in (State.tombe, State.tombe1):
                self.animate('rouladeAV-out', self.animTick)

        elif temps == self.reftemps + 14:
            self.xAtt = self.x_loc() + (-1 if self.rtl else 5)

        elif temps > self.reftemps + 10:
            pass  # do not update xM after reftemps+10
        elif temps > self.reftemps + 2:
            self.xM = self.x_loc() + (0 if self.rtl else 4)

        elif temps == self.reftemps + 2:
            self.xM = self.x_loc() + (0 if self.rtl else 4)
            self.snd_play('roule.ogg')
            self.animate('rouladeAV', 2)

    def gestion_rouladeAR(self, temps):
        self.reset_xX_back()
        self.yG = YG
        self.yAtt = self.yG
        self.xAtt = self.x_loc() + (4 if self.rtl else 0)
        if temps > self.reftemps + 33:
            self.xT = self.x_loc() + (0 if self.rtl else 4)
            self.xM = self.x_loc() + (0 if self.rtl else 4)
            self.occupe = False
            self.state = State.debout
        elif temps == self.reftemps + 2:
            self.snd_play('roule.ogg')
            self.animate('rouladeAR', 2)

    def gestion_protegeH1(self, temps):
        self.reset_xX_front()
        self.xAtt = self.x_loc() + (4 if self.rtl else 0)
        self.yG = YG
        if temps > self.reftemps + 5:
            self.protegeH = True
            self.state = State.protegeH
            self.occupe = False
        elif temps == self.reftemps + 2:
            self.snd_play('protege.ogg')
            self.animate('protegeH', 2)

    def gestion_protegeH(self, temps, opponent: 'Barbarian',
                         soncling: iter, songrogne: iter):
        self.reset_xX_front()
        self.xAtt = self.x_loc() + (4 if self.rtl else 0)
        self.yG = YG
        self.set_anim_frame('protegeH', 1)
        if self.attaque:
            self.occupe_state(State.araignee, temps)
            self.gestion_araignee(temps, opponent, soncling, songrogne)

    def gestion_protegeD1(self, temps):
        self.xAtt = self.x_loc() + (4 if self.rtl else 0)
        self.yG = YG
        self.reset_xX_front()
        self.decapite = False
        self.set_anim_frame('protegeD', 0)
        if self.attaque:
            self.occupe_state(State.coupdetete, temps)
            self.gestion_coupdetete(temps)
        elif temps > self.reftemps + 5:
            self.state = State.protegeD
            self.protegeD = True
            self.occupe = False
        elif temps == self.reftemps + 2:
            self.snd_play('protege.ogg')

    def gestion_protegeD(self, temps):
        self.xAtt = self.x_loc() + (4 if self.rtl else 0)
        self.yG = YG
        self.reset_xX_front()
        self.decapite = False
        self.set_anim_frame('protegeD', 1)
        if self.attaque:
            self.occupe_state(State.coupdetete, temps)
            self.gestion_coupdetete(temps)

    def gestion_cou(self, temps, opponent: 'Barbarian',
                    soncling: iter, songrogne: iter):
        self.reset_xX_front()
        self.yG = YG
        self.yT = YT
        self.yAtt = YT
        if temps > self.reftemps + 45:
            self.occupe = False
            self.state = State.debout

        elif temps > self.reftemps + 31:
            self.xAtt = self.x_loc() + (4 if self.rtl else 0)

        elif temps == self.reftemps + 31:
            if (opponent.state == State.cou
                    and abs(self.x_loc() - opponent.x_loc()) < 12
                    and (30 < temps - opponent.reftemps <= 45)):
                # do not attack in same state
                # cycle and play cling-sound once (for one player only)
                if not self.rtl:
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

        self.reset_xX_front()
        self.yG = YG
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
        self.xM = self.x_loc() + (0 if self.rtl else 4)
        self.xG = self.x_loc() + (0 if self.rtl else 4)
        self.yG = YG
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
        self.yAtt = YM
        self.xAtt = self.x_loc() + (4 if self.rtl else 0)
        self.yG = YG
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
                self.xAtt = self.x_loc() + (-2 if self.rtl else 6)

        elif temps > self.reftemps + 12:
            self.xAtt = self.x_loc() + (4 if self.rtl else 0)

        elif temps == self.reftemps + 7:
            self.snd_play(next(songrogne))
            self.snd_play('epee.ogg')
            self.xAtt = self.x_loc()

        elif temps == self.reftemps:
            self.animate('araignee')

    def gestion_coupdepied(self, temps, opponent):
        self.reset_xX_front()
        self.xF = self.x_loc() + 2
        self.xT = self.x_loc() + 2
        self.yAtt = self.yM
        self.yM = YM
        if temps > self.reftemps + 50:
            self.occupe = False
            self.state = State.debout
            self.xF = self.x_loc() + (0 if self.rtl else 4)
            self.xT = self.x_loc() + (0 if self.rtl else 4)
        elif temps > self.reftemps + 30:
            self.xM = self.x_loc() + (0 if self.rtl else 4)
        elif temps > self.reftemps + 10:
            self.xG = self.x_loc() + (3 if self.rtl else 1)
            self.xM = self.x_loc() + (0 if self.rtl else 4)
            self.xAtt = self.x_loc() + (4 if self.rtl else 0)
        elif temps > self.reftemps + 9:
            self.xM = self.x_loc() + (4 if self.rtl else 0)
            if opponent.state == State.coupdepied and (7 < temps - opponent.reftemps < 11):
                pass  # do no attack
            else:
                self.xAtt = self.x_loc() + (-1 if self.rtl else 5)
        elif temps > self.reftemps + 1:
            self.xM = self.x_loc() + (0 if self.rtl else 4)
        elif temps == self.reftemps:
            self.animate('coupdepied')

    def gestion_coupdetete(self, temps):
        self.reset_xX_front()
        self.yG = YG
        if temps > self.reftemps + 37:
            self.occupe = False
            self.state = State.debout
        elif temps > self.reftemps + 20:
            self.xAtt = self.x_loc() + (4 if self.rtl else 0)
        elif temps > self.reftemps + 19:
            self.xAtt = self.x_loc() + (0 if self.rtl else 4)
        elif temps > self.reftemps + 18:
            self.xAtt = self.x_loc() + (4 if self.rtl else 0)
        elif temps > self.reftemps + 9:
            self.yAtt = self.yF
        elif temps == self.reftemps:
            self.animate('coupdetete')

    def gestion_decapite(self, temps):
        self.decapite = False
        self.xF = self.x_loc() + (0 if self.rtl else 4)
        self.xT = self.x_loc() + 2
        self.xM = self.x_loc() + (0 if self.rtl else 4)
        self.xG = self.x_loc() + (0 if self.rtl else 4)
        if temps > self.reftemps + 58:
            self.occupe = False
            self.state = State.debout
        elif temps > self.reftemps + 51:
            self.xAtt = self.x_loc() + (4 if self.rtl else 0)
        elif temps > self.reftemps + 50:
            self.yAtt = YT
            self.xAtt = self.x_loc() + (-3 if self.rtl else 7)
        elif temps == self.reftemps + 15:
            self.snd_play('decapite.ogg')
        elif temps == self.reftemps + 2:
            self.animate('decapite', 2)

    def gestion_front(self, temps, opponent: 'Barbarian',
                      soncling: iter, songrogne: iter):
        self.reset_xX_front()
        self.yG = YG
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
                self.xAtt = self.x_loc() + (-2 if self.rtl else 6)

        elif temps == self.reftemps + 6:
            self.snd_play(next(songrogne))
            self.snd_play('epee.ogg')
            self.yAtt = self.yF

        elif temps == self.reftemps + 4:
            self.animate('front', 4)

    def gestion_retourne(self, temps):
        self.xAtt = self.x_loc()
        self.reset_xX_front()
        self.yAtt = 14
        if temps > self.reftemps + 15:
            self.state = State.debout
            self.occupe = False
            self.turn_around(not self.rtl)
        elif self.anim != 'retourne':
            self.animate('retourne')

    def gestion_debout(self, temps, is_ai):
        if self.anim != 'debout':
            self.set_anim_frame('debout', 0)
        self.decapite = True
        self.xAtt = self.x_loc() + (0 if self.rtl else 4)
        self.yAtt = 14
        self.reset_yX()
        self.reset_xX_front()
        if is_ai and temps > self.reftemps + 20:
            self.occupe = False

    def gestion_vainqueur(self):
        self.xAtt = self.x_loc()
        self.yG = YG
        self.yAtt = 14
        self.reset_xX_front()
        if self.anim != 'vainqueur':
            self.animate('vainqueur')

    def gestion_vainqueurKO(self, temps, opponent: 'Barbarian'):
        self.xAtt = self.x_loc() + (4 if self.rtl else 0)
        self.yG = YG
        self.yAtt = 14
        self.reset_xX_front()

        if temps == self.reftemps + 75:
            opponent.set_anim_frame('mort', 3)  # mort4

        elif temps == self.reftemps + 72:
            opponent.set_anim_frame('mort', 2)  # mort3

        elif temps == self.reftemps + 51:
            self.animate('vainqueurKO', 51)

        elif temps == self.reftemps + 36:
            distance = abs(self.x_loc() - opponent.x_loc())
            rtl = self.rtl
            if (distance < 6 and rtl) or (distance > 6 and not rtl):
                self.set_anim_frame('vainqueurKO', 4)  # 'marche3'
                self.x = loc2px(self.x_loc() + abs(6 - distance))
            if (distance > 6 and rtl) or (distance < 6 and not rtl):
                self.set_anim_frame('vainqueurKO', 5)  # 'marche3' xflip=True
                self.x = loc2px(self.x_loc() - abs(6 - distance))

        elif temps == self.reftemps + 8:
            self.animate('vainqueurKO', 8)

    def gestion_touche1(self, temps):
        self.attente = 0
        self.xAtt = self.x_loc() + (4 if self.rtl else 0)
        self.reset_xX_back()
        if temps > self.reftemps + 20:
            self.occupe = False
            self.state = State.debout
        elif temps == self.reftemps:
            self.animate('touche1')

    def gestion_tombe1(self, temps, opponent: 'Barbarian'):
        self.xAtt = self.x_loc() + (4 if self.rtl else 0)
        self.attente = 0
        self.reset_xX_back()
        if temps == self.reftemps + 25:
            self.state = State.debout
            self.occupe = False
        elif temps == self.reftemps + 2:
            if opponent.state != State.coupdetete:
                self.snd_play('tombe.ogg')
        elif temps == self.reftemps:
            self.animate('tombe1')

    # endregion gestions

    @AnimatedSprite.speed.getter
    def speed(self):
        # noinspection PyArgumentList
        return AnimatedSprite.speed.fget(self)

    @speed.setter
    def speed(self, speed: float):
        # noinspection PyArgumentList
        AnimatedSprite.speed.fset(self, speed)
        for s in (self.sangSprite, self.teteSprite, self.teteOmbreSprite):
            s.speed = speed

    def kill(self):
        super().kill()
        for s in (self.sangSprite, self.teteSprite, self.teteOmbreSprite):
            s.kill()

    def animate_football(self, temps):
        if self.teteSprite.is_stopped:
            self.reftemps = temps
            self.snd_play('tete2.ogg')
            self.teteSprite.top_left = self.teteSprite.rect.topleft
            self.teteSprite.animate('football')
            self.teteOmbreSprite.top_left = self.teteOmbreSprite.rect.topleft
            self.teteOmbreSprite.animate('football')

    def stop_football(self):
        self.teteSprite.is_stopped = True
        self.teteOmbreSprite.is_stopped = True
        self.teteSprite.kill()
        self.teteOmbreSprite.kill()

    def animate_sang(self, y):
        if self.sangSprite.alive():
            return
        for gr in self.groups():  # type:LayeredDirty
            # noinspection PyTypeChecker
            gr.add(self.sangSprite, layer=3)
        if self.rtl:
            self.sangSprite.top_left = (self.x + 1 * CHAR_W, y)
        else:
            self.sangSprite.top_left = (self.x + 2 * CHAR_W, y)
        self.sangSprite.animate('sang_touche')

    def animate(self, anim: str, tick=0):
        super().animate(anim, tick)
        #
        if self.anim == 'mortdecap':
            for gr in self.groups():  # type:LayeredDirty
                # noinspection PyTypeChecker
                gr.add(self.sangSprite, self.teteSprite, self.teteOmbreSprite,
                       layer=3)
            #
            for s in (self.sangSprite, self.teteSprite, self.teteOmbreSprite):
                s.rect.topleft = self.top_left
                s.top_left = self.top_left
            rtl = '_rtl' if self.rtl else ''
            self.sangSprite.animate(f'sang{rtl}')
            if self.x_loc() > 19:
                self.teteSprite.animate(f'teteagauche{rtl}')
                self.teteOmbreSprite.animate(f'teteagauche')
            else:
                self.teteSprite.animate(f'teteadroite{rtl}')
                self.teteOmbreSprite.animate(f'teteadroite')


class Sorcier(AnimatedSprite):
    def __init__(self, opts, x, y, rtl=False, anim='idle'):
        super().__init__((x, y), anims.sorcier())
        self.opts = opts
        self.rtl = rtl
        self.animate(anim)
        self.ltr_anims = self.anims
        self.rtl_anims = rtl_anims(self.anims)
        #
        self.clavierX = 7
        self.clavierY = 7
        self.attaque = False
        #
        self.yAtt = YT
        self.xAtt = 6
        self.yF = YF  # front
        self.yT = YT  # tete
        self.yM = YM  # corps
        self.yG = YG  # genou
        self.xF = px2loc(self.x) + 4
        self.xT = px2loc(self.x) + 4
        self.xM = px2loc(self.x) + 4
        self.xG = px2loc(self.x) + 4
        #
        self.vie = 0
        self.bonus = False
        self.reftemps = 0
        self.attente = 1
        self.occupe = False
        self.sortie = False
        self.levier: Levier = Levier.neutre
        self.state: State = State.debout
        self.feu = AnimatedSprite(self.top_left, anims.feu())
        self.feu.layer = 3

    def snd_play(self, snd: str):
        if snd and self.opts.sound:
            get_snd(snd).play()

    def x_loc(self):
        return px2loc(self.x)

    def occupe_state(self, state: State, temps: int):
        self.state = state
        self.occupe = True
        self.reftemps = temps

    def kill(self):
        super().kill()
        self.feu.kill()

    def gestion_debout(self):
        if self.anim != 'debout':
            self.set_anim_frame('debout', 0)

    def gestion_sorcier(self, temps):
        if temps > self.reftemps + 171:
            self.reftemps = temps + 1

        elif temps == self.reftemps + 171:
            self.xAtt = 6

        elif self.reftemps + 135 < temps < self.reftemps + 170:
            self.xAtt = px2loc(self.feu.x)

        elif temps == self.reftemps + 131:
            self.yAtt = YT
            self.snd_play('feu.ogg')
            # noinspection PyTypeChecker
            self.feu.add(self.groups())
            self.feu.top_left = loc(self.xAtt, self.yAtt)
            self.feu.animate('feu_high', self.animTick)

        elif temps == self.reftemps + 91:
            self.xAtt = 6

        elif self.reftemps + 55 < temps < self.reftemps + 90:
            self.xAtt = px2loc(self.feu.x)
            self.yAtt = YG

        elif temps == self.reftemps + 51:
            self.snd_play('feu.ogg')
            # noinspection PyTypeChecker
            self.feu.add(self.groups())
            self.feu.top_left = loc(self.xAtt, self.yAtt)
            self.feu.animate('feu_low', self.animTick)

        elif temps == self.reftemps + 1:
            if self.is_stopped or self.anim != 'attaque':
                self.animate('attaque', 1)
                self.xAtt = self.x_loc()
                self.yAtt = YT
