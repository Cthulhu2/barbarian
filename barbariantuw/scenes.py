# -*- coding: utf-8 -*-
from itertools import cycle

from pygame import Surface
from pygame.locals import *
from pygame.sprite import LayeredDirty, Group
from pygame.time import get_ticks

from barbariantuw.settings import (
    Theme, SCREEN_SIZE, SCALE_X, SCALE_Y, CHAR_W, CHAR_H,
)
from barbariantuw.sprites import (
    Txt, AnimatedSprite, StaticSprite, Barbarian,
    loc2pxX, loc2pxY, loc, State, Levier, Sorcier, Rectangle,
)
import barbariantuw.ai as ai
import barbariantuw.anims as anims
from barbariantuw.anims import get_img, rtl_anims, get_snd


class Game:  # Mutable options
    Country = 'Europe'  # USA, Europe
    Decor = 'foret'  # foret, plaine, trone, arene
    Partie = 'solo'  # solo, vs
    Demo = False
    IA = 0
    ScoreA = 0
    ScoreB = 0


class EmptyScene(LayeredDirty):
    def __init__(self, opts, *sprites_, **kwargs):
        super(EmptyScene, self).__init__(*sprites_, **kwargs)
        self.set_timing_threshold(1000.0 / 25.0)
        back = Surface(SCREEN_SIZE)
        back.fill(Theme.BACK, back.get_rect())
        # noinspection PyTypeChecker
        self.clear(None, back)
        self.timer = get_ticks()
        self.opts = opts

    def process_event(self, evt):
        pass


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
        self.repaint_rect(((0, 0), SCREEN_SIZE))

    def show_titre(self):
        if self.titre:
            return
        self.titre = True

        if Game.Country == 'USA':
            img = get_img('menu/titre.png').copy()
            logo_ds = get_img('menu/logoDS.png')
            img.blit(logo_ds, (46 * SCALE_X, 10 * SCALE_Y))
        else:
            img = get_img('menu/titre.png')

        # noinspection PyTypeChecker
        self.clear(None, img)
        self.repaint_rect(((0, 0), SCREEN_SIZE))

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

        get_img('spritesA/debout.gif')
        get_img('spritesA/assis1.gif')
        get_img('spritesA/assis2.gif')
        get_img('spritesA/attente1.gif')
        get_img('spritesA/attente2.gif')
        get_img('spritesA/attente3.gif')
        get_img('spritesA/protegeH.gif')
        get_img('spritesA/cou2.gif')
        get_img('spritesA/cou3.gif')
        get_img('spritesA/devant1.gif')
        get_img('spritesA/devant2.gif')
        get_img('spritesA/devant3.gif')
        get_img('spritesA/genou1.gif')
        get_img('spritesA/genou3.gif')
        get_img('spritesA/marche1.gif')
        get_img('spritesA/marche2.gif')
        get_img('spritesA/marche3.gif')
        get_img('spritesA/saut1.gif')
        get_img('spritesA/saut2.gif')
        get_img('spritesA/vainqueur1.gif')
        get_img('spritesA/vainqueur2.gif')
        get_img('spritesA/vainqueur3.gif')
        get_img('spritesA/retourne1.gif')
        get_img('spritesA/retourne2.gif')
        get_img('spritesA/retourne3.gif')
        get_img('spritesA/front1.gif')
        get_img('spritesA/front2.gif')
        get_img('spritesA/front3.gif')
        get_img('spritesA/toile1.gif')
        get_img('spritesA/toile2.gif')
        get_img('spritesA/toile3.gif')
        get_img('spritesA/toile4.gif')
        get_img('spritesA/tombe1.gif')
        get_img('spritesA/tombe2.gif')
        get_img('spritesA/tombe3.gif')
        get_img('spritesA/protegeD.gif')
        get_img('spritesA/protegeH.gif')
        get_img('spritesA/tete1.gif')
        get_img('spritesA/tete2.gif')
        get_img('spritesA/touche2.gif')
        get_img('spritesA/touche1.gif')
        get_img('spritesA/touche2.gif')

        get_img('spritesA/pied1.gif')
        get_img('spritesA/pied2.gif')
        get_img('spritesA/decap1.gif')
        get_img('spritesA/decap2.gif')
        get_img('spritesA/decap3.gif')
        get_img('spritesA/decap4.gif')
        get_img('spritesA/assis1.gif')
        get_img('spritesA/mort2.gif')
        get_img('spritesA/mort3.gif')
        get_img('spritesA/mort4.gif')

        get_img('spritesA/roulade1.gif')
        get_img('spritesA/roulade2.gif')
        get_img('spritesA/roulade3.gif')
        get_img('spritesA/roulade5.gif')

        get_img('sprites/drax1.gif')
        get_img('sprites/drax2.gif')
        get_img('sprites/marianna.gif')

        # gnome

        get_img('sprites/gnome1.gif')
        get_img('sprites/gnome2.gif')
        get_img('sprites/gnome3.gif')
        get_img('sprites/gnome4.gif')

        # divers
        get_img('sprites/sang.gif')
        get_img('spritesA/teteombre.gif')

        get_img('spritesA/tetedecap1.gif')
        get_img('spritesA/tetedecap2.gif')
        get_img('spritesA/tetedecap3.gif')
        get_img('spritesA/tetedecap4.gif')
        get_img('spritesA/tetedecap5.gif')
        get_img('spritesA/tetedecap6.gif')

        get_img('sprites/feu1.gif')
        get_img('sprites/feu2.gif')
        get_img('sprites/feu3.gif')

        get_img('sprites/gicle1.gif')
        get_img('sprites/gicle2.gif')
        get_img('sprites/gicle3.gif')

        get_img('stage/serpent1.gif')
        get_img('stage/serpent2.gif')
        get_img('stage/serpent3.gif')

    def update(self, current_time, *args):
        super(Logo, self).update(current_time, *args)
        passed = current_time - self.timer
        if Game.Country == 'USA':
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
        if evt.type == KEYUP:
            self.skip = True


