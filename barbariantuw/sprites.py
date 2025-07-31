# -*- coding: utf-8 -*-
from typing import Tuple, Dict, Callable, Optional, Iterator

from pygame import Rect
from pygame.font import Font
from pygame.sprite import DirtySprite, AbstractGroup, Group, LayeredDirty
from pygame.surface import Surface
from pygame.time import get_ticks
from pygame.transform import scale

import barbariantuw.anims as anims
from barbariantuw import Game, FRAME_RATE, FONT, Theme, Levier, State
from barbariantuw.anims import get_img


def px2locX(x: float) -> int:
    """
    Convert scaled pixel to character location X 40x25 (320x200 mode, 8x8 font).
    :param x: 0..959
    :return: 1..40
    """
    return int(x / Game.chw + 1)


def px2locY(y: float) -> int:
    """
    Convert scaled pixel to character location X 40x25 (320x200 mode, 8x8 font).
    :param y: 0..599
    :return: 1..25
    """
    return int(y / Game.chh + 1)


def loc2pxX(x: int) -> int:
    """
    Convert character location X 40x25 (320x200 mode, 8x8 font) to scaled pixel.
    :param x: 1..40
    :return:
    """
    return (x - 1) * Game.chw


def loc2pxY(y: int) -> int:
    """
    Convert character location X 40x25 (320x200 mode, 8x8 font) to scaled pixel.
    :param y: 1..25
    :return:
    """
    return (y - 1) * Game.chh


