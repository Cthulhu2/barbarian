# -*- coding: utf-8 -*-
import enum
from itertools import cycle
from typing import List

import pygame.key
from pygame import Surface, mixer
from pygame.event import Event
from pygame.locals import *
from pygame.sprite import LayeredDirty, Group
from pygame.time import get_ticks

import barbariantuw.ai as ai
import barbariantuw.anims as anims
from barbariantuw import Game, Partie, Theme, Levier, State
from barbariantuw.core import (
    get_img, get_snd, snd_play, Rectangle, Txt, StaticSprite, AnimatedSprite
)
from barbariantuw.sprites import Barbarian, loc2pxX, loc2pxY, loc, Sorcier


class EmptyScene(LayeredDirty):
    def __init__(self, opts, *sprites_, **kwargs):
        super(EmptyScene, self).__init__(*sprites_, **kwargs)
        self.set_timing_threshold(1000.0 / 25.0)
        back = Surface(Game.screen)
        back.fill(Theme.BACK, back.get_rect())
        # noinspection PyTypeChecker
        self.clear(None, back)
        self.timer = get_ticks()
        self.opts = opts

    def process_event(self, evt):
        pass


def is_any_key_pressed(evt):
    return ((evt.type == JOYBUTTONDOWN and evt.instance_id == 0)
            or (evt.type == KEYDOWN and evt.key in (K_KP_ENTER, K_RETURN,
                                                    K_ESCAPE, K_SPACE)))


class Logo(EmptyScene):
    def __init__(self, opts, *, on_load):
        super(Logo, self).__init__(opts)
        self.usaLogo = False
        self.titre = False
        self.load = False
        self.skip = False
        self.on_load = on_load

    def show_usa_logo(self):
        if self.usaLogo:
            return
        self.usaLogo = True

        # noinspection PyTypeChecker
        self.clear(None, get_img('menu/titreDS.png'))
        self.repaint_rect(((0, 0), Game.screen))

    def show_titre(self):
        if self.titre:
            return
        self.titre = True

        if Game.country == 'USA':
            img = get_img('menu/menu.png').copy()
            logo_ds = get_img('menu/logoDS.png')
            img.blit(logo_ds, (46 * Game.scx, 10 * Game.scy))
        else:
            img = get_img('menu/menu.png')

        heroes = StaticSprite((0, 86 * Game.scy), 'menu/heroes.png', self)
        heroes.rect.x = Game.screen[0] / 2 - heroes.rect.w / 2 - 3 * Game.scx
        hiscores = Game.load_hiscores()
        sz = int(8 * Game.scy)
        top = 114 * Game.scy
        for i, (score, name) in enumerate(hiscores):
            col = Theme.LEADER_TXT if i == 0 else Theme.TXT
            txt = Txt(sz, f'{name:3} {score:05}', col, (121 * Game.scx, top), self)
            top = txt.rect.bottom + 4 * Game.scy
        # noinspection PyTypeChecker
        self.clear(None, img)
        self.repaint_rect(((0, 0), Game.screen))

    def do_load(self):
        if self.load:
            return
        self.load = True
        if self.opts.sound:
            get_snd('tombe.ogg')
            get_snd('epee.ogg')
            get_snd('roule.ogg')
            get_snd('touche.ogg')
            get_snd('touche2.ogg')
            get_snd('touche3.ogg')
            get_snd('attente.ogg')
            get_snd('tete.ogg')
            get_snd('tete2.ogg')
            get_snd('decapite.ogg')
            get_snd('block1.ogg')
            get_snd('block2.ogg')
            get_snd('block3.ogg')
            get_snd('coupdetete.ogg')
            get_snd('coupdepied.ogg')
            get_snd('feu.ogg')
            get_snd('mortdecap.ogg')
            get_snd('mortKO.ogg')
            get_snd('prepare.ogg')
            get_snd('protege.ogg')
            get_snd('grogne1.ogg')
            get_snd('grogne2.ogg')

    def update(self, current_time, *args):
        super(Logo, self).update(current_time, *args)
        passed = current_time - self.timer
        if Game.country == 'USA':
            if passed < 4000:
                self.show_usa_logo()
                if self.skip:
                    self.skip = False
                    self.timer = current_time - 4000
            elif 4000 <= passed < 8000:
                self.show_titre()
                self.do_load()
                if self.skip:
                    self.timer = current_time - 8000
            else:
                self.on_load()
        else:
            if passed < 4000:
                self.show_titre()
                self.do_load()
                if self.skip:
                    self.timer = current_time - 4000
            else:
                self.on_load()

    def process_event(self, evt):
        if is_any_key_pressed(evt):
            self.skip = True


class _MenuBackScene(EmptyScene):
    items: List[Txt]
    cursorIdx: int = 0

    def __init__(self, opts, back: str):
        super(_MenuBackScene, self).__init__(opts)
        if Game.country == 'USA':
            back = get_img(back).copy()
            logo_ds = get_img('menu/logoDS.png')
            back.blit(logo_ds, (46 * Game.scx, 10 * Game.scy))
        else:
            back = get_img(back)
        # noinspection PyTypeChecker
        self.clear(None, back)
        self.items = []

    def select(self, idx, run):
        if self.items:
            idx = min(len(self.items) - 1, max(0, idx))
            self.items[self.cursorIdx].color = Theme.MENU_TXT
            self.cursorIdx = idx
            self.items[self.cursorIdx].color = Theme.BLACK

    def process_event(self, evt):
        if evt.type == KEYDOWN:
            if evt.key in (K_RETURN, K_KP_ENTER):
                self.select(self.cursorIdx, True)
            elif evt.key in (K_UP, K_KP_8):
                self.select(self.cursorIdx - 1, False)
            elif evt.key in (K_DOWN, K_KP_2):
                self.select(self.cursorIdx + 1, False)
        elif evt.type == JOYBUTTONDOWN and evt.instance_id == 0:
            self.select(self.cursorIdx, True)
        elif evt.type == JOYAXISMOTION and evt.instance_id == 0 and evt.axis == 1:
            if -1.1 < evt.value < -0.1:
                self.select(self.cursorIdx - 1, False)
            elif 0.1 < evt.value < 1.1:
                self.select(self.cursorIdx + 1, False)