class _MenuBackScene(EmptyScene):
    def __init__(self, opts, back: str):
        super(_MenuBackScene, self).__init__(opts)
        if Game.Country == 'USA':
            back = get_img(back).copy()
            logo_ds = get_img('menu/logoDS.png')
            back.blit(logo_ds, (46 * SCALE_X, 10 * SCALE_Y))
        else:
            back = get_img(back)
        # noinspection PyTypeChecker
        self.clear(None, back)


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

    def process_event(self, evt):
        if evt.type != KEYUP:
            return
        elif evt.key == K_0:
            self.on_demo()
        elif evt.key == K_1:
            self.on_solo()
        elif evt.key == K_2:
            self.on_duel()
        elif evt.key == K_3:
            self.on_options()
        elif evt.key == K_4:
            self.on_controls()
        elif evt.key == K_5:
            self.on_history()
        elif evt.key == K_6:
            self.on_credits()
        elif evt.key in (K_7, K_ESCAPE):
            self.on_quit()


def area(color, lbl, border_width=2):
    return Rectangle(0, 0, CHAR_W, CHAR_H, color, border_width, lbl)


MORT_RIGHT_BORDER = 34


class Battle(EmptyScene):
    chrono: int = 0  # current millisecond
    chronoOn: bool = False
    chronometre: int = 60  # seconds
    entree: bool = True
    sorcier: bool = False
    entreesorcier: bool = False
    lancerintro: bool = True

    def __init__(self, opts, *, on_esc, on_next, on_menu):
        super(Battle, self).__init__(opts)
        self.on_esc = on_esc
        self.on_menu = on_menu
        self.on_next = on_next
        self.jeu = 'encours'  # perdu, gagne

        back = get_img(f'stage/{Game.Decor}.gif')
        if Game.Country == 'USA':
            back = back.copy()
            if Game.Decor in ('foret', 'plaine'):
                logo = get_img('stage/logoDS2.png')
                if Game.Decor == 'foret':
                    back.blit(logo, (59 * SCALE_X, 16 * SCALE_Y))
                elif Game.Decor == 'plaine':
                    back.blit(logo, (59 * SCALE_X, 14 * SCALE_Y))
            if Game.Decor in ('arene', 'trone'):
                logo = get_img('stage/logoDS3.png')
                back.blit(logo, (59 * SCALE_X, 16 * SCALE_Y))
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
            StaticSprite((0, 104 * SCALE_Y),
                         f'stage/{Game.Decor}ARBREG.gif'),
            StaticSprite((272 * SCALE_X, 104 * SCALE_Y),
                         f'stage/{Game.Decor}ARBRED.gif'),
            layer=5)

        self.joueurA = Barbarian(opts, loc2pxX(1), loc2pxY(14),
                                 'spritesA', rtl=False)
        self.joueurA.infoCoup = 3
        self.joueurB = Barbarian(opts, loc2pxX(36), loc2pxY(14),
                                 f'spritesB/spritesB{Game.IA}', rtl=True)
        sz = CHAR_H
        if Game.Partie == 'solo' and not Game.Demo:
            Txt(sz, 'ONE  PLAYER', Theme.TXT, loc(16, 25), self)
        elif Game.Partie == 'vs':
            Txt(sz, 'TWO PLAYERS', Theme.TXT, loc(16, 25), self)
        elif Game.Demo:
            Txt(sz, 'DEMO', Theme.TXT, loc(18, 25), self)

        self.txtScoreA = Txt(sz, f'{Game.ScoreA:05}', Theme.TXT, loc(13, 8),
                             self, cached=False)
        self.txtScoreB = Txt(sz, f'{Game.ScoreB:05}', Theme.TXT, loc(24, 8),
                             self, cached=False)

        if Game.Partie == 'vs':
            self.txtChronometre = Txt(sz, f'{self.chronometre:02}',
                                      Theme.TXT, loc(20, 8))
            # noinspection PyTypeChecker
            self.add(self.txtChronometre)

        elif Game.Partie == 'solo':
            Txt(sz, f'{Game.IA:02}', Theme.TXT, loc(20, 8), self)
        # noinspection PyTypeChecker
        self.add(self.joueurA, self.joueurB, layer=1)
        self.joueurA.animate('avance')
        self.joueurB.animate('avance')
        self.serpentA = AnimatedSprite((11 * SCALE_X, 22 * SCALE_Y),
                                       anims.serpent(), self)
        self.serpentB = AnimatedSprite((275 * SCALE_X, 22 * SCALE_Y),
                                       rtl_anims(anims.serpent()), self)
        self.temps = 0
        self.tempsfini = False
        self.sense = 'normal'  # inverse
        self.soncling = cycle(['block1.ogg', 'block2.ogg', 'block3.ogg'])
        self.songrogne = cycle([0, 0, 0, 'grogne1.ogg', 0, 0, 'grogne1.ogg'])
        self.sontouche = cycle(['touche.ogg', 'touche2.ogg', 'touche3.ogg'])
        self.vieA0 = AnimatedSprite((43 * SCALE_X, 0), anims.vie(), self)
        self.vieA1 = AnimatedSprite((43 * SCALE_X, 11 * SCALE_Y), anims.vie(), self)
        self.vieB0 = AnimatedSprite((276 * SCALE_X, 0), anims.vie(), self)
        self.vieB1 = AnimatedSprite((276 * SCALE_X, 11 * SCALE_Y), anims.vie(), self)
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
            get_snd('mortdecap.ogg').stop()
            get_snd('mortKO.ogg').stop()
            get_snd('prepare.ogg').stop()
        self.on_menu()

    def next_stage(self):
        if self.opts.sound:
            get_snd('mortdecap.ogg').stop()
            get_snd('mortKO.ogg').stop()
            get_snd('prepare.ogg').stop()
        self.on_next()

    def process_event(self, evt):
        if evt.type == KEYUP and evt.key == K_ESCAPE:
            if self.jeu == 'encours':
                if self.opts.sound:
                    get_snd('mortdecap.ogg').stop()
                    get_snd('mortKO.ogg').stop()
                    get_snd('prepare.ogg').stop()
            Game.IA = 0
            self.on_esc()
            return
        if evt.type == KEYUP and evt.key == K_F12 and self.opts.debug > 1:
            self.debugAttArea = not self.debugAttArea
            if self.debugAttArea:
                self.add(self.attAreas, layer=99)
            else:
                self.remove(self.attAreas)

        if Game.Demo:
            return

        # TODO: Joystick events
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

    def animate_gnome(self):
        if not self.gnome:
            self.gnome = True
            # noinspection PyTypeChecker
            self.add(self.gnomeSprite, layer=4)
            self.gnomeSprite.animate('gnome')

    def start_sorcier(self):
        self.sorcier = True
        self.sense = 'inverse'
        self.joueurA.animate('avance')
        self.joueurA.x = loc2pxX(36)
        if not self.joueurA.rtl:
            self.joueurA.turn_around(True)
        self.gnome = False
        self.joueurA.sortie = False
        self.joueurA.attaque = False
        self.entreesorcier = True
        self.joueurB = Sorcier(self.opts, loc2pxX(9), loc2pxY(14))
        self.joueurB.occupe_state(State.debout, self.temps)
        # noinspection PyTypeChecker
        self.add(self.joueurB,
                 StaticSprite((114 * SCALE_X, 95 * SCALE_Y),
                              'fill', w=16, h=6, fill=Theme.BLACK),
                 StaticSprite((109 * SCALE_X, 100 * SCALE_Y),
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
                if self.jeu == 'perdu' or ja.state == State.mortSORCIER:
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

        if not Game.Demo:
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
                             self.soncling, self.songrogne, self.sontouche,
                             Game.Demo)
        #
        if self.joueurA.state == State.retourne:
            if self.temps == self.joueurA.reftemps + 16:
                self.sense = "inverse" if self.joueurA.rtl else "normal"

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
                self.jeu = 'perdu'
            elif self.temps == self.joueurA.reftemps:
                self.joueurB.stopped = True
                self.joueurA.animate('mortSORCIER')

    @staticmethod
    def _center_txt(msg):
        txt = Txt(CHAR_H, msg,
                  color=(34, 34, 153), bgcolor=Theme.BLACK)
        txt.rect.topleft = (SCREEN_SIZE[0] / 2 - txt.rect.w / 2, loc2pxY(11))
        bg = StaticSprite((0, 0), 'fill',
                          w=(txt.rect.w + 2 * CHAR_W) / SCALE_X,
                          h=(txt.rect.h + 2 * CHAR_H) / SCALE_Y,
                          fill=Theme.BLACK)
        bg.rect.topleft = (txt.rect.topleft[0] - CHAR_W,
                           txt.rect.topleft[1] - CHAR_H)
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
            StaticSprite(loc(16.5, 14), 'sprites/marianna.gif'),
            StaticSprite((186 * SCALE_X, 95 * SCALE_Y), 'fill',
                         w=15, h=20, fill=Theme.BLACK),
            StaticSprite((185 * SCALE_X, 113 * SCALE_Y), 'fill',
                         w=18, h=2.1, fill=Theme.BLACK),
            self._center_txt('Thanks big boy.'))
        self.jeu = 'gagne'

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

        if Game.Partie == 'vs':
            self.joueurB.clavier()
        elif Game.Partie == 'solo':
            if ai.joueurB(Game.Demo, Game.IA,
                          self.joueurA, self.joueurB, self.temps):
                return
        # redirection suivant les touches
        if self.joueurB.levier != Levier.neutre:
            self.joueurB.action(self.temps)
        else:
            self.joueurB.action_debut(self.temps)

    def _gestionB(self):
        self.joueurB.gestion(self.temps, self.joueurA,
                             self.soncling, self.songrogne, self.sontouche,
                             Game.Partie == 'solo')
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
        Game.ScoreA += increment
        self.txtScoreA.msg = f'{Game.ScoreA:05}'

    def on_scoreB(self, increment):
        Game.ScoreB += increment
        self.txtScoreB.msg = f'{Game.ScoreB:05}'

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
            if (gnome.rect.left >= mort.rect.right - CHAR_W
                    and mort.anim != 'mortgnome'):
                mort.topleft = mort.rect.topleft
                mort.animate('mortgnome')
        elif mort.state == State.mortdecap:
            if (gnome.rect.left >= mort.rect.right - CHAR_W
                    and mort.anim != 'mortdecapgnome'):
                mort.topleft = mort.rect.topleft
                mort.animate('mortdecapgnome')
            if mort.tete.alive():
                if gnome.rect.right >= mort.tete.rect.center[0]:
                    mort.animate_football()
                if mort.tete.rect.left > SCREEN_SIZE[0]:
                    mort.stop_football()
        if gnome.alive() and mort.xLoc > MORT_RIGHT_BORDER:
            gnome.kill()
            mort.kill()
            if Game.Partie == 'vs':
                vainqueur.bonus = True
            if Game.Partie == 'solo':
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
                if Game.Partie == 'vs':
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
            if Game.Partie == 'vs':
                self.chronoOn = True

    def check_sortiedA(self, jax, jbx):
        if not self.tempsfini:
            if jbx >= MORT_RIGHT_BORDER and (jax <= 0 or 38 <= jax):
                if Game.Partie == 'solo':
                    if Game.Demo:
                        self.finish()
                    elif Game.IA < 7:
                        self.next_stage()
                    else:
                        self.start_sorcier()
                elif Game.Partie == 'vs':
                    self.finish()
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
        if self.jeu in ('gagne', 'perdu'):
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
            anims.snd_play('prepare.ogg')

        if self.entree:
            self.do_entree(ja.xLoc, jb.xLoc)
            return  #
        if Game.Demo and self.sense == 'inverse':
            self.on_menu()
            return  #

        if ja.sortie:
            self.check_sortiedA(ja.xLoc, jb.xLoc)
            return  #
        elif jb.sortie:
            self.check_sortiedB(ja.xLoc, jb.xLoc)
            return  #
        elif self.gnome:
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