def loc(x: int, y: int) -> Tuple[int, int]:
    """
    Convert character location 40x25 (320x200 mode, 8x8 font) to scaled pixel.
    :param x: 1..40
    :param y: 1..25
    :return:
    """
    return loc2pxX(x), loc2pxY(y)


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
    actions: Optional[Iterator[anims.Act]] = None
    act: Optional[anims.Act] = None
    actTick: int = 0

    def __init__(self,
                 topleft: Tuple[float, float],
                 animations: Dict[str, anims.Animation],
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


YF = 16
YT = 17
YM = 19
YG = 21


class Barbarian(AnimatedSprite):
    xF: int = 0
    xT: int = 0
    xM: int = 0
    xG: int = 0
    _vie: int = 12
    on_vie_changed: Callable[[int], None]
    on_score: Callable[[int], None]
    on_mort: Callable[['Barbarian'], None]

    def __init__(self, opts, x, y, subdir: str, rtl=False, anim='debout'):
        super().__init__((x, y), anims.barb(subdir))
        self.opts = opts
        self.rtl = rtl
        #
        self.sang = AnimatedSprite(self.topleft, anims.sang_decap())
        self.tete = AnimatedSprite(self.topleft, anims.tete_decap(subdir))
        self.teteOmbre = AnimatedSprite(self.topleft, anims.teteombre_decap())
        self.ltr_anims = self.anims
        self.rtl_anims = anims.barb_rtl(subdir)
        self.anims = self.rtl_anims if rtl else self.ltr_anims
        self._xLoc = px2locX(self.x)
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

    @property
    def vie(self):
        return self._vie

    @vie.setter
    def vie(self, vie: int):
        if self._vie != vie:
            self._vie = vie
            if self.on_vie_changed:
                self.on_vie_changed(vie)

    def recule_levier(self):
        return Levier.droite if self.rtl else Levier.gauche

    def avance_levier(self):
        return Levier.gauche if self.rtl else Levier.droite

    def reset_xX(self, offset):
        self.xF = self.xLoc + offset
        self.xT = self.xF
        self.xM = self.xF
        self.xG = self.xF

    def reset_xX_front(self):
        self.reset_xX(0 if self.rtl else 4)

    def reset_xX_back(self):
        self.reset_xX(4 if self.rtl else 0)

    def reset_xX_assis(self):
        self.xF = self.xLoc + (4 if self.rtl else 0)
        self.xT = self.xLoc + (4 if self.rtl else 0)
        self.xM = self.xLoc + (0 if self.rtl else 4)
        self.xG = self.xLoc + (0 if self.rtl else 4)

    def reset_yX(self):
        self.yF = YF
        self.yT = YT
        self.yM = YM
        self.yG = YG

    @property
    def xLoc(self):
        return self._xLoc

    @property
    def x(self):
        # noinspection PyArgumentList
        return AnimatedSprite.x.fget(self)

    @x.setter
    def x(self, x: float):
        # noinspection PyArgumentList
        AnimatedSprite.x.fset(self, x)
        self._xLoc = px2locX(x)

    @property
    def topleft(self) -> Tuple[float, float]:
        # noinspection PyArgumentList
        return AnimatedSprite.topleft.fget(self)

    @topleft.setter
    def topleft(self, topleft: Tuple[float, float]):
        # noinspection PyArgumentList
        AnimatedSprite.topleft.fset(self, topleft)
        self._xLoc = px2locX(topleft[0])

    def degat(self, opponent: 'Barbarian'):
        ltr = not self.rtl and self.xLoc < opponent.xLoc
        rtl = self.rtl and self.xLoc > opponent.xLoc
        yAtt = opponent.yAtt
        xAtt = opponent.xAtt
        if yAtt == self.yF and (ltr and xAtt <= self.xF
                                or rtl and xAtt >= self.xF):
            if self.state == State.protegeH:
                self.state = State.clingH
            else:
                self.state = State.tombe
                self.infoDegatF += 1
            return True

        if yAtt == self.yT and (ltr and xAtt <= self.xT
                                or rtl and xAtt >= self.xT):
            if opponent.state == State.coupdetete:
                self.state = State.tombe
            else:
                self.state = State.touche
                self.infoDegatT += 1
                opponent.on_score(250)
            return True

        if yAtt == self.yM and (ltr and xAtt <= self.xM
                                or rtl and xAtt >= self.xM):
            if self.state == State.protegeD:
                self.state = State.clingD
            elif opponent.state == State.coupdepied:
                self.state = State.tombe
            else:
                self.state = State.touche
                opponent.on_score(250)
            return True

        if yAtt == self.yG and (ltr and xAtt <= self.xG
                                or rtl and xAtt >= self.xG):
            if opponent.state in (State.araignee, State.rouladeAV):
                self.state = State.tombe
            elif self.state == State.protegeD:
                self.state = State.clingD
            else:
                self.state = State.touche
                self.infoDegatG += 1
                opponent.on_score(100)
            return True

        return False

    def turn_around(self, rtl):
        self.anims = self.rtl_anims if rtl else self.ltr_anims
        self.frames = self.anims[self.anim].frames
        self.frame = self.frames[self.frameNum]
        self.image = self.frame.image
        self.rtl = rtl
        self._update_rect()

    def occupe_state(self, state: State, temps: int):
        self.state = state
        self.occupe = True
        self.reftemps = temps

    def deoccupe_state(self, state: State):
        self.state = state
        self.occupe = False

    def clavier(self):
        if self.pressedUp and self.clavierY > 5:
            self.clavierY -= 1
        if self.pressedDown and self.clavierY < 9:
            self.clavierY += 1
        if self.pressedLeft and self.clavierX > 5:
            self.clavierX -= 1
        if self.pressedRight and self.clavierX < 9:
            self.clavierX += 1
        self.attaque = self.pressedFire

        if self.clavierX <= 6 and self.clavierY <= 6:
            self.levier = Levier.hautG
        elif self.clavierX >= 8 and self.clavierY <= 6:
            self.levier = Levier.hautD
        elif self.clavierX <= 6 and self.clavierY >= 8:
            self.levier = Levier.basG
        elif self.clavierX >= 8 and self.clavierY >= 8:
            self.levier = Levier.basD

        elif self.clavierX <= 6 and self.clavierY == 7:
            self.levier = Levier.gauche
        elif self.clavierX >= 8 and self.clavierY == 7:
            self.levier = Levier.droite
        elif self.clavierX == 7 and self.clavierY >= 8:
            self.levier = Levier.bas
        elif self.clavierX == 7 and self.clavierY <= 6:
            self.levier = Levier.haut

    # region actions
    def action_debut(self, temps):
        self.protegeD = False
        self.protegeH = False
        self.attente += 1
        # pour se relever
        self.assis = False
        if self.state == State.assis2:
            self.occupe_state(State.releve, temps)
        # attente des 5 secondes
        elif self.attente > FRAME_RATE * 5:
            self.occupe_state(State.attente, temps)
        # etat debout
        else:
            self.state = State.debout

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
    def gestion(self, temps, opponent: 'Barbarian',
                soncling: iter, songrogne: iter, sontouche: iter):

        if self.state == State.attente:
            self.gestion_attente(temps)

        elif self.state == State.debout:
            self.gestion_debout(temps)

        elif self.state == State.avance:
            self.gestion_avance(temps, opponent, soncling, songrogne)

        elif self.state == State.recule:
            self.gestion_recule(temps)

        elif self.state == State.saute:
            self.gestion_saute(temps)

        elif self.state == State.assis:
            self.gestion_assis(temps)

        elif self.state == State.assis2:
            self.gestion_assis2(temps, opponent, soncling, songrogne)

        elif self.state == State.releve:
            self.gestion_releve(temps, opponent, soncling, songrogne)

        elif self.state == State.rouladeAV:
            self.gestion_rouladeAV(temps, opponent)

        elif self.state == State.rouladeAR:
            self.gestion_rouladeAR(temps)

        elif self.state == State.protegeH1:
            self.gestion_protegeH1(temps)

        elif self.state == State.protegeH:
            self.gestion_protegeH(temps, opponent, soncling, songrogne)

        elif self.state == State.protegeD1:
            self.gestion_protegeD1(temps)

        elif self.state == State.protegeD:
            self.gestion_protegeD(temps)

        elif self.state == State.cou:  # ****attention au temps sinon il saute
            self.gestion_cou(temps, opponent, soncling, songrogne)

        elif self.state == State.devant:
            self.gestion_devant(temps, opponent, soncling, songrogne)

        elif self.state == State.genou:
            self.gestion_genou(temps, opponent, soncling, songrogne)

        elif self.state == State.araignee:
            self.gestion_araignee(temps, opponent, soncling, songrogne)

        elif self.state == State.coupdepied:
            self.gestion_coupdepied(temps, opponent)

        elif self.state == State.coupdetete:
            self.gestion_coupdetete(temps)

        elif self.state == State.decapite:
            self.gestion_decapite(temps)

        elif self.state == State.front:
            self.gestion_front(temps, opponent, soncling, songrogne)

        elif self.state == State.retourne:
            self.gestion_retourne(temps)

        elif self.state == State.vainqueur:
            self.gestion_vainqueur()

        elif self.state == State.vainqueurKO:
            self.gestion_vainqueurKO(temps, opponent)

        # ******degats******
        elif self.state == State.touche:
            self.gestion_touche(temps, opponent, sontouche)

        elif self.state == State.touche1:
            self.gestion_touche1(temps)

        elif self.state == State.tombe:
            self.gestion_tombe(temps, opponent)

        elif self.state == State.tombe1:
            self.gestion_tombe1(temps, opponent)

        # bruit des epees  et decapitations loupees
        elif self.state == State.clingD:
            self.gestion_clingD(temps, opponent, soncling, sontouche)

        elif self.state == State.clingH:
            self.gestion_clingH(opponent, soncling)

        elif self.state == State.mortdecap:
            self.gestion_mortedecap(temps, opponent)

    def gestion_attente(self, temps):
        self.reset_xX_front()
        if temps > self.reftemps + 50:
            self.attente = 1
            self.deoccupe_state(State.debout)
        elif temps == self.reftemps + 8:
            self.animate('attente', 8)

    def gestion_avance(self, temps, opponent: 'Barbarian',
                       soncling: iter, songrogne: iter):
        self.reset_xX_front()
        self.xAtt = self.xLoc + (4 if self.rtl else 0)
        if self.attaque:
            self.occupe_state(State.devant, temps)
            self.gestion_devant(temps, opponent, soncling, songrogne)
        elif self.anim != 'avance':
            self.animate('avance')

    def gestion_recule(self, temps):
        self.reset_xX_front()
        self.xAtt = self.xLoc + (4 if self.rtl else 0)
        if self.attaque:
            self.occupe_state(State.decapite, temps)
            self.gestion_decapite(temps)
        elif self.anim != 'recule':
            self.animate('recule')

    def gestion_saute(self, temps):
        self.xAtt = self.xLoc + (4 if self.rtl else 0)
        self.reset_xX_front()
        self.decapite = False
        self.yG = YT
        self.yM = YT
        self.yAtt = 14
        if self.attaque:
            self.occupe_state(State.cou, temps)
        elif temps > self.reftemps + 45:
            self.deoccupe_state(State.debout)
            self.yG = YG
            self.yM = YM
        elif temps > self.reftemps + 40:
            self.xM = self.xLoc + (0 if self.rtl else 4)
            self.xG = self.xLoc + (0 if self.rtl else 4)
        elif temps > self.reftemps + 30:
            self.xM = self.xLoc + (0 if self.rtl else 4)
            self.xG = self.xLoc + (3 if self.rtl else 1)
            self.decapite = True
        elif temps > self.reftemps + 13:
            self.xM = self.xLoc + (3 if self.rtl else 1)
            self.xG = self.xLoc + (3 if self.rtl else 1)
        elif temps > self.reftemps + 2:
            self.xM = self.xLoc + (0 if self.rtl else 4)
            self.xG = self.xLoc + (3 if self.rtl else 1)
        elif self.anim != 'saute':
            self.animate('saute')

    def gestion_assis(self, temps):
        self.xAtt = self.xLoc + (4 if self.rtl else 0)
        self.reset_xX_assis()
        self.yT = YM
        self.set_frame('assis', 0)
        if temps > self.reftemps + 10:
            self.state = State.assis2

    def gestion_assis2(self, temps, opponent: 'Barbarian',
                       soncling: iter, songrogne: iter):
        self.occupe = False
        self.assis = True
        self.xAtt = self.xLoc + (4 if self.rtl else 0)
        self.reset_xX_assis()
        self.set_frame('assis', 1)
        if self.attaque and self.levier == Levier.bas:
            self.occupe_state(State.genou, temps)
            self.gestion_genou(temps, opponent, soncling, songrogne)

    def gestion_releve(self, temps, opponent: 'Barbarian',
                       soncling: iter, songrogne: iter):
        self.xAtt = self.xLoc + (4 if self.rtl else 0)
        self.yAtt = 14
        self.reset_xX_assis()
        self.yT = YT
        self.set_frame('releve', 0)
        if temps > self.reftemps + 10:
            self.deoccupe_state(State.debout)
        elif self.attaque and self.levier == Levier.bas:
            self.occupe_state(State.genou, temps)
            self.gestion_genou(temps, opponent, soncling, songrogne)

    def gestion_rouladeAV(self, temps, opponent):
        self.reset_xX_back()
        self.yG = YG
        self.yAtt = self.yG
        self.xAtt = self.xLoc + (4 if self.rtl else 0)
        self.yT = self.yG
        if self.attaque:
            self.yT = YT
            self.occupe_state(State.coupdepied, temps)

        elif temps > self.reftemps + 38:
            self.xT = self.xLoc + (0 if self.rtl else 4)
            self.xM = self.xLoc + (0 if self.rtl else 4)
            self.yT = YT
            jax = self.xLoc
            jbx = opponent.xLoc
            if (not self.rtl and jax >= jbx - 1) or (self.rtl and jax <= jbx + 1):
                self.occupe_state(State.retourne, temps)
                opponent.occupe_state(State.retourne, temps)
                self.yAtt = 14
                opponent.yAtt = 14
            else:
                self.deoccupe_state(State.debout)
                self.xAtt = jax + (4 if self.rtl else 0)
                self.yAtt = YT
                self.reset_xX_front()
                self.reset_yX()

        elif temps > self.reftemps + 23:
            if self.anim == 'rouladeAV':
                if self.rtl:
                    distance = self.xLoc - opponent.xLoc
                else:
                    distance = opponent.xLoc - self.xLoc
                if 3 == distance:  # do not rollout at left half opponent
                    self.animate('rouladeAV-out', self.animTick)

        elif temps == self.reftemps + 18:
            if opponent.state in (State.tombe, State.tombe1):
                self.animate('rouladeAV-out', self.animTick)

        elif temps == self.reftemps + 17:
            self.xAtt = self.xLoc + (0 if self.rtl else 4)

        elif temps == self.reftemps + 15:
            if opponent.state in (State.tombe, State.tombe1):
                self.animate('rouladeAV-out', self.animTick)

        elif temps == self.reftemps + 14:
            self.xAtt = self.xLoc + (0 if self.rtl else 4)

        elif 2 < temps - self.reftemps < 11:
            self.xM = self.xLoc + (0 if self.rtl else 4)

        elif temps == self.reftemps + 2:
            self.xM = self.xLoc + (0 if self.rtl else 4)
            self.animate('rouladeAV', 2)

    def gestion_rouladeAR(self, temps):
        self.reset_xX_back()
        self.yG = YG
        self.yAtt = self.yG
        self.xAtt = self.xLoc + (4 if self.rtl else 0)
        if temps > self.reftemps + 33:
            self.xT = self.xLoc + (0 if self.rtl else 4)
            self.xM = self.xLoc + (0 if self.rtl else 4)
            self.deoccupe_state(State.debout)
        elif temps == self.reftemps + 2:
            self.animate('rouladeAR', 2)

    def gestion_protegeH1(self, temps):
        self.reset_xX_front()
        self.xAtt = self.xLoc + (4 if self.rtl else 0)
        self.yG = YG
        if temps > self.reftemps + 5:
            self.protegeH = True
            self.deoccupe_state(State.protegeH)
        elif temps == self.reftemps + 2:
            self.animate('protegeH', 1)

    def gestion_protegeH(self, temps, opponent: 'Barbarian',
                         soncling: iter, songrogne: iter):
        self.reset_xX_front()
        self.xAtt = self.xLoc + (4 if self.rtl else 0)
        self.yG = YG
        self.set_frame('protegeH', 1)
        if self.attaque:
            self.occupe_state(State.araignee, temps)
            self.gestion_araignee(temps, opponent, soncling, songrogne)

    def gestion_protegeD1(self, temps):
        self.xAtt = self.xLoc + (4 if self.rtl else 0)
        self.yG = YG
        self.reset_xX_front()
        self.decapite = False
        self.set_frame('protegeD', 0)
        if self.attaque:
            self.occupe_state(State.coupdetete, temps)
            self.gestion_coupdetete(temps)
        elif temps > self.reftemps + 5:
            self.deoccupe_state(State.protegeD)
            self.protegeD = True
        elif temps == self.reftemps + 2:
            anims.snd_play('protege.ogg')

    def gestion_protegeD(self, temps):
        self.xAtt = self.xLoc + (4 if self.rtl else 0)
        self.yG = YG
        self.reset_xX_front()
        self.decapite = False
        self.set_frame('protegeD', 1)
        if self.attaque:
            self.occupe_state(State.coupdetete, temps)
            self.gestion_coupdetete(temps)

    def gestion_cou(self, temps, opponent: 'Barbarian',
                    soncling: iter, songrogne: iter):
        self.reset_xX_front()
        self.reset_yX()
        self.yAtt = YT
        if temps > self.reftemps + 45:
            self.deoccupe_state(State.debout)

        elif temps > self.reftemps + 31:
            self.xAtt = self.xLoc + (4 if self.rtl else 0)

        elif temps == self.reftemps + 31:
            if (opponent.state == State.cou
                    and abs(self.xLoc - opponent.xLoc) < 12
                    and (30 < temps - opponent.reftemps <= 45)):
                # do not attack in same state
                # cycle and play cling-sound once (for one player only)
                if not self.rtl:
                    anims.snd_play(next(soncling))
            else:
                self.xT = self.xLoc + (4 if self.rtl else 0)
                self.xAtt = self.xLoc + (-3 if self.rtl else 7)

        elif temps == self.reftemps + 16:
            self.yAtt = self.yT

        elif temps == self.reftemps + 4:
            anims.snd_play(next(songrogne))
            self.animate('cou', 4)

    def gestion_devant(self, temps, opponent: 'Barbarian',
                       soncling: iter, songrogne: iter):

        self.reset_xX_front()
        self.yG = YG
        if temps > self.reftemps + 45:
            self.deoccupe_state(State.debout)

        elif temps > self.reftemps + 21:
            self.xAtt = self.xLoc + (4 if self.rtl else 0)

        elif temps == self.reftemps + 21:
            if opponent.state == State.devant and opponent.frameNum == 2:  # devant3.gif
                distance = abs(self.xLoc - opponent.xLoc)
                # cycle and play cling-sound once (for one player only)
                if distance < 10 and not self.rtl:
                    anims.snd_play(next(soncling))
            else:
                self.xM = self.xLoc + (4 if self.rtl else 0)
                self.xAtt = self.xLoc + (-2 if self.rtl else 6)

        elif temps == self.reftemps + 11:
            anims.snd_play(next(songrogne))
            self.yAtt = self.yM

        elif temps == self.reftemps:
            self.animate('devant')

    def gestion_genou(self, temps, opponent: 'Barbarian',
                      soncling: iter, songrogne: iter):
        self.reset_xX_assis()
        self.yG = YG
        if temps > self.reftemps + 45:
            self.deoccupe_state(State.assis2)
        elif temps > self.reftemps + 21:
            self.xAtt = self.xLoc + (4 if self.rtl else 0)
        elif temps > self.reftemps + 20:
            if (opponent.state == State.genou
                    and 20 <= temps - opponent.reftemps < 30):  # genou3.gif
                distance = abs(self.xLoc - opponent.xLoc)
                # cycle and play cling-sound once (for one player only)
                if distance < 12 and not self.rtl:
                    anims.snd_play(next(soncling))
            else:
                self.xG = self.xLoc + (4 if self.rtl else 0)
                # no attack genou<>coupdepied (pied2.gif)
                if not (opponent.state == State.coupdepied
                        and opponent.frameNum == 1):
                    self.xAtt = self.xLoc + (-3 if self.rtl else 7)
        elif temps == self.reftemps + 11:
            anims.snd_play(next(songrogne))
            self.yAtt = self.yG

        elif temps == self.reftemps:
            self.animate('genou')

    def gestion_araignee(self, temps, opponent: 'Barbarian',
                         soncling: iter, songrogne: iter):
        self.reset_xX_front()
        self.yAtt = YM
        self.xAtt = self.xLoc + (4 if self.rtl else 0)
        self.yG = YG
        if temps > self.reftemps + 32:
            self.deoccupe_state(State.debout)

        elif temps == self.reftemps + 21:
            if opponent.state == State.araignee:
                distance = abs(self.xLoc - opponent.xLoc)
                # cycle and play cling-sound once (for one player only)
                if distance < 9 and not self.rtl:
                    anims.snd_play(next(soncling))
            else:
                self.xAtt = self.xLoc + (-2 if self.rtl else 6)

        elif temps == self.reftemps + 8:
            anims.snd_play(next(songrogne))

        elif temps == self.reftemps:
            self.animate('araignee')

    def gestion_coupdepied(self, temps, opponent):
        self.reset_xX_front()
        self.xF = self.xLoc + 2
        self.xT = self.xLoc + 2
        self.yAtt = self.yM
        self.yM = YM
        if temps > self.reftemps + 50:
            self.deoccupe_state(State.debout)
            self.xF = self.xLoc + (0 if self.rtl else 4)
            self.xT = self.xLoc + (0 if self.rtl else 4)
        elif temps > self.reftemps + 30:
            self.xM = self.xLoc + (0 if self.rtl else 4)
        elif temps > self.reftemps + 10:
            self.xM = self.xLoc + (-1 if self.rtl else 5)
            self.xAtt = self.xLoc + (4 if self.rtl else 0)
        elif temps > self.reftemps + 9:
            self.xM = self.xLoc + (4 if self.rtl else 0)
            # no attack coupdepied<>coupdepied
            if not (opponent.state == State.coupdepied
                    and (7 < temps - opponent.reftemps < 30)):
                self.xAtt = self.xLoc + (-1 if self.rtl else 5)
        elif temps > self.reftemps + 1:
            self.xM = self.xLoc + (0 if self.rtl else 4)
        elif temps == self.reftemps:
            self.animate('coupdepied')

    def gestion_coupdetete(self, temps):
        self.reset_xX_front()
        self.yG = YG
        if temps > self.reftemps + 38:
            self.deoccupe_state(State.debout)
        elif temps > self.reftemps + 20:
            self.xAtt = self.xLoc + (4 if self.rtl else 0)
        elif temps > self.reftemps + 19:
            self.xAtt = self.xLoc + (0 if self.rtl else 4)
        elif temps > self.reftemps + 18:
            self.xAtt = self.xLoc + (4 if self.rtl else 0)
        elif temps > self.reftemps + 9:
            self.yAtt = self.yF
        elif temps == self.reftemps:
            self.animate('coupdetete')

    def gestion_decapite(self, temps):
        self.decapite = False
        self.xF = self.xLoc + (0 if self.rtl else 4)
        self.xT = self.xLoc + 2
        self.xM = self.xLoc + (0 if self.rtl else 4)
        self.xG = self.xLoc + (0 if self.rtl else 4)
        if temps > self.reftemps + 58:
            self.deoccupe_state(State.debout)
        elif temps > self.reftemps + 51:
            self.xAtt = self.xLoc + (4 if self.rtl else 0)
        elif temps > self.reftemps + 50:
            self.yAtt = YT
            self.xAtt = self.xLoc + (-3 if self.rtl else 7)
        elif temps == self.reftemps + 2:
            self.animate('decapite', 2)

    def gestion_front(self, temps, opponent: 'Barbarian',
                      soncling: iter, songrogne: iter):
        self.reset_xX_front()
        self.yG = YG
        if temps > self.reftemps + 45:
            self.deoccupe_state(State.debout)

        elif temps > self.reftemps + 24:
            self.xAtt = self.xLoc + (4 if self.rtl else 0)

        elif temps == self.reftemps + 24:
            if opponent.state == State.front:
                distance = abs(self.xLoc - opponent.xLoc)
                # cycle and play cling-sound once (for one player only)
                if distance < 12 and not self.rtl:
                    anims.snd_play(next(soncling))
            else:
                self.xF = self.xLoc + (4 if self.rtl else 0)
                self.xAtt = self.xLoc + (-2 if self.rtl else 6)

        elif temps == self.reftemps + 6:
            anims.snd_play(next(songrogne))
            self.yAtt = self.yF

        elif temps == self.reftemps + 4:
            self.animate('front', 4)

    def gestion_retourne(self, temps):
        self.xAtt = self.xLoc
        self.reset_xX_front()
        self.yAtt = 14
        if temps > self.reftemps + 15:
            self.deoccupe_state(State.debout)
            self.turn_around(not self.rtl)
        elif self.anim != 'retourne':
            self.animate('retourne')

    def gestion_debout(self, temps):
        if self.anim != 'debout':
            self.set_frame('debout', 0)
        self.decapite = True
        self.xAtt = self.xLoc + (0 if self.rtl else 4)
        self.yAtt = 14
        self.reset_yX()
        self.reset_xX_front()
        if temps > self.reftemps + 20:  # for ai, see occupe debout
            self.occupe = False

    def gestion_touche(self, temps, opponent: 'Barbarian', sontouche: iter):
        self.attente = 0
        self.xAtt = self.xLoc + (4 if self.rtl else 0)
        self.reset_xX_back()
        self.reset_yX()
        if opponent.state == State.coupdepied:
            self.state = State.tombe
            self.gestion_tombe(temps, opponent)
            return

        if opponent.state == State.decapite and self.decapite:
            self.vie = 0
            self.occupe_state(State.mortdecap, temps)
            opponent.on_score(250)
            self.gestion_mortedecap(temps, opponent)
            return

        self.animate_sang(loc2pxY(opponent.yAtt))
        self.vie -= 1
        if self.vie <= 0:
            self.occupe_state(State.mort, temps)
            self.gestion_mort(temps, opponent)
            return

        anims.snd_play(next(sontouche))

        self.occupe_state(State.touche1, temps)
        self.decapite = True
        self.gestion_touche1(temps)

    def gestion_tombe(self, temps, opponent: 'Barbarian'):
        self.xAtt = self.xLoc + (4 if self.rtl else 0)
        self.attente = 0
        self.reset_xX_back()
        self.reset_yX()
        if opponent.state != State.rouladeAV:
            self.animate_sang(loc2pxY(opponent.yAtt))
            self.vie -= 1
            opponent.on_score(100)

        if self.vie <= 0:
            self.occupe_state(State.mort, temps)
            self.gestion_mort(temps, opponent)
            return
        if opponent.state == State.coupdetete:
            opponent.on_score(150)
            anims.snd_play('coupdetete.ogg')
        elif opponent.state == State.coupdepied:
            opponent.on_score(150)
            anims.snd_play('coupdepied.ogg')
        self.occupe_state(State.tombe1, temps)
        self.gestion_tombe1(temps, opponent)

    def gestion_mort(self, temps, opponent: 'Barbarian'):
        self.on_mort(self)
        self.animate('mort')
        opponent.occupe_state(State.vainqueurKO, temps)

    def gestion_mortedecap(self, temps, opponent: 'Barbarian'):
        if temps == self.reftemps:
            self.on_mort(self)
            self.animate('mortdecap')
            opponent.occupe_state(State.vainqueur, temps)

    def gestion_vainqueur(self):
        self.xAtt = self.xLoc
        self.yG = YG
        self.yAtt = 14
        self.reset_xX_front()
        if self.anim != 'vainqueur':
            self.animate('vainqueur')

    def gestion_vainqueurKO(self, temps, opponent: 'Barbarian'):
        self.xAtt = self.xLoc + (4 if self.rtl else 0)
        self.yG = YG
        self.yAtt = 14
        self.reset_xX_front()

        if temps == self.reftemps + 75:
            opponent.set_frame('mort', 3)  # mort4

        elif temps == self.reftemps + 72:
            opponent.set_frame('mort', 2)  # mort3

        elif temps == self.reftemps + 51:
            self.animate('vainqueurKO', 51)

        elif temps == self.reftemps + 36:
            distance = abs(self.xLoc - opponent.xLoc)
            if (distance < 5 and self.rtl) or (distance > 5 and not self.rtl):
                self.set_frame('vainqueurKO', 4)  # 'marche3'
                self.x = loc2pxX(self.xLoc + abs(5 - distance))
            if (distance > 5 and self.rtl) or (distance < 5 and not self.rtl):
                self.set_frame('vainqueurKO', 5)  # 'marche3' xflip=True
                self.x = loc2pxX(self.xLoc - abs(5 - distance))

        elif temps == self.reftemps + 8:
            self.animate('vainqueurKO', 8)

    def gestion_touche1(self, temps):
        self.attente = 0
        self.xAtt = self.xLoc + (4 if self.rtl else 0)
        self.reset_xX_back()
        if temps > self.reftemps + 20:
            self.deoccupe_state(State.debout)
        elif temps == self.reftemps:
            self.animate('touche1')

    def gestion_tombe1(self, temps, opponent: 'Barbarian'):
        self.xAtt = self.xLoc + (4 if self.rtl else 0)
        self.attente = 0
        self.reset_xX_back()
        if temps == self.reftemps + 25:
            self.deoccupe_state(State.debout)
        elif temps == self.reftemps + 2:
            if opponent.state != State.coupdetete:
                anims.snd_play('tombe.ogg')
        elif temps == self.reftemps:
            self.animate('tombe1')

    def gestion_clingD(self, temps, opponent: 'Barbarian',
                       soncling: iter, sontouche: iter):
        if (opponent.state == State.decapite and not self.decapite
                or opponent.state == State.genou):
            self.occupe_state(State.touche, temps)
            self.gestion_touche(temps, opponent, sontouche)
        else:
            distance = abs(self.xLoc - opponent.xLoc)
            if distance < 12:
                anims.snd_play(next(soncling))
            self.state = State.protegeD

    def gestion_clingH(self, opponent: 'Barbarian', soncling: iter):
        distance = abs(self.xLoc - opponent.xLoc)
        if distance < 12:
            anims.snd_play(next(soncling))
        self.state = State.protegeH

    # endregion gestions

    @property
    def speed(self):
        # noinspection PyArgumentList
        return AnimatedSprite.speed.fget(self)

    @speed.setter
    def speed(self, speed: float):
        # noinspection PyArgumentList
        AnimatedSprite.speed.fset(self, speed)
        for s in (self.sang, self.tete, self.teteOmbre):
            s.speed = speed

    def kill(self):
        super().kill()
        for s in (self.sang, self.tete, self.teteOmbre):
            s.kill()

    def animate_football(self):
        if self.tete.stopped:
            self.tete.topleft = self.tete.rect.topleft
            self.tete.animate('football')
            self.teteOmbre.topleft = self.teteOmbre.rect.topleft
            self.teteOmbre.animate('football')

    def stop_football(self):
        if self.tete.alive():
            self.tete.kill()
            self.teteOmbre.kill()

    def animate_sang(self, y):
        if self.sang.alive():
            return
        for gr in self.groups():  # type:LayeredDirty
            # noinspection PyTypeChecker
            gr.add(self.sang, layer=3)
        if self.rtl:
            self.sang.topleft = (self.x + 1 * Game.chw, y)
        else:
            self.sang.topleft = (self.x + 2 * Game.chw, y)
        self.sang.animate('sang_touche')

    def animate(self, anim: str, tick=0):
        super().animate(anim, tick)
        #
        if self.anim == 'mortdecap':
            for gr in self.groups():  # type:LayeredDirty
                # noinspection PyTypeChecker
                gr.add(self.sang, self.tete, self.teteOmbre,
                       layer=3)
            #
            for s in (self.sang, self.tete, self.teteOmbre):
                s.rect.topleft = self.topleft
                s.topleft = self.topleft
            rtl = '_rtl' if self.rtl else ''
            self.sang.animate(f'sang{rtl}')
            if self.xLoc > 19:
                self.tete.animate(f'teteagauche{rtl}')
                self.teteOmbre.animate(f'teteagauche')
            else:
                self.tete.animate(f'teteadroite{rtl}')
                self.teteOmbre.animate(f'teteadroite')


class Sorcier(AnimatedSprite):
    def __init__(self, x, y, anim='debout'):
        super().__init__((x, y), anims.sorcier())
        self.rtl = False
        self._xLoc = px2locX(self.x)
        self.animate(anim)
        #
        self.yAtt = YT
        self.xAtt = 6
        self.yF = YF  # front
        self.yT = YT  # tete
        self.yM = YM  # corps
        self.yG = YG  # genou
        self.xF = px2locX(self.x) + 4
        self.xT = px2locX(self.x) + 4
        self.xM = px2locX(self.x) + 4
        self.xG = px2locX(self.x) + 4
        #
        self.vie = 0
        self.bonus = False
        self.reftemps = 0
        self.occupe = False
        self.sortie = False
        self.levier: Levier = Levier.neutre
        self.state: State = State.debout
        self.feu = AnimatedSprite(self.topleft, anims.feu())
        self.feu.layer = 3
        self.sangSprite = AnimatedSprite(self.topleft, anims.sang_decap())

    @property
    def xLoc(self):
        return self._xLoc

    @property
    def x(self):
        # noinspection PyArgumentList
        return AnimatedSprite.x.fget(self)

    @x.setter
    def x(self, x: float):
        # noinspection PyArgumentList
        AnimatedSprite.x.fset(self, x)
        self._xLoc = px2locX(x)

    @property
    def topleft(self) -> Tuple[float, float]:
        # noinspection PyArgumentList
        return AnimatedSprite.topleft.fget(self)

    @topleft.setter
    def topleft(self, topleft: Tuple[float, float]):
        # noinspection PyArgumentList
        AnimatedSprite.topleft.fset(self, topleft)
        self._xLoc = px2locX(topleft[0])

    def occupe_state(self, state: State, temps: int):
        self.state = state
        self.occupe = True
        self.reftemps = temps

    def kill(self):
        super().kill()
        self.feu.kill()

    def degat(self, opponent: Barbarian) -> bool:
        return self.xLoc <= opponent.xAtt <= self.xLoc + 1

    def gestion_debout(self):
        if self.anim != 'debout':
            self.set_frame('debout', 0)

    # noinspection PyUnusedLocal
    def gestion(self, temps, opponent: 'Barbarian',
                soncling: iter, songrogne: iter, sontouche: iter,
                is_ai: bool):

        if self.state == State.debout:
            self.gestion_debout()

        elif self.state == State.sorcier:
            self.gestion_sorcier(temps)

    def animate_sang(self, y):
        for gr in self.groups():  # type:LayeredDirty
            # noinspection PyTypeChecker
            gr.add(self.sangSprite, layer=3)
        self.sangSprite.topleft = (self.x + 2 * Game.chw, y)
        self.sangSprite.animate('sang_touche')
        anims.snd_play('touche.ogg')

    def gestion_sorcier(self, temps):
        if temps > self.reftemps + 173:
            self.reftemps = temps + 1

        elif temps == self.reftemps + 173:
            self.xAtt = 6

        elif 135 < temps - self.reftemps < 170:
            self.xAtt = px2locX(self.feu.x)

        elif temps == self.reftemps + 131:
            self.yAtt = YT
            self.feu.add(*self.groups())
            self.feu.topleft = loc(self.xAtt - 2, self.yAtt)
            self.feu.animate('feu_high', self.animTick)

        elif temps == self.reftemps + 93:
            self.xAtt = 6

        elif 55 < temps - self.reftemps < 90:
            self.xAtt = px2locX(self.feu.x)
            self.yAtt = YG

        elif temps == self.reftemps + 51:
            self.feu.add(*self.groups())
            self.feu.topleft = loc(self.xAtt - 2, self.yAtt)
            self.feu.animate('feu_low', self.animTick)

        elif temps == self.reftemps + 1:
            if self.stopped or self.anim != 'attaque':
                self.animate('attaque', 1)
                self.xAtt = self.xLoc
                self.yAtt = YT