class Menu(_MenuBackScene):
    def __init__(self, opts, *,
                 on_demo, on_solo, on_duel,
                 on_options, on_controls,
                 on_history, on_credits, on_quit):
        super(Menu, self).__init__(opts, 'menu/menu.png')
        self.on_demo = on_demo
        self.on_solo = on_solo
        self.on_duel = on_duel
        self.on_options = on_options
        self.on_controls = on_controls
        self.on_history = on_history
        self.on_credits = on_credits
        self.on_quit = on_quit
        sz = int(7 * Game.scy)
        col = Theme.MENU_TXT
        txt = Txt(sz, 'SELECT', col, (136 * Game.scx, 86 * Game.scy), self)
        txt.rect.x = Game.screen[0] / 2 - txt.rect.w / 2 - 3 * Game.scx
        txt = Txt(sz, 'OPTION', col, (136 * Game.scx, txt.rect.bottom + 2 * Game.scy), self)
        txt.rect.x = Game.screen[0] / 2 - txt.rect.w / 2 - 3 * Game.scx
        #
        x = 112 * Game.scx
        txt = Txt(sz, '0 DEMO', Theme.BLACK, (x, txt.rect.bottom + 10 * Game.scy), self)
        self.items.append(txt)

        txt = Txt(sz, '1 ONE PLAYER', col, (x, txt.rect.bottom + 2 * Game.scy), self)
        self.items.append(txt)

        txt = Txt(sz, '2 TWO PLAYERS', col, (x, txt.rect.bottom + 2 * Game.scy), self)
        self.items.append(txt)

        txt = Txt(sz, '3 OPTIONS', col, (x, txt.rect.bottom + 2 * Game.scy), self)
        self.items.append(txt)

        txt = Txt(sz, '4 CONTROLS', col, (x, txt.rect.bottom + 2 * Game.scy), self)
        self.items.append(txt)

        txt = Txt(sz, '5 STORY', col, (x, txt.rect.bottom + 2 * Game.scy), self)
        self.items.append(txt)

        txt = Txt(sz, '6 CREDITS', col, (x, txt.rect.bottom + 2 * Game.scy), self)
        self.items.append(txt)

        txt = Txt(sz, '7 QUIT', col, (x, txt.rect.bottom + 2 * Game.scy), self)
        self.items.append(txt)

    def select(self, idx, run):
        super().select(idx, run)
        if run:
            if self.cursorIdx == 0:
                self.on_demo()
            elif self.cursorIdx == 1:
                self.on_solo()
            elif self.cursorIdx == 2:
                self.on_duel()
            elif self.cursorIdx == 3:
                self.on_options()
            elif self.cursorIdx == 4:
                self.on_controls()
            elif self.cursorIdx == 5:
                self.on_history()
            elif self.cursorIdx == 6:
                self.on_credits()
            elif self.cursorIdx == 7:
                self.on_quit()

    def process_event(self, evt):
        super().process_event(evt)
        if evt.type == KEYDOWN:
            if evt.key == K_0:
                self.select(0, True)
            elif evt.key == K_1:
                self.select(1, True)
            elif evt.key == K_2:
                self.select(2, True)
            elif evt.key == K_3:
                self.select(3, True)
            elif evt.key == K_4:
                self.select(4, True)
            elif evt.key == K_5:
                self.select(5, True)
            elif evt.key == K_6:
                self.select(6, True)
            elif evt.key in (K_7, K_ESCAPE):
                self.select(7, True)


def area(color, lbl, border_width=2):
    return Rectangle(0, 0, Game.chw, Game.chh, color, border_width, lbl)


MORT_RIGHT_BORDER = 34


class BattleState(enum.Enum):
    in_progress = enum.auto()
    win = enum.auto()
    loose = enum.auto()