class Version(_MenuBackScene):
    def __init__(self, opts, *, on_display, on_back):
        super(Version, self).__init__(opts, 'menu/version.png')
        self.on_display = on_display
        self.on_back = on_back

    def process_event(self, evt):
        if evt.type != KEYUP:
            return
        elif evt.key == K_1:
            Game.Country = 'Europe'
            self.on_display()
        elif evt.key == K_2:
            Game.Country = 'USA'
            self.on_display()
        elif evt.key == K_ESCAPE:
            self.on_back()


class Display(_MenuBackScene):
    def __init__(self, opts, *, on_fullscreen, on_window, on_back):
        super(Display, self).__init__(opts, 'menu/display.png')
        self.on_fullscreen = on_fullscreen
        self.on_window = on_window
        self.on_back = on_back

    def process_event(self, evt):
        if evt.type != KEYUP:
            return
        elif evt.key == K_1:
            self.on_fullscreen()
        elif evt.key == K_2:
            self.on_window()
        elif evt.key == K_ESCAPE:
            self.on_back()


class SelectStage(_MenuBackScene):
    def __init__(self, opts, *, on_start, on_back):
        super(SelectStage, self).__init__(opts, 'menu/stage.png')
        self.on_start = on_start
        self.on_back = on_back

    def process_event(self, evt):
        if evt.type != KEYUP:
            return
        elif evt.key == K_1:
            Game.Decor = 'plaine'
            self.on_start()
        elif evt.key == K_2:
            Game.Decor = 'foret'
            self.on_start()
        elif evt.key == K_3:
            Game.Decor = 'trone'
            self.on_start()
        elif evt.key == K_4:
            Game.Decor = 'arene'
            self.on_start()
        elif evt.key in (K_6, K_ESCAPE):
            self.on_back()


