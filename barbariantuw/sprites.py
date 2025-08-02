# -*- coding: utf-8 -*-
from typing import Tuple, Callable

from pygame.sprite import LayeredDirty

import barbariantuw.anims as anims
from barbariantuw import Game, FRAME_RATE, Levier, State
from barbariantuw.core import AnimatedSprite, snd_play


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
        self.reset_yX()
        self.yT = YM
        self.yF = YM
        self.set_frame('assis', 0)
        if temps > self.reftemps + 10:
            self.state = State.assis2

    def gestion_assis2(self, temps, opponent: 'Barbarian',
                       soncling: iter, songrogne: iter):
        self.occupe = False
        self.assis = True
        self.xAtt = self.xLoc + (4 if self.rtl else 0)
        self.reset_xX_assis()
        self.reset_yX()
        self.yT = YM
        self.yF = YM
        self.set_frame('assis', 1)
        if self.attaque and self.levier == Levier.bas:
            self.occupe_state(State.genou, temps)
            self.gestion_genou(temps, opponent, soncling, songrogne)

    def gestion_releve(self, temps, opponent: 'Barbarian',
                       soncling: iter, songrogne: iter):
        self.xAtt = self.xLoc + (4 if self.rtl else 0)
        self.yAtt = 14
        self.reset_xX_assis()
        self.reset_yX()
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
            snd_play('protege.ogg')

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
                    snd_play(next(soncling))
            else:
                self.xT = self.xLoc + (4 if self.rtl else 0)
                self.xAtt = self.xLoc + (-3 if self.rtl else 7)

        elif temps == self.reftemps + 16:
            self.yAtt = self.yT

        elif temps == self.reftemps + 4:
            snd_play(next(songrogne))
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
                    snd_play(next(soncling))
            else:
                self.xM = self.xLoc + (4 if self.rtl else 0)
                self.xAtt = self.xLoc + (-2 if self.rtl else 6)

        elif temps == self.reftemps + 11:
            snd_play(next(songrogne))
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
                    snd_play(next(soncling))
            else:
                self.xG = self.xLoc + (4 if self.rtl else 0)
                # no attack genou<>coupdepied (pied2.gif)
                if not (opponent.state == State.coupdepied
                        and opponent.frameNum == 1):
                    self.xAtt = self.xLoc + (-3 if self.rtl else 7)
        elif temps == self.reftemps + 11:
            snd_play(next(songrogne))
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
                    snd_play(next(soncling))
            else:
                self.xAtt = self.xLoc + (-2 if self.rtl else 6)

        elif temps == self.reftemps + 8:
            snd_play(next(songrogne))

        elif temps == self.reftemps:
            self.animate('araignee')

    def gestion_coupdepied(self, temps, opponent):
        self.reset_xX_front()
        self.xF = self.xLoc + 2
        self.xT = self.xLoc + 2
        self.yAtt = self.yM
        self.yM = YM
        self.yT = YT
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
                    snd_play(next(soncling))
            else:
                self.xF = self.xLoc + (4 if self.rtl else 0)
                self.xAtt = self.xLoc + (-2 if self.rtl else 6)

        elif temps == self.reftemps + 6:
            snd_play(next(songrogne))
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

        snd_play(next(sontouche))

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
            snd_play('coupdetete.ogg')
        elif opponent.state == State.coupdepied:
            opponent.on_score(150)
            snd_play('coupdepied.ogg')
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
                snd_play('tombe.ogg')
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
                snd_play(next(soncling))
            self.state = State.protegeD

    def gestion_clingH(self, opponent: 'Barbarian', soncling: iter):
        distance = abs(self.xLoc - opponent.xLoc)
        if distance < 12:
            snd_play(next(soncling))
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
                soncling: iter, songrogne: iter, sontouche: iter):

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
        snd_play('touche.ogg')

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