class Battle(EmptyScene):
    chrono: int = 0  # current millisecond
    chronoOn: bool = False
    chronometre: int = 60  # seconds
    entree: bool = True
    sorcier: bool = False
    entreesorcier: bool = False
    lancerintro: bool = True
    bState: BattleState = BattleState.in_progress

    def __init__(self, opts, *, on_esc, on_next, on_finish):
        super(Battle, self).__init__(opts)
        self.on_esc = on_esc
        self.on_finish = on_finish
        self.on_next = on_next
        back = get_img(f'stage/{Game.decor}.gif')
        if Game.country == 'USA':
            back = back.copy()
            if Game.decor in ('foret', 'plaine'):
                logo = get_img('stage/logoDS2.png')
                if Game.decor == 'foret':
                    back.blit(logo, (59 * Game.scx, 16 * Game.scy))
                elif Game.decor == 'plaine':
                    back.blit(logo, (59 * Game.scx, 14 * Game.scy))
            if Game.decor in ('arene', 'trone'):
                logo = get_img('stage/logoDS3.png')
                back.blit(logo, (59 * Game.scx, 16 * Game.scy))
        # noinspection PyTypeChecker
        self.clear(None, back)
        self.debugAttArea = False
        if self.opts.debug > 1:
            self.jAstate = Txt.Debug(loc2pxX(10), 0)
            self.jBstate = Txt.Debug(loc2pxX(25), 0)
            self.jAlevier = Txt.Debug(loc2pxX(10), self.jAstate.rect.bottom)
            self.jBlevier = Txt.Debug(loc2pxX(25), self.jBstate.rect.bottom)
            self.jAtemps = Txt.Debug(loc2pxX(10), self.jAlevier.rect.bottom)
            self.jBtemps = Txt.Debug(loc2pxX(25), self.jBlevier.rect.bottom)
            self.debugTemps = Txt.Debug(loc2pxX(18), 0)
            self.distance = Txt.Debug(loc2pxX(18), self.jBtemps.rect.top)
            # noinspection PyTypeChecker
            self.add(self.jAstate, self.jAlevier, self.jAtemps,
                     self.jBstate, self.jBlevier, self.jBtemps,
                     self.debugTemps, self.distance, layer=99)
            if self.opts.debug > 2:
                self.jAframe = Txt.Debug(loc2pxX(10), self.jAtemps.rect.bottom)
                self.jBframe = Txt.Debug(loc2pxX(25), self.jBtemps.rect.bottom)
                # noinspection PyTypeChecker
                self.add(self.jAframe, self.jBframe, layer=99)

            self.jAAtt = area(Theme.RED, 'A', border_width=5)
            self.jAF = area(Theme.YELLOW, 'F')
            self.jAT = area(Theme.RED, 'T')
            self.jAM = area(Theme.GREEN, 'M')
            self.jAG = area(Theme.PURPLE, 'G')
            self.jBAtt = area(Theme.RED, 'A', border_width=5)
            self.jBF = area(Theme.YELLOW, 'F')
            self.jBT = area(Theme.RED, 'T')
            self.jBM = area(Theme.GREEN, 'M')
            self.jBG = area(Theme.PURPLE, 'G')
            self.attAreas = Group(
                self.jAAtt, self.jAF, self.jAT, self.jAM, self.jAG,
                self.jBAtt, self.jBF, self.jBT, self.jBM, self.jBG)
        # noinspection PyTypeChecker
        self.add(
            StaticSprite((0, 104 * Game.scy),
                         f'stage/{Game.decor}ARBREG.gif'),
            StaticSprite((272 * Game.scx, 104 * Game.scy),
                         f'stage/{Game.decor}ARBRED.gif'),
            layer=5)

        self.joueurA = Barbarian(opts, loc2pxX(1), loc2pxY(14),
                                 'spritesA', rtl=False)
        self.joueurA.infoCoup = 1
        self.joueurB = Barbarian(opts, loc2pxX(36), loc2pxY(14),
                                 f'spritesB/spritesB{Game.ia}', rtl=True)
        sz = Game.chh
        if Game.partie == Partie.solo:
            Txt(sz, 'ONE  PLAYER', Theme.TXT, loc(16, 25), self)
        elif Game.partie == Partie.vs:
            Txt(sz, 'TWO PLAYERS', Theme.TXT, loc(16, 25), self)
        elif Game.partie == Partie.demo:
            Txt(sz, 'DEMO', Theme.TXT, loc(18, 25), self)

        self.txtScoreA = Txt(sz, f'{Game.scoreA:05}', Theme.TXT, loc(13, 8),
                             self, cached=False)
        self.txtScoreB = Txt(sz, f'{Game.scoreB:05}', Theme.TXT, loc(24, 8),
                             self, cached=False)

        if Game.partie == Partie.vs:
            self.txtChronometre = Txt(sz, f'{self.chronometre:02}',
                                      Theme.TXT, loc(20, 8), self)
        else:
            Txt(sz, f'{Game.ia:02}', Theme.TXT, loc(20, 8), self)
        # noinspection PyTypeChecker
        self.add(self.joueurA, self.joueurB, layer=1)
        self.joueurA.animate('avance')
        self.joueurB.animate('avance')
        self.serpentA = AnimatedSprite((11 * Game.scx, 22 * Game.scy),
                                       anims.serpent(), self)
        self.serpentB = AnimatedSprite((275 * Game.scx, 22 * Game.scy),
                                       anims.serpent_rtl(), self)
        self.temps = 0
        self.tempsfini = False
        self.inverse = False
        self.soncling = cycle(['block1.ogg', 'block2.ogg', 'block3.ogg'])
        self.songrogne = cycle([0, 0, 0, 'grogne1.ogg', 0, 0, 'grogne1.ogg'])
        self.sontouche = cycle(['touche.ogg', 'touche2.ogg', 'touche3.ogg'])
        self.vieA0 = AnimatedSprite((43 * Game.scx, 0), anims.vie(), self)
        self.vieA1 = AnimatedSprite((43 * Game.scx, 11 * Game.scy), anims.vie(), self)
        self.vieB0 = AnimatedSprite((276 * Game.scx, 0), anims.vie(), self)
        self.vieB1 = AnimatedSprite((276 * Game.scx, 11 * Game.scy), anims.vie(), self)
        self.joueurA.on_vie_changed = self.on_vieA_changed
        self.joueurA.on_score = self.on_scoreA
        self.joueurA.on_mort = self.on_mort
        self.joueurB.on_vie_changed = self.on_vieB_changed
        self.joueurB.on_score = self.on_scoreB
        self.joueurB.on_mort = self.on_mort
        #
        self.gnome = False
        self.gnomeSprite = AnimatedSprite((0, loc2pxY(20)), anims.gnome())

    def finish(self):
        if self.opts.sound:
            mixer.stop()
        self.on_finish()

    def next_stage(self):
        if self.opts.sound:
            mixer.stop()
        self.on_next()

    def process_event(self, evt):
        if evt.type == KEYUP and evt.key == K_ESCAPE:
            if self.bState == BattleState.in_progress:
                if self.opts.sound:
                    mixer.stop()
                self.on_esc()
            else:
                self.finish()
            return
        if evt.type == KEYUP and evt.key == K_F12 and self.opts.debug > 1:
            self.debugAttArea = not self.debugAttArea
            if self.debugAttArea:
                self.add(self.attAreas, layer=99)
            else:
                self.remove(self.attAreas)

        if Game.partie == Partie.demo:
            if is_any_key_pressed(evt):
                self.on_esc()
            return
        if self.bState != BattleState.in_progress and is_any_key_pressed(evt):
            self.finish()
            return

        keyState = (True if evt.type == KEYDOWN else
                    False if evt.type == KEYUP else
                    None)
        if keyState is not None:
            # Joueur A
            if evt.key in (K_UP, K_KP_8):
                self.joueurA.pressedUp = keyState
            elif evt.key in (K_DOWN, K_KP_2):
                self.joueurA.pressedDown = keyState
            elif evt.key in (K_LEFT, K_KP_4):
                self.joueurA.pressedLeft = keyState
            elif evt.key in (K_RIGHT, K_KP_6):
                self.joueurA.pressedRight = keyState
            elif evt.key in (K_RSHIFT, K_KP_0):
                self.joueurA.pressedFire = keyState
            # Joueur B
            elif evt.key == K_i:
                self.joueurB.pressedUp = keyState
            elif evt.key == K_j:
                self.joueurB.pressedLeft = keyState
            elif evt.key == K_k:
                self.joueurB.pressedDown = keyState
            elif evt.key == K_l:
                self.joueurB.pressedRight = keyState
            elif evt.key == K_SPACE:
                self.joueurB.pressedFire = keyState

        elif evt.type == JOYAXISMOTION:
            joueur = self.joueurA if evt.instance_id == 0 else self.joueurB
            if evt.axis == 0:
                if -1.1 < evt.value < -0.1:
                    joueur.pressedLeft = True
                elif 0.1 < evt.value < 1.1:
                    joueur.pressedRight = True
                else:
                    joueur.pressedLeft = False
                    joueur.pressedRight = False
            elif evt.axis == 1:
                if -1.1 < evt.value < -0.1:
                    joueur.pressedUp = True
                elif 0.1 < evt.value < 1.1:
                    joueur.pressedDown = True
                else:
                    joueur.pressedDown = False
                    joueur.pressedUp = False

        keyState = (True if evt.type == JOYBUTTONDOWN else
                    False if evt.type == JOYBUTTONUP else
                    None)
        if keyState is not None:
            joueur = self.joueurA if evt.instance_id == 0 else self.joueurB
            if 0 <= evt.button <= 3:
                joueur.pressedFire = keyState
            elif evt.button == 7:
                joueur.pressedDown = keyState
            elif evt.button == 6:
                joueur.pressedUp = keyState
            elif evt.button == 4:
                joueur.pressedLeft = keyState
            elif evt.button == 5:
                joueur.pressedRight = keyState

    def animate_gnome(self):
        if not self.gnome:
            self.gnome = True
            # noinspection PyTypeChecker
            self.add(self.gnomeSprite, layer=4)
            self.gnomeSprite.animate('gnome')

    def start_sorcier(self):
        self.sorcier = True
        self.inverse = True
        self.joueurA.animate('avance')
        self.joueurA.x = loc2pxX(36)
        if not self.joueurA.rtl:
            self.joueurA.turn_around(True)
        self.gnome = False
        self.joueurA.sortie = False
        self.joueurA.attaque = False
        self.entreesorcier = True
        self.joueurB = Sorcier(loc2pxX(9), loc2pxY(14))
        self.joueurB.occupe_state(State.debout, self.temps)
        # noinspection PyTypeChecker
        self.add(self.joueurB,
                 StaticSprite((114 * Game.scx, 95 * Game.scy),
                              'fill', w=16, h=6, fill=Theme.BLACK),
                 StaticSprite((109 * Game.scx, 100 * Game.scy),
                              'fill', w=27, h=15.1, fill=Theme.BLACK),
                 layer=0)
        self.on_vieA_changed(0)
        self.on_vieB_changed(0)

    def _degats(self):
        # degats sur joueurA
        ja = self.joueurA
        jb = self.joueurB
        degat = False
        if self.sorcier:
            if (ja.xLoc < 33 and (
                    (jb.yAtt == ja.yT and ja.xT <= jb.xAtt <= ja.xT + 2)
                    or (jb.yAtt == ja.yG and ja.xG <= jb.xAtt <= ja.xG + 2)
                    or (jb.yAtt == ja.yM and ja.xM <= jb.xAtt <= ja.xM + 2)
            )):
                if self.bState == BattleState.loose or ja.state == State.mortSORCIER:
                    return
                ja.occupe_state(State.mortSORCIER, self.temps)
                jb.occupe_state(State.sorcierFINI, self.temps)
                return
        else:
            degat = ja.degat(jb)
        if not degat and not ja.occupe and not self.entreesorcier:
            self._clavier()

    def _clavier(self):
        self.joueurA.clavierX = 7
        self.joueurA.clavierY = 7
        self.joueurA.levier = Levier.neutre

        if Game.partie != Partie.demo:
            self.joueurA.clavier()
        else:
            if ai.demo_joueurA(self.joueurA, self.joueurB, self.temps):
                return

        # redirection suivant les touches
        if self.joueurA.levier != Levier.neutre:
            self.joueurA.action(self.temps)
        else:
            self.joueurA.action_debut(self.temps)

    def _gestion(self):
        self.joueurA.gestion(self.temps, self.joueurB,
                             self.soncling, self.songrogne, self.sontouche)
        #
        if self.joueurA.state == State.retourne:
            if self.temps == self.joueurA.reftemps + 16:
                self.inverse = self.joueurA.rtl

        elif self.joueurA.state == State.vainqueurKO:
            if self.temps == self.joueurA.reftemps + 231:
                self.animate_gnome()

        elif self.joueurA.state == State.mortdecap:
            if self.temps == self.joueurA.reftemps + 126:
                self.animate_gnome()

        elif self.joueurA.state == State.mortSORCIER:
            if self.temps > self.joueurA.reftemps + 86:
                self.joueurA.state = State.sorcierFINI
                self.add(self._center_txt('Your end has come!'))
                self.bState = BattleState.loose
            elif self.temps == self.joueurA.reftemps:
                self.joueurB.stopped = True
                self.joueurA.animate('mortSORCIER')

    @staticmethod
    def _center_txt(msg):
        txt = Txt(Game.chh, msg,
                  color=(34, 34, 153), bgcolor=Theme.BLACK)
        txt.rect.topleft = (Game.screen[0] / 2 - txt.rect.w / 2, loc2pxY(11))
        bg = StaticSprite((0, 0), 'fill',
                          w=(txt.rect.w + 2 * Game.chw) / Game.scx,
                          h=(txt.rect.h + 2 * Game.chh) / Game.scy,
                          fill=Theme.BLACK)
        bg.rect.topleft = (txt.rect.topleft[0] - Game.chw,
                           txt.rect.topleft[1] - Game.chh)
        return bg, txt

    def _win(self):
        self.joueurB.stopped = True
        self.joueurB.animate_sang(loc2pxX(self.joueurA.yAtt))
        self.joueurB.kill()
        self.joueurB.occupe_state(State.mortSORCIER, self.temps)
        self.joueurA.occupe_state(State.fini, self.temps)
        self.joueurA.set_frame('vainqueur', 2)
        self.joueurA.x = loc2pxX(17)
        # noinspection PyTypeChecker
        self.add(
            StaticSprite((self.joueurA.rect.right, loc2pxY(17)),
                         'sprites/marianna.gif'),
            StaticSprite((186 * Game.scx, 95 * Game.scy), 'fill',
                         w=15, h=20, fill=Theme.BLACK),
            StaticSprite((185 * Game.scx, 113 * Game.scy), 'fill',
                         w=18, h=2.1, fill=Theme.BLACK),
            self._center_txt('Thanks big boy.'))
        self.bState = BattleState.win

    def _joueur2(self):
        # debut joueur 2
        degat = self.joueurB.degat(self.joueurA)
        if self.sorcier and degat:
            self._win()
            return

        if not degat and not self.joueurB.occupe:
            self._clavierB()

    def _clavierB(self):
        self.joueurB.clavierX = 7
        self.joueurB.clavierY = 7
        self.joueurB.levier = Levier.neutre

        if Game.partie == Partie.vs:
            self.joueurB.clavier()
        else:
            if ai.joueurB(Game.partie == Partie.demo, Game.ia,
                          self.joueurA, self.joueurB, self.temps):
                return
        # redirection suivant les touches
        if self.joueurB.levier != Levier.neutre:
            self.joueurB.action(self.temps)
        else:
            self.joueurB.action_debut(self.temps)

    def _gestionB(self):
        self.joueurB.gestion(self.temps, self.joueurA,
                             self.soncling, self.songrogne, self.sontouche)
        #
        if self.joueurB.state == State.vainqueurKO:
            if self.temps > self.joueurB.reftemps + 230:
                self.animate_gnome()

        elif self.joueurB.state == State.mortdecap:
            if self.temps == self.joueurB.reftemps + 126:
                self.animate_gnome()

    def _colision(self, ja: Barbarian, jb: Barbarian):
        # ***************************************
        # ***********   COLISION   **************
        # ***************************************
        if (abs(jb.xLoc - ja.xLoc) < 3
                and not (ja.state == State.saute and jb.state == State.rouladeAV)
                and not (jb.state == State.saute and ja.state == State.rouladeAV)):
            # pour empecher que A entre dans B
            if (ja.levier == ja.avance_levier()
                    or ja.state in (State.rouladeAV, State.decapite,
                                    State.debout, State.coupdepied)):
                if ja.xLocPrev != ja.xLoc:
                    ja.x = loc2pxX(ja.xLoc - (-1 if ja.rtl else 1))

            # pour empecher que B entre dans A
            if (self.sorcier or jb.levier == jb.avance_levier()
                    or jb.state in (State.rouladeAV, State.decapite,
                                    State.debout, State.coupdepied)):
                if jb.xLocPrev != jb.xLoc:
                    jb.x = loc2pxX(jb.xLoc - (-1 if jb.rtl else 1))

        left, right = self._colision_borders(ja, jb)
        if ja.xLoc < left:
            ja.x = loc2pxX(left)
        elif ja.xLoc > right:
            ja.x = loc2pxX(right)
        #
        left, right = self._colision_borders(jb, ja)
        if jb.xLoc < left:
            jb.x = loc2pxX(left)
        elif jb.xLoc > right:
            jb.x = loc2pxX(right)

    def _colision_borders(self, joueur: Barbarian, opponent: Barbarian):
        return ((0, 40) if any((self.entree, self.entreesorcier,
                                joueur.sortie, opponent.sortie)) else
                (5, 32) if joueur.state == State.retourne else
                (8, 32) if joueur.rtl else
                (5, 29))

    def on_vieA_changed(self, num):
        self.vieA0.set_frame('vie', max(0, min(6, 6 - num)))
        self.vieA1.set_frame('vie', max(0, min(6, 12 - num)))
        self.serpentA.animate('bite')

    def on_vieB_changed(self, num):
        self.vieB0.set_frame('vie_rtl', max(0, min(6, 6 - num)))
        self.vieB1.set_frame('vie_rtl', max(0, min(6, 12 - num)))
        self.serpentB.animate('bite')

    def on_scoreA(self, increment):
        Game.scoreA += increment
        self.txtScoreA.msg = f'{Game.scoreA:05}'

    def on_scoreB(self, increment):
        Game.scoreB += increment
        self.txtScoreB.msg = f'{Game.scoreB:05}'

    def on_mort(self, mort: Barbarian):
        self.chronoOn = False
        # noinspection PyTypeChecker
        self.change_layer(mort, 2)

    def _gnome(self):
        if self.joueurA.state in (State.mort, State.mortdecap):
            mort, vainqueur = self.joueurA, self.joueurB
        elif self.joueurB.state in (State.mort, State.mortdecap):
            mort, vainqueur = self.joueurB, self.joueurA
        else:
            return
        gnome = self.gnomeSprite

        if mort.state == State.mort:
            if (gnome.rect.left >= mort.rect.right - Game.chw
                    and mort.anim != 'mortgnome'):
                mort.topleft = mort.rect.topleft
                mort.animate('mortgnome')
        elif mort.state == State.mortdecap:
            if (gnome.rect.left >= mort.rect.right - Game.chw
                    and mort.anim != 'mortdecapgnome'):
                mort.topleft = mort.rect.topleft
                mort.animate('mortdecapgnome')
            if mort.tete.alive():
                if gnome.rect.right >= mort.tete.rect.center[0]:
                    mort.animate_football()
                if mort.tete.rect.left > Game.screen[0]:
                    mort.stop_football()
        if gnome.alive() and mort.xLoc > MORT_RIGHT_BORDER:
            gnome.kill()
            mort.kill()
            if Game.partie == Partie.vs:
                vainqueur.bonus = True
            else:
                vainqueur.sortie = True
                vainqueur.occupe = False
                vainqueur.animate('recule')

    def tick_chrono(self, current_time, ja: Barbarian, jb: Barbarian):
        if self.chrono == 0:
            self.chrono = current_time
        elif current_time > self.chrono:
            self.chrono += 1000
            self.chronometre -= 1
            if self.chronometre < 1:
                self.chronometre = 0
                self.chronoOn = False
                if Game.partie == Partie.vs:
                    ja.sortie = jb.sortie = True
                    ja.occupe = jb.occupe = False
                    self.tempsfini = True
                    ja.animate('recule')
                    jb.animate('recule')
            self.txtChronometre.msg = f'{self.chronometre:02}'

    def joueurX_bonus(self, winner: Barbarian, dead: Barbarian):
        if self.chronometre > 0:
            winner.on_score(10)
            self.chronometre -= 1
            self.txtChronometre.msg = f'{self.chronometre:02}'
        elif dead.xLoc >= MORT_RIGHT_BORDER:
            winner.bonus = False
            winner.sortie = True
            winner.occupe = False
            winner.animate('recule')

    def do_entree(self, jax, jbx):
        if self.serpentA.anim == 'idle' and jax >= 3:
            self.serpentA.animate('bite')
            self.serpentB.animate('bite')
        if jax >= 13:
            self.joueurA.x = loc2pxX(13)
        if jbx <= 22:
            self.joueurB.x = loc2pxX(22)
        if jax >= 13 or jbx <= 22:
            self.joueurA.set_frame('debout', 0)
            self.joueurB.set_frame('debout', 0)
            self.entree = False
            if Game.partie == Partie.vs:
                self.chronoOn = True

    def check_sortiedA(self, jax, jbx):
        if not self.tempsfini:
            if jbx >= MORT_RIGHT_BORDER and (jax <= 0 or 38 <= jax):
                if Game.partie in (Partie.demo, Partie.vs):
                    self.finish()
                elif Game.partie == Partie.solo and Game.ia < 7:
                    self.next_stage()
                elif Game.partie == Partie.solo:
                    self.start_sorcier()
        elif (jax < 2 and 38 < jbx) or (jbx < 2 and 38 < jax):
            self.next_stage()

    def check_sortiedB(self, jax, jbx):
        if not self.tempsfini:
            if jax >= MORT_RIGHT_BORDER and (jbx <= 0 or 38 <= jbx):
                self.finish()

    def update(self, current_time, *args):
        ja = self.joueurA
        jb = self.joueurB
        ja.xLocPrev = ja.xLoc  # for collision
        jb.xLocPrev = jb.xLoc  # for collision
        super(Battle, self).update(current_time, *args)
        if self.bState != BattleState.in_progress:
            return
        if self.chronoOn:
            self.tick_chrono(current_time, ja, jb)
        #
        self.temps += 1
        self.update_internal(ja, jb)
        #
        if self.opts.debug > 1:
            self.debug(ja, jb)

    def update_internal(self, ja, jb):
        if ja.bonus:
            self.joueurX_bonus(ja, jb)
        if jb.bonus:
            self.joueurX_bonus(jb, ja)
        if self.lancerintro:
            self.lancerintro = False
            snd_play('prepare.ogg')

        if self.entree:
            self.do_entree(ja.xLoc, jb.xLoc)
            return  #
        if ja.sortie:
            self.check_sortiedA(ja.xLoc, jb.xLoc)
            return  #
        if jb.sortie:
            self.check_sortiedB(ja.xLoc, jb.xLoc)
            return  #
        if self.gnome:
            self._gnome()
            return  #

        if self.entreesorcier:
            if self.joueurA.xLoc <= 33:
                self.entreesorcier = False
                self.joueurB.occupe_state(State.sorcier, self.temps)

        self._degats()
        self._gestion()
        self._joueur2()
        self._gestionB()
        self._colision(ja, jb)

    def debug(self, ja, jb):
        self.jAstate.msg = f'AS: {ja.state}'
        self.jAlevier.msg = f'AL: {ja.levier}'
        self.jAtemps.msg = f'AT: {ja.reftemps} ({self.temps - ja.reftemps})'
        self.jBstate.msg = f'BS: {jb.state}'
        self.jBlevier.msg = f'BL: {jb.levier}'
        self.jBtemps.msg = f'BT: {jb.reftemps} ({self.temps - jb.reftemps})'
        self.debugTemps.msg = f'T: {self.temps}'
        self.distance.msg = f'A <- {abs(jb.xLoc - ja.xLoc):>2} -> B'
        if self.debugAttArea:
            self.jAAtt.move_to(loc2pxX(ja.xAtt), loc2pxY(ja.yAtt))
            self.jAF.move_to(loc2pxX(ja.xF), loc2pxY(ja.yF))
            self.jAT.move_to(loc2pxX(ja.xT), loc2pxY(ja.yT))
            self.jAM.move_to(loc2pxX(ja.xM), loc2pxY(ja.yM))
            self.jAG.move_to(loc2pxX(ja.xG), loc2pxY(ja.yG))
            #
            self.jBAtt.move_to(loc2pxX(jb.xAtt), loc2pxY(jb.yAtt))
            self.jBF.move_to(loc2pxX(jb.xF), loc2pxY(jb.yF))
            self.jBT.move_to(loc2pxX(jb.xT), loc2pxY(jb.yT))
            self.jBM.move_to(loc2pxX(jb.xM), loc2pxY(jb.yM))
            self.jBG.move_to(loc2pxX(jb.xG), loc2pxY(jb.yG))
        if self.opts.debug > 2:
            self.jAframe.msg = (f'{ja.frameNum + 1} / {len(ja.frames)}'
                                f' ({ja.frame.name})')
            self.jBframe.msg = (f'{jb.frameNum + 1} / {len(jb.frames)}'
                                f' ({jb.frame.name})')