class ControlsKeys(_MenuBackScene):
    def __init__(self, opts, *, on_next):
        super(ControlsKeys, self).__init__(opts, 'menu/titre2.png')
        self.on_next = on_next
        sz = CHAR_H
        self.add([
            StaticSprite((0, 0), 'menu/playerA.png',
                         color=(255, 255, 255)),
            StaticSprite((280 * SCALE_X, 0), 'menu/playerB.png',
                         color=(255, 255, 255)),
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
        if evt.type != KEYUP:
            return
        elif evt.key in (K_KP_ENTER, K_RETURN, K_ESCAPE, K_SPACE):
            self.on_next()


class ControlsMoves(EmptyScene):
    def __init__(self, opts, *, on_next):
        super(ControlsMoves, self).__init__(opts)
        self.on_next = on_next
        sz = CHAR_H
        self.add([
            StaticSprite((100 * SCALE_X, 40 * SCALE_Y), 'menu/controls1.gif'),
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
        if evt.type != KEYUP:
            return
        elif evt.key in (K_KP_ENTER, K_RETURN, K_ESCAPE, K_SPACE):
            self.on_next()


class ControlsFight(EmptyScene):
    def __init__(self, opts, *, on_next):
        super(ControlsFight, self).__init__(opts)
        self.on_next = on_next
        sz = CHAR_H
        self.add([
            StaticSprite((100 * SCALE_X, 40 * SCALE_Y), 'menu/controls2.gif'),
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
        if evt.type != KEYUP:
            return
        elif evt.key in (K_KP_ENTER, K_RETURN, K_ESCAPE, K_SPACE):
            self.on_next()


class Credits(EmptyScene):
    def __init__(self, opts, *, on_back):
        super(Credits, self).__init__(opts)
        self.on_back = on_back
        sz = CHAR_H
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
        if evt.type != KEYUP:
            return
        elif evt.key in (K_KP_ENTER, K_RETURN, K_ESCAPE, K_SPACE):
            self.on_back()


class History(EmptyScene):
    def __init__(self, opts, *, on_back):
        super(History, self).__init__(opts)
        self.on_back = on_back
        sz = CHAR_H
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
        if evt.type != KEYUP:
            return
        elif evt.key in (K_KP_ENTER, K_RETURN, K_ESCAPE, K_SPACE):
            self.on_back()