class HiScores(_MenuBackScene):
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+'
    charIdx = 0
    cursorLoc = 0

    def __init__(self, opts, *, on_finish):
        super(HiScores, self).__init__(opts, 'menu/menu.png')
        self.on_finish = on_finish
        heroes = StaticSprite((0, 86 * Game.scy), 'menu/heroes.png', self)
        heroes.rect.x = Game.screen[0] / 2 - heroes.rect.w / 2 - 3 * Game.scx
        #
        hiscores = Game.load_hiscores()
        self.pos = 6
        for i, (score, _) in enumerate(hiscores):
            if Game.scoreA > score:
                hiscores.insert(i, (Game.scoreA, 'AAA'))
                self.pos = i
                break
        if self.pos < 6:
            hiscores = hiscores[0:6]
            top = 114 * Game.scy
        else:
            hiscores.append((Game.scoreA, '---'))
            top = 108 * Game.scy
        #
        self.sz = int(8 * Game.scy)
        for i, (score, name) in enumerate(hiscores):
            col = Theme.LEADER_TXT if i == 0 else Theme.TXT
            txt = Txt(self.sz, f'{name:3} {score:05}', col,
                      (121 * Game.scx, top),
                      self, cached=False)
            top = txt.rect.bottom + 4 * Game.scy
            if i == self.pos:
                self.txt = txt
                self.cursor = Rectangle(
                    self.txt.rect.left - 1 * Game.scx - 1,
                    self.txt.rect.top - 1 * Game.scy - 1,
                    self.sz + 2 * Game.scx + 1,
                    self.sz + 2 * Game.scy + 1,
                    col, border_width=int(1 * Game.scx))
        self.hiscores = hiscores
        if self.pos < 6:
            self.add(self.cursor)
        pygame.key.set_repeat(600, 100)

    def finish(self):
        pygame.key.set_repeat(0, 0)  # disable
        self.on_finish()

    def on_up_pressed(self):
        self.charIdx += 1
        if self.charIdx >= len(self.chars):
            self.charIdx = 0
        self.txt.msg = (self.txt.msg[0:self.cursorLoc] +
                        self.chars[self.charIdx] +
                        self.txt.msg[self.cursorLoc + 1:])

    def on_down_pressed(self):
        self.charIdx -= 1
        if self.charIdx < 0:
            self.charIdx = len(self.chars) - 1
        self.txt.msg = (self.txt.msg[0:self.cursorLoc] +
                        self.chars[self.charIdx] +
                        self.txt.msg[self.cursorLoc + 1:])

    def on_fire_pressed(self):
        self.cursor.move_to(self.cursor.rect.x + self.sz,
                            self.cursor.rect.y)
        self.charIdx = 0
        self.hiscores[self.pos] = (self.hiscores[self.pos][0],
                                   self.txt.msg[0:3])
        self.cursorLoc += 1
        if self.cursorLoc > 2:
            Game.save_hiscores(self.hiscores)
            self.finish()

    def process_event(self, evt: Event):
        if self.pos >= 6:
            if ((evt.type == JOYBUTTONDOWN and evt.instance_id == 0)
                    or (evt.type == K_DOWN and evt.key in (
                            K_ESCAPE, K_RSHIFT, K_KP_0, K_RETURN, K_KP_ENTER))):
                self.on_finish()
            return

        if evt.type == KEYDOWN:
            if evt.unicode and evt.unicode.upper() in self.chars:
                self.txt.msg = (self.txt.msg[0:self.cursorLoc] +
                                evt.unicode.upper() +
                                self.txt.msg[self.cursorLoc + 1:])
                self.charIdx = self.chars.index(evt.unicode.upper())

            elif evt.key in (K_UP, K_KP_8):
                self.on_up_pressed()

            elif evt.key in (K_DOWN, K_KP_2):
                self.on_down_pressed()

            elif evt.key in (K_LEFT, K_KP_4):
                self.cursorLoc -= 1
                if self.cursorLoc < 0:
                    self.cursorLoc = 0
                else:
                    self.cursor.move_to(self.cursor.rect.x - self.sz,
                                        self.cursor.rect.y)
                    self.charIdx = self.chars.index(self.txt.msg[self.cursorLoc])

            elif evt.key in (K_RIGHT, K_KP_6):
                self.cursorLoc += 1
                if self.cursorLoc > 2:
                    self.cursorLoc = 2
                else:
                    self.cursor.move_to(self.cursor.rect.x + self.sz,
                                        self.cursor.rect.y)
                    self.charIdx = self.chars.index(self.txt.msg[self.cursorLoc])

            elif evt.key in (K_RSHIFT, K_KP_0, K_RETURN, K_KP_ENTER):
                self.on_fire_pressed()

        elif evt.type == JOYBUTTONDOWN and evt.instance_id == 0:
            self.on_fire_pressed()
        elif evt.type == JOYAXISMOTION and evt.instance_id == 0 and evt.axis == 1:
            if -1.1 < evt.value < -0.1:
                self.on_up_pressed()
            elif 0.1 < evt.value < 1.1:
                self.on_down_pressed()


class Version(_MenuBackScene):
    def __init__(self, opts, *, on_display, on_back):
        super(Version, self).__init__(opts, 'menu/menu.png')
        self.on_display = on_display
        self.on_back = on_back
        sz = int(7 * Game.scy)
        col = Theme.MENU_TXT
        txt = Txt(sz, 'SELECT', col, (136 * Game.scx, 86 * Game.scy), self)
        txt.rect.x = Game.screen[0] / 2 - txt.rect.w / 2 - 3 * Game.scx
        txt = Txt(sz, 'VERSION', col, (136 * Game.scx, txt.rect.bottom + 2 * Game.scy), self)
        txt.rect.x = Game.screen[0] / 2 - txt.rect.w / 2 - 3 * Game.scx
        #
        x = 112 * Game.scx
        txt = Txt(sz, '1 EUROPE', Theme.BLACK, (x, txt.rect.bottom + 10 * Game.scy), self)
        self.items.append(txt)

        txt = Txt(sz, '2 USA', col, (x, txt.rect.bottom + 2 * Game.scy), self)
        self.items.append(txt)

        txt = Txt(sz, '4 BACK', col, (x, txt.rect.bottom + sz + 4 * Game.scy), self)
        self.items.append(txt)

    def select(self, idx, run):
        super().select(idx, run)
        if run:
            if self.cursorIdx == 0:
                Game.country = 'EUROPE'
                self.on_display()
            elif self.cursorIdx == 1:
                Game.country = 'USA'
                self.on_display()
            elif self.cursorIdx == 2:
                self.on_back()

    def process_event(self, evt):
        super().process_event(evt)
        if evt.type == KEYDOWN:
            if evt.key == K_1:
                self.select(0, True)
            elif evt.key == K_2:
                self.select(1, True)
            elif evt.key in (K_4, K_ESCAPE):
                self.select(2, True)


class Display(_MenuBackScene):
    def __init__(self, opts, *, on_fullscreen, on_window, on_back):
        super(Display, self).__init__(opts, 'menu/menu.png')
        self.on_fullscreen = on_fullscreen
        self.on_window = on_window
        self.on_back = on_back
        sz = int(7 * Game.scy)
        col = Theme.MENU_TXT
        txt = Txt(sz, 'SELECT', col, (136 * Game.scx, 86 * Game.scy), self)
        txt.rect.x = Game.screen[0] / 2 - txt.rect.w / 2 - 3 * Game.scx
        txt = Txt(sz, 'DISPLAY', col,
                  (136 * Game.scx, txt.rect.bottom + 2 * Game.scy), self)
        txt.rect.x = Game.screen[0] / 2 - txt.rect.w / 2 - 3 * Game.scx
        #
        x = 112 * Game.scx
        txt = Txt(sz, '1 FULLSCREEN', Theme.BLACK, (x, txt.rect.bottom + 10 * Game.scy), self)
        self.items.append(txt)

        txt = Txt(sz, '2 WINDOWS', col, (x, txt.rect.bottom + 2 * Game.scy), self)
        self.items.append(txt)

        txt = Txt(sz, '4 BACK', col, (x, txt.rect.bottom + sz + 4 * Game.scy), self)
        self.items.append(txt)

    def select(self, idx, run):
        super().select(idx, run)
        if run:
            if self.cursorIdx == 0:
                self.on_fullscreen()
            elif self.cursorIdx == 1:
                self.on_window()
            elif self.cursorIdx == 2:
                self.on_back()

    def process_event(self, evt):
        super().process_event(evt)
        if evt.type == KEYDOWN:
            if evt.key == K_1:
                self.select(0, True)
            elif evt.key == K_2:
                self.select(1, True)
            elif evt.key in (K_4, K_ESCAPE):
                self.select(2, True)


class SelectStage(_MenuBackScene):
    def __init__(self, opts, *, on_start, on_back):
        super(SelectStage, self).__init__(opts, 'menu/menu.png')
        self.on_start = on_start
        self.on_back = on_back
        sz = int(7 * Game.scy)
        col = Theme.MENU_TXT
        txt = Txt(sz, 'SELECT', col, (136 * Game.scx, 86 * Game.scy), self)
        txt.rect.x = Game.screen[0] / 2 - txt.rect.w / 2 - 3 * Game.scx
        txt = Txt(sz, 'STAGE', col, (136 * Game.scx, txt.rect.bottom + 2 * Game.scy), self)
        txt.rect.x = Game.screen[0] / 2 - txt.rect.w / 2 - 3 * Game.scx

        x = 112 * Game.scx
        txt = Txt(sz, '1 WASTELAND', Theme.BLACK, (x, txt.rect.bottom + 10 * Game.scy), self)
        self.items.append(txt)
        txt = Txt(sz, '2 FOREST', col, (x, txt.rect.bottom + 2 * Game.scy), self)
        self.items.append(txt)
        txt = Txt(sz, '3 THRONE', col, (x, txt.rect.bottom + 2 * Game.scy), self)
        self.items.append(txt)
        txt = Txt(sz, '4 ARENA', col, (x, txt.rect.bottom + 2 * Game.scy), self)
        self.items.append(txt)
        txt = Txt(sz, '6 BACK', col, (x, txt.rect.bottom + sz + 4 * Game.scy), self)
        self.items.append(txt)

    def select(self, idx, run):
        super().select(idx, run)
        if run:
            if self.cursorIdx == 0:
                Game.decor = 'plaine'
                self.on_start()
            elif self.cursorIdx == 1:
                Game.decor = 'foret'
                self.on_start()
            elif self.cursorIdx == 2:
                Game.decor = 'trone'
                self.on_start()
            elif self.cursorIdx == 3:
                Game.decor = 'arene'
                self.on_start()
            elif self.cursorIdx == 4:
                self.on_back()

    def process_event(self, evt):
        super().process_event(evt)
        if evt.type == KEYDOWN:
            if evt.key == K_1:
                self.select(0, True)
            elif evt.key == K_2:
                self.select(1, True)
            elif evt.key == K_3:
                self.select(2, True)
            elif evt.key == K_4:
                self.select(3, True)
            elif evt.key in (K_6, K_ESCAPE):
                self.select(4, True)


class ControlsKeys(_MenuBackScene):
    def __init__(self, opts, *, on_next):
        super(ControlsKeys, self).__init__(opts, 'menu/titre2.png')
        self.on_next = on_next
        sz = Game.chh
        self.add([
            StaticSprite((0, 0), 'spritesA/debout.gif'),
            StaticSprite((280 * Game.scx, 0), 'spritesB/spritesB4/debout.gif',
                         xflip=True),
            Txt(sz, 'CONTROLS KEYS', Theme.OPTS_TITLE, loc(14, 11)),

            Txt(sz, ' PLAYER A      ', Theme.OPTS_TXT, loc(2, 11)),
            Txt(sz, 'UP............↑', Theme.OPTS_TXT, loc(2, 13)),
            Txt(sz, 'DOWN..........↓', Theme.OPTS_TXT, loc(2, 14)),
            Txt(sz, 'LEFT..........←', Theme.OPTS_TXT, loc(2, 15)),
            Txt(sz, 'RIGHT.........→', Theme.OPTS_TXT, loc(2, 16)),
            Txt(sz, 'ATTACK....SHIFT', Theme.OPTS_TXT, loc(2, 18)),
            Txt(sz, '   or GAMEPAD 1', (255, 0, 0), loc(2, 19)),

            Txt(sz, '      PLAYER B ', Theme.OPTS_TXT, loc(25, 11)),
            Txt(sz, 'UP............I', Theme.OPTS_TXT, loc(25, 13)),
            Txt(sz, 'DOWN..........J', Theme.OPTS_TXT, loc(25, 14)),
            Txt(sz, 'LEFT..........K', Theme.OPTS_TXT, loc(25, 15)),
            Txt(sz, 'RIGHT.........L', Theme.OPTS_TXT, loc(25, 16)),
            Txt(sz, 'ATTACK....SPACE', Theme.OPTS_TXT, loc(25, 18)),
            Txt(sz, '   or GAMEPAD 2', (255, 0, 0), loc(25, 19)),

            Txt(sz, 'ABORT GAME...........ESC', Theme.OPTS_TXT, loc(9, 21)),
            Txt(sz, 'GOTO MENU..........ENTER', Theme.OPTS_TXT, loc(9, 23)),
        ])

    def process_event(self, evt):
        if is_any_key_pressed(evt):
            self.on_next()


class ControlsMoves(EmptyScene):
    def __init__(self, opts, *, on_next):
        super(ControlsMoves, self).__init__(opts)
        self.on_next = on_next
        sz = Game.chh
        self.add([
            StaticSprite((100 * Game.scx, 40 * Game.scy), 'menu/controls1.gif'),
            Txt(sz, 'MOVING CONTROLS', Theme.OPTS_TITLE, loc(13, 2)),

            Txt(sz, 'jump', Theme.OPTS_TXT, loc(19, 5)),
            Txt(sz, 'protect', Theme.OPTS_TXT, loc(8, 7)),
            Txt(sz, 'head', Theme.OPTS_TXT, loc(11, 8)),
            Txt(sz, 'protect', Theme.OPTS_TXT, loc(27, 7)),
            Txt(sz, 'body', Theme.OPTS_TXT, loc(27, 8)),
            Txt(sz, 'move', Theme.OPTS_TXT, loc(9, 12)),
            Txt(sz, 'back', Theme.OPTS_TXT, loc(9, 13)),
            Txt(sz, 'move', Theme.OPTS_TXT, loc(29, 12)),
            Txt(sz, 'forward', Theme.OPTS_TXT, loc(29, 13)),
            Txt(sz, 'roll', Theme.OPTS_TXT, loc(11, 18)),
            Txt(sz, 'back', Theme.OPTS_TXT, loc(11, 19)),
            Txt(sz, 'roll', Theme.OPTS_TXT, loc(27, 18)),
            Txt(sz, 'front', Theme.OPTS_TXT, loc(27, 19)),
            Txt(sz, 'crouch', Theme.OPTS_TXT, loc(18, 21)),
        ])

    def process_event(self, evt):
        if is_any_key_pressed(evt):
            self.on_next()


class ControlsFight(EmptyScene):
    def __init__(self, opts, *, on_next):
        super(ControlsFight, self).__init__(opts)
        self.on_next = on_next
        sz = Game.chh
        self.add([
            StaticSprite((100 * Game.scx, 40 * Game.scy), 'menu/controls2.gif'),
            Txt(sz, 'FIGHTING CONTROLS', Theme.OPTS_TITLE, loc(13, 2)),
            Txt(sz, '(with attack key)', Theme.OPTS_TITLE, loc(13, 3)),

            Txt(sz, 'neck chop', Theme.OPTS_TXT, loc(16, 5)),
            Txt(sz, 'web of', Theme.OPTS_TXT, loc(9, 7)),
            Txt(sz, 'death', Theme.OPTS_TXT, loc(9, 8)),
            Txt(sz, 'head', Theme.OPTS_TXT, loc(27, 7)),
            Txt(sz, 'butt', Theme.OPTS_TXT, loc(27, 8)),
            Txt(sz, 'flying', Theme.OPTS_TXT, loc(7, 12)),
            Txt(sz, 'neck', Theme.OPTS_TXT, loc(9, 13)),
            Txt(sz, 'chop', Theme.OPTS_TXT, loc(9, 14)),
            Txt(sz, 'body', Theme.OPTS_TXT, loc(29, 12)),
            Txt(sz, 'chop', Theme.OPTS_TXT, loc(29, 13)),
            Txt(sz, 'overhead', Theme.OPTS_TXT, loc(7, 18)),
            Txt(sz, 'chop', Theme.OPTS_TXT, loc(11, 19)),
            Txt(sz, 'kick ', Theme.OPTS_TXT, loc(27, 19)),
            Txt(sz, 'leg chop', Theme.OPTS_TXT, loc(17, 21)),
        ])

    def process_event(self, evt):
        if is_any_key_pressed(evt):
            self.on_next()


class Credits(EmptyScene):
    def __init__(self, opts, *, on_back):
        super(Credits, self).__init__(opts)
        self.on_back = on_back
        sz = Game.chh
        col = Theme.OPTS_TXT
        self.add([
            StaticSprite((0, 0), 'menu/team.png'),
            Txt(sz, '     BARBARIAN      ', col, loc(21, 2)),
            Txt(sz, 'the ultimate warrior', col, loc(21, 3)),
            #
            Txt(sz, '  Palace Software   ', col, loc(21, 5)),
            Txt(sz, '         1987       ', col, loc(21, 6)),
            Txt(sz, ' AMIGA 500 version  ', col, loc(21, 7)),
            #
            Txt(sz, 'created and designed', col, loc(21, 9)),
            Txt(sz, '  by STEVE BROWN    ', col, loc(21, 10)),
            #
            Txt(sz, '     programmer     ', col, loc(21, 12)),
            Txt(sz, ' Richard Leinfellner', col, loc(21, 13)),
            #
            Txt(sz, '  assistant artist  ', col, loc(21, 15)),
            #
            Txt(sz, '     GARY CARR      ', col, loc(21, 17)),
            #
            Txt(sz, '     JO WALKER      ', col, loc(21, 19)),
            #
            Txt(sz, '       music        ', col, loc(21, 21)),
            Txt(sz, '   RICHARD JOSEPH   ', col, loc(21, 22)),
            #
        ])

    def process_event(self, evt):
        if is_any_key_pressed(evt):
            self.on_back()


class History(EmptyScene):
    def __init__(self, opts, *, on_back):
        super(History, self).__init__(opts)
        self.on_back = on_back
        sz = Game.chh
        col = Theme.OPTS_TXT
        self.add([
            Txt(sz, 'The evil sorcerer Drax desires        ', col, loc(2, 2)),
            Txt(sz, 'Princess Marianna and has sworn       ', col, loc(2, 3)),
            Txt(sz, 'to wreak an unspeakable doom on the   ', col, loc(2, 4)),
            Txt(sz, 'people of the Jewelled City, unless   ', col, loc(2, 5)),
            Txt(sz, 'she is delivered to him.              ', col, loc(2, 6)),
            Txt(sz, 'However, he has agreed that if a      ', col, loc(2, 7)),
            Txt(sz, 'champion can be found who is able to  ', col, loc(2, 8)),
            Txt(sz, 'defeat his 7 demonic guardians, the   ', col, loc(2, 9)),
            Txt(sz, 'princess will be allowed to go free.  ', col, loc(2, 10)),
            #
            Txt(sz, 'All seems lost as champion after      ', col, loc(2, 12)),
            Txt(sz, 'champion is defeated.                 ', col, loc(2, 13)),
            #
            Txt(sz, 'Then, from the forgotten wastelands of', col, loc(2, 15)),
            Txt(sz, 'the North, comes an unknown barbarian,', col, loc(2, 16)),
            Txt(sz, 'a mighty warrior, wielding broadsword ', col, loc(2, 17)),
            Txt(sz, 'with deadly skill.                    ', col, loc(2, 18)),
            #
            Txt(sz, 'Can he vanquish the forces of Darkness', col, loc(2, 20)),
            Txt(sz, 'and free the princess ?               ', col, loc(2, 21)),
            #
            Txt(sz, 'Only you can say ...                  ', col, loc(2, 23)),
        ])

    def process_event(self, evt):
        if is_any_key_pressed(evt):
            self.on_back()
