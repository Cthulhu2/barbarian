# -*- coding: utf-8 -*-
from itertools import cycle
from typing import Union

from pygame import Surface
from pygame.locals import *
from pygame.sprite import LayeredDirty, Group
from pygame.time import get_ticks

from settings import Theme, SCREEN_SIZE, SCALE, FRAME_RATE, CHAR_W, CHAR_H
from sprites import (
    get_snd, Txt, AnimatedSprite, StaticSprite, Barbarian,
    loc2px, loc, State, Levier, Sorcier, Rectangle, px2loc
)
import anims
from anims import get_img, rtl_anims


class Game:  # Mutable options
    Country = 'europe'  # USA, europe
    Decor = 'foret'  # foret, plaine, trone, arene
    Partie = 'solo'  # solo, vs
    Sorcier = False
    Demo = False
    IA = 0
    Chronometre = 0
    ScoreA = 0
    ScoreB = 0
    Rtl = False


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
            img.blit(logo_ds, (46 * SCALE, 10 * SCALE))
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
            back.blit(logo_ds, (46 * SCALE, 10 * SCALE))
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


class Battle(EmptyScene):
    chrono: int = 0
    chronoOn: bool = False
    entree: bool = True
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
                    back.blit(logo, (59 * SCALE, 16 * SCALE))
                elif Game.Decor == 'plaine':
                    back.blit(logo, (59 * SCALE, 14 * SCALE))
            if Game.Decor in ('arene', 'trone'):
                logo = get_img('stage/logoDS3.png')
                back.blit(logo, (59 * SCALE, 16 * SCALE))
        # noinspection PyTypeChecker
        self.clear(None, back)
        self.debugAttArea = False
        if self.opts.debug > 1:
            self.jAstate = Txt.Debug(loc2px(10), 0)
            self.jBstate = Txt.Debug(loc2px(25), 0)
            self.jAlevier = Txt.Debug(loc2px(10), self.jAstate.rect.bottom)
            self.jBlevier = Txt.Debug(loc2px(25), self.jBstate.rect.bottom)
            self.jAtemps = Txt.Debug(loc2px(10), self.jAlevier.rect.bottom)
            self.jBtemps = Txt.Debug(loc2px(25), self.jBlevier.rect.bottom)
            self.debugTemps = Txt.Debug(loc2px(18), 0)
            self.distance = Txt.Debug(loc2px(18), self.jBtemps.rect.top)
            # noinspection PyTypeChecker
            self.add(self.jAstate, self.jAlevier, self.jAtemps,
                     self.jBstate, self.jBlevier, self.jBtemps,
                     self.debugTemps, self.distance, layer=99)
            if self.opts.debug > 2:
                self.jAframe = Txt.Debug(loc2px(10), self.jAtemps.rect.bottom)
                self.jBframe = Txt.Debug(loc2px(25), self.jBtemps.rect.bottom)
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
            StaticSprite((0, 104 * SCALE),
                         f'stage/{Game.Decor}ARBREG.gif'),
            StaticSprite((272 * SCALE, 104 * SCALE),
                         f'stage/{Game.Decor}ARBRED.gif'),
            layer=5)

        self.joueurA = Barbarian(opts, loc2px(1), loc2px(14),
                                 'spritesA',
                                 rtl=Game.Rtl)
        self.joueurA.infoCoup = 3
        self.joueurB = Barbarian(opts, loc2px(36), loc2px(14),
                                 f'spritesB/spritesB{Game.IA}',
                                 rtl=not Game.Rtl)  # type: Union[Barbarian, Sorcier]
        sz = CHAR_H
        if Game.Partie == 'solo' and not Game.Demo:
            Txt(sz, 'ONE  PLAYER', Theme.TXT, loc(16, 25), self)
        elif Game.Partie == 'vs':
            Txt(sz, 'TWO PLAYERS', Theme.TXT, loc(16, 25), self)
        elif Game.Demo:
            Txt(sz, 'DEMO', Theme.TXT, loc(18, 25), self)

        self.txtScoreA = Txt(sz, f'{Game.ScoreA:05}', Theme.TXT, loc(13, 8), self)
        self.txtScoreB = Txt(sz, f'{Game.ScoreB:05}', Theme.TXT, loc(24, 8), self)

        if Game.Partie == 'vs':
            self.txtChronometre = Txt(sz, f'{Game.Chronometre:02}',
                                      Theme.TXT, loc(20, 8))
            self.add(self.txtChronometre)

        elif Game.Partie == 'solo':
            Txt(sz, f'{Game.IA:02}', Theme.TXT, loc(20, 8), self)
        self.add(self.joueurA, self.joueurB, layer=1)
        self.joueurA.animate('avance')
        self.joueurB.animate('avance')
        self.serpentA = AnimatedSprite((11 * SCALE, 22 * SCALE),
                                       anims.serpent(), self)
        self.serpentB = AnimatedSprite((275 * SCALE, 22 * SCALE),
                                       rtl_anims(anims.serpent()), self)
        self.entreesorcier = False
        self.temps = 0
        self.tempsfini = False
        self.sense = 'normal'  # inverse
        self.soncling = cycle(['block1.ogg', 'block2.ogg', 'block3.ogg'])
        self.songrogne = cycle([0, 0, 0, 'grogne1.ogg', 0, 0, 'grogne1.ogg'])
        self.sontouche = cycle(['touche.ogg', 'touche2.ogg', 'touche3.ogg'])
        self.vieA0 = AnimatedSprite((43 * SCALE, 0), anims.vie(), self)
        self.vieA1 = AnimatedSprite((43 * SCALE, 11 * SCALE), anims.vie(), self)
        self.vieB0 = AnimatedSprite((276 * SCALE, 0), anims.vie(), self)
        self.vieB1 = AnimatedSprite((276 * SCALE, 11 * SCALE), anims.vie(), self)
        self.vieA(self.joueurA.vie)
        self.vieB(self.joueurB.vie)
        #
        self.gnome = False
        self.gnomeSprite = AnimatedSprite((0, loc2px(20)), anims.gnome())

    def snd_play(self, snd: str):
        if snd and self.opts.sound:
            get_snd(snd).play()

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
        Game.Sorcier = True
        self.sense = 'inverse'
        self.joueurA.state = State.debout
        self.joueurA.x = loc2px(36)
        if not self.joueurA.rtl:
            self.joueurA.turn_around(True)
        self.gnome = False
        self.joueurA.sortie = False
        self.entreesorcier = True
        self.joueurB = Sorcier(self.opts, loc2px(7), loc2px(14))
        self.joueurB.occupe_state(State.sorcier, self.temps)
        # noinspection PyTypeChecker
        self.add(self.joueurB,
                 StaticSprite((114 * SCALE, 95 * SCALE),
                              'fill', w=16, h=6, fill=Theme.BLACK),
                 StaticSprite((109 * SCALE, 100 * SCALE),
                              'fill', w=27, h=15.1, fill=Theme.BLACK),
                 layer=0)
        self.vieA(0)
        self.vieB(0)
        self.serpentA.animate('bite')
        self.serpentB.animate('bite')

    def _degats(self):
        # degats sur joueurA
        ja = self.joueurA
        jb = self.joueurB
        degat = False
        if Game.Sorcier:
            if (ja.x_loc() < 33 and (
                    (jb.yAtt == ja.yT and ja.xT < jb.xAtt <= ja.xT + 2)
                    or (jb.yAtt == ja.yG and ja.xG <= jb.xAtt <= ja.xG + 2)
            )):
                if self.jeu == 'perdu' or ja.state == State.mortSORCIER:
                    return 'gestion'
                ja.occupe_state(State.mortSORCIER, self.temps)
                jb.occupe_state(State.sorcierFINI, self.temps)
                return 'gestion'
        else:
            degat, score = ja.degat(jb)
            if score:
                Game.ScoreB += score
                self.txtScoreB.msg = f'{Game.ScoreB:05}'
        if degat or ja.occupe:
            return 'gestion'
        return 'clavier'

    def _clavier(self):
        self.joueurA.clavierX = 7
        self.joueurA.clavierY = 7
        self.joueurA.levier = Levier.neutre
        if self.joueurA.sortie:
            self.joueurA.attaque = False
            self.joueurA.levier = self.joueurA.recule_levier()
            self.joueurA.action(self.temps)
            return 'gestion'
        if self.entreesorcier:
            if self.joueurA.x_loc() <= 33:
                self.entreesorcier = False
                return 'gestion'
            self.joueurA.levier = Levier.gauche
            self.joueurA.action(self.temps)
            return 'gestion'
        if not Game.Demo:
            self.joueurA.clavier()
        else:
            distance = abs(self.joueurB.x_loc() - self.joueurA.x_loc())
            if distance >= 15:  # quand trop loin
                self.joueurA.occupe_state(State.rouladeAV, self.temps)
                return 'gestion'
            if distance == 12 and self.joueurB.anim == 'debout':
                self.joueurA.occupe_state(State.decapite, self.temps)
                return 'gestion'

            if distance == 9:
                if self.joueurB.attente > 100:
                    self.joueurA.occupe_state(State.decapite, self.temps)
                    return 'gestion'
                if self.joueurB.state == State.rouladeAR:
                    self.joueurA.occupe_state(State.genou, self.temps)
                    return 'gestion'
                if self.joueurB.occupe:
                    self.joueurA.occupe_state(State.rouladeAV, self.temps)
                    return 'gestion'

            if 6 < distance < 9:  # distance de combat 1
                # pour se rapprocher
                if self.joueurB.state == State.rouladeAR:
                    self.joueurA.occupe_state(State.genou, self.temps)
                    return 'gestion'
                if self.joueurB.levier == Levier.gauche:
                    self.joueurA.occupe_state(State.araignee, self.temps)
                    return 'gestion'
                if self.joueurB.state == State.front:
                    self.joueurA.state = State.protegeH
                    self.joueurA.reftemps = self.temps
                    return 'gestion'
                # pour eviter les degats repetitifs
                if self.joueurA.infoDegatG > 4:
                    if self.joueurB.state in (State.assis2, State.genou):
                        self.joueurA.occupe_state(State.genou, self.temps)
                        return 'gestion'
                if self.joueurA.infoDegatG > 2:
                    if self.joueurB.state in (State.assis2, State.genou):
                        self.joueurA.occupe_state(State.rouladeAV, self.temps)
                        return 'gestion'
                if self.joueurA.infoDegatT > 2:
                    if self.joueurB.state == State.cou:
                        self.joueurA.occupe_state(State.genou, self.temps)
                        return 'gestion'
                if self.joueurA.infoDegatF > 2:
                    if self.joueurB.state == State.front:
                        self.joueurA.occupe_state(State.rouladeAV, self.temps)
                        return 'gestion'

                # pour alterner les attaques
                if self.joueurA.infoCoup == 0:
                    self.joueurA.infoCoup += 1
                    self.joueurA.occupe_state(State.devant, self.temps)
                    return 'gestion'
                if self.joueurA.infoCoup == 1:
                    self.joueurA.infoCoup += 1
                    self.joueurA.occupe_state(State.front, self.temps)
                    return 'gestion'
                if self.joueurA.infoCoup == 2:
                    self.joueurA.infoCoup += 1
                    self.joueurA.occupe_state(State.araignee, self.temps)
                    return 'gestion'
                if self.joueurA.infoCoup == 3:
                    self.joueurA.infoCoup += 1
                    self.joueurA.occupe_state(State.araignee, self.temps)
                    return 'gestion'
                if self.joueurA.infoCoup == 4:
                    self.joueurA.infoCoup += 1
                    self.joueurA.occupe_state(State.cou, self.temps)
                    return 'gestion'
                if self.joueurA.infoCoup == 5:
                    self.joueurA.infoCoup = 0
                    self.joueurA.levier = self.joueurA.avance_levier()

            if distance <= 6:
                if self.joueurB.state == State.devant:
                    self.joueurA.state = State.protegeD
                    self.joueurA.reftemps = self.temps
                    return 'gestion'

                if self.joueurA.infoDegatG > 4:
                    if self.joueurB.state in (State.assis2, State.genou):
                        self.joueurA.occupe_state(State.genou, self.temps)
                        return 'gestion'
                if self.joueurA.infoDegatG > 2:
                    if self.joueurB.state == State.coupdepied:
                        self.joueurA.occupe_state(State.rouladeAV, self.temps)
                        return 'gestion'
                    if self.joueurB.state in (State.assis2, State.genou):
                        self.joueurA.occupe_state(State.rouladeAV, self.temps)
                        return 'gestion'

                if self.joueurA.infoCoup == 0:
                    self.joueurA.infoCoup += 1
                    self.joueurA.occupe_state(State.genou, self.temps)
                    return 'gestion'
                if self.joueurA.infoCoup == 1:
                    self.joueurA.infoCoup += 1
                    self.joueurA.occupe_state(State.coupdetete, self.temps)
                    return 'gestion'
                if self.joueurA.infoCoup == 2:
                    self.joueurA.infoCoup += 1
                    self.joueurA.occupe_state(State.araignee, self.temps)
                    return 'gestion'
                if self.joueurA.infoCoup == 3:
                    self.joueurA.infoCoup += 1
                    self.joueurA.occupe_state(State.genou, self.temps)
                    return 'gestion'
                if self.joueurA.infoCoup == 4:
                    self.joueurA.infoCoup += 1
                    self.joueurA.occupe_state(State.coupdepied, self.temps)
                    return 'gestion'
                if self.joueurA.infoCoup == 5:
                    self.joueurA.infoCoup = 0
                    self.joueurA.levier = self.joueurA.avance_levier()

            if self.sense == 'inverse':
                self.on_menu()
                return None

        # redirection suivant les touches
        if self.joueurA.levier != Levier.neutre:
            self.joueurA.action(self.temps)
            return 'gestion'

        self.joueurA.protegeD = False
        self.joueurA.protegeH = False
        self.joueurA.attente += 1
        # pour se relever
        self.joueurA.assis = False
        if self.joueurA.state == State.assis2:
            self.joueurA.occupe_state(State.releve, self.temps)
            return 'gestion'
        # attente des 5 secondes
        if self.joueurA.attente > FRAME_RATE * 5:
            self.joueurA.occupe_state(State.attente, self.temps)
            return 'gestion'
        # etat debout
        self.joueurA.state = State.debout
        return 'gestion'

    def _gestion(self):
        # ********************************************
        # *************GESTION DES ETATS**************
        # ********************************************
        if self.joueurA.state == State.attente:
            self.joueurA.gestion_attente(self.temps)
            return 'joueur2'

        if self.joueurA.state == State.debout:
            self.joueurA.gestion_debout(self.temps, Game.Demo)
            return 'joueur2'

        if self.joueurA.state == State.avance:
            self.joueurA.gestion_avance(self.temps, self.joueurB,
                                        self.soncling, self.songrogne)
            return 'joueur2'

        if self.joueurA.state == State.recule:
            self.joueurA.gestion_recule(self.temps)
            return 'joueur2'

        if self.joueurA.state == State.saute:
            self.joueurA.gestion_saute(self.temps)
            return 'joueur2'

        if self.joueurA.state == State.assis:
            self.joueurA.gestion_assis(self.temps)
            return 'joueur2'

        if self.joueurA.state == State.assis2:
            self.joueurA.gestion_assis2(self.temps, self.joueurB,
                                        self.soncling, self.songrogne,
                                        Game.Demo)
            return 'joueur2'

        if self.joueurA.state == State.releve:
            self.joueurA.gestion_releve(self.temps, self.joueurB,
                                        self.soncling, self.songrogne)
            return 'joueur2'

        if self.joueurA.state == State.rouladeAV:
            self.joueurA.gestion_rouladeAV(self.temps, self.joueurB)
            return 'joueur2'

        if self.joueurA.state == State.rouladeAR:
            self.joueurA.gestion_rouladeAR(self.temps)
            return 'joueur2'

        if self.joueurA.state == State.protegeH1:
            self.joueurA.gestion_protegeH1(self.temps)
            return 'joueur2'

        if self.joueurA.state == State.protegeH:
            self.joueurA.gestion_protegeH(self.temps, self.joueurB,
                                          self.soncling, self.songrogne)
            return 'joueur2'

        if self.joueurA.state == State.protegeD1:
            self.joueurA.gestion_protegeD1(self.temps)
            return 'joueur2'

        if self.joueurA.state == State.protegeD:
            self.joueurA.gestion_protegeD(self.temps)
            return 'joueur2'

        if self.joueurA.state == State.cou:  # ****attention au temps sinon il saute
            self.joueurA.gestion_cou(self.temps, self.joueurB,
                                     self.soncling, self.songrogne)
            return 'joueur2'

        if self.joueurA.state == State.devant:
            self.joueurA.gestion_devant(self.temps, self.joueurB,
                                        self.soncling, self.songrogne)
            return 'joueur2'

        if self.joueurA.state == State.genou:
            self.joueurA.gestion_genou(self.temps, self.joueurB,
                                       self.soncling, self.songrogne)

        if self.joueurA.state == State.araignee:
            self.joueurA.gestion_araignee(self.temps, self.joueurB,
                                          self.soncling, self.songrogne)

        if self.joueurA.state == State.coupdepied:
            self.joueurA.gestion_coupdepied(self.temps, self.joueurB)

        if self.joueurA.state == State.coupdetete:
            self.joueurA.gestion_coupdetete(self.temps)

        if self.joueurA.state == State.decapite:
            self.joueurA.gestion_decapite(self.temps)

        if self.joueurA.state == State.front:
            self.joueurA.gestion_front(self.temps, self.joueurB,
                                       self.soncling, self.songrogne)

        if self.joueurA.state == State.retourne:
            self.joueurA.gestion_retourne(self.temps)
            if self.temps == self.joueurA.reftemps + 16:
                self.sense = "inverse" if self.joueurA.rtl else "normal"

        if self.joueurA.state == State.vainqueur:
            self.joueurA.gestion_vainqueur()

        if self.joueurA.state == State.vainqueurKO:
            self.joueurA.gestion_vainqueurKO(self.temps, self.joueurB)
            if self.temps > self.joueurA.reftemps + 230:
                self.animate_gnome()
                self.joueurA.reftemps = self.temps
                return None
            elif self.temps == self.joueurA.reftemps + 36:
                return 'colision'

        # ******degats******
        if self.joueurA.state == State.touche:
            rtl = self.joueurA.rtl
            self.joueurA.attente = 0
            self.joueurA.xAtt = self.joueurA.x_loc() + (4 if rtl else 0)
            self.joueurA.reset_xX_back()
            self.joueurA.reset_yX()
            if self.joueurB.state == State.coupdepied:
                self.joueurA.state = State.tombe
                return 'gestion'

            self.serpentA.animate('bite')

            if self.joueurB.state == State.decapite and self.joueurA.decapite:
                self.joueurA.occupe_state(State.mortdecap, self.temps)
                Game.ScoreB += 250
                self.txtScoreB.msg = f'{Game.ScoreB:05}'
                self._gestion_mort()
                return 'joueur2'

            self.joueurA.animate_sang(loc2px(self.joueurB.yAtt))
            self.joueurA.vie -= 1
            self.vieA(self.joueurA.vie)
            if self.joueurA.vie <= 0:
                self.joueurA.occupe_state(State.mort, self.temps)
                self._gestion_mort()
                return 'joueur2'

            self.snd_play(next(self.sontouche))

            self.joueurA.occupe_state(State.touche1, self.temps)
            self.joueurA.decapite = True

        if self.joueurA.state == State.touche1:
            self.joueurA.gestion_touche1(self.temps)

        if self.joueurA.state == State.tombe:
            rtl = self.joueurA.rtl
            self.joueurA.xAttA = self.joueurA.x_loc() + (4 if rtl else 0)
            self.joueurA.attente = 0
            self.joueurA.reset_xX_back()
            self.joueurA.reset_yX()
            if self.joueurB.state != State.rouladeAV:
                self.joueurA.animate_sang(loc2px(self.joueurB.yAtt))
                self.serpentA.animate('bite')
                self.joueurA.vie -= 1
                self.vieA(self.joueurA.vie)
                Game.ScoreB += 100
                self.txtScoreB.msg = f'{Game.ScoreB:05}'

            if self.joueurA.vie <= 0:
                self.joueurA.occupe_state(State.mort, self.temps)
                self._gestion_mort()
                return 'joueur2'
            if self.joueurB.state == State.coupdetete:
                Game.ScoreB += 150
                self.txtScoreB.msg = f'{Game.ScoreB:05}'
                self.snd_play('coupdetete.ogg')
            if self.joueurB.state == State.coupdepied:
                Game.ScoreB += 150
                self.txtScoreB.msg = f'{Game.ScoreB:05}'
                self.snd_play('coupdepied.ogg')
            self.joueurA.occupe_state(State.tombe1, self.temps)

        if self.joueurA.state == State.tombe1:
            self.joueurA.gestion_tombe1(self.temps, self.joueurB)

        # bruit des epees  et decapitations loupees
        if self.joueurA.state == State.clingD:
            if self.joueurB.state == State.decapite and not self.joueurA.decapite:
                self.joueurA.occupe_state(State.touche, self.temps)
                return 'gestion'
            if self.joueurB.state == State.genou:
                self.joueurA.occupe_state(State.touche, self.temps)
                return 'gestion'
            distance = abs(self.joueurB.x_loc() - self.joueurA.x_loc())
            if distance < 12:
                self.snd_play(next(self.soncling))
            self.joueurA.state = State.protegeD
            return 'joueur2'

        if self.joueurA.state == State.clingH:
            distance = abs(self.joueurB.x_loc() - self.joueurA.x_loc())
            if distance < 12:
                self.snd_play(next(self.soncling))
            self.joueurA.state = State.protegeH
            return 'joueur2'

        self._gestion_mort()

        return 'joueur2'

    def _gestion_mort(self):
        if self.joueurA.state == State.mort:
            if self.temps == self.joueurA.reftemps:
                self.chronoOn = False
                # noinspection PyTypeChecker
                self.change_layer(self.joueurA, 2)
                self.joueurA.animate('mort')
                self.joueurB.occupe_state(State.vainqueurKO, self.temps)
                self.snd_play('mortKO.ogg')

        elif self.joueurA.state == State.mortdecap:
            if self.temps == self.joueurA.reftemps + 126:
                self.animate_gnome()
                self.joueurA.reftemps = self.temps
            elif self.temps == self.joueurA.reftemps:
                self.chronoOn = False
                # noinspection PyTypeChecker
                self.change_layer(self.joueurA, 2)
                self.joueurA.animate('mortdecap')
                self.joueurB.occupe_state(State.vainqueur, self.temps)
                self.snd_play('mortdecap.ogg')

        elif self.joueurA.state == State.mortSORCIER:
            if self.temps > self.joueurA.reftemps + 86:
                self.joueurA.state = State.sorcierFINI
                self._loose()
            elif self.temps == self.joueurA.reftemps:
                self.joueurB.is_stopped = True
                self.joueurA.animate('mortSORCIER')

    @staticmethod
    def _center_txt(msg):
        txt = Txt(CHAR_H, msg,
                  color=(34, 34, 153), bgcolor=Theme.BLACK)
        txt.rect.topleft = (SCREEN_SIZE[0] / 2 - txt.rect.w / 2, loc2px(11))
        bg = StaticSprite((0, 0), 'fill',
                          w=(txt.rect.w + 2 * CHAR_W) / SCALE,
                          h=(txt.rect.h + 2 * CHAR_H) / SCALE,
                          fill=Theme.BLACK)
        bg.rect.topleft = (txt.rect.topleft[0] - CHAR_W,
                           txt.rect.topleft[1] - CHAR_H)
        return bg, txt

    def _win(self):
        self.joueurB.kill()
        self.joueurB.occupe_state(State.mortSORCIER, self.temps)
        self.joueurA.occupe_state(State.fini, self.temps)
        self.joueurA.set_anim_frame('vainqueur', 2)
        self.joueurA.x = loc2px(17)
        bg, txt = self._center_txt('Thanks big boy.')
        # noinspection PyTypeChecker
        self.add(
            StaticSprite(loc(16.5, 14), 'sprites/marianna.gif'),
            StaticSprite((186 * SCALE, 95 * SCALE), 'fill',
                         w=15, h=20, fill=Theme.BLACK),
            StaticSprite((185 * SCALE, 113 * SCALE), 'fill',
                         w=18, h=2.1, fill=Theme.BLACK),
            bg, txt)
        self.jeu = 'gagne'

    def _loose(self):
        bg, txt = self._center_txt('Your end has come!')
        # noinspection PyTypeChecker
        self.add(bg, txt)
        self.jeu = 'perdu'

    def _joueur2(self):
        # debut joueur 2
        ja = self.joueurA
        jb = self.joueurB
        degat = False
        if Game.Sorcier:
            if ja.x_loc() <= jb.x_loc() + 4:
                self._win()
                return None
        else:
            degat, score = jb.degat(ja)
            if score:
                Game.ScoreA += score
                self.txtScoreA.msg = f'{Game.ScoreA:05}'

        if degat or jb.occupe:
            return 'gestionB'
        return 'clavierB'

    def _clavierB(self):
        self.joueurB.clavierX = 7
        self.joueurB.clavierY = 7
        self.joueurB.levier = Levier.neutre
        if self.joueurB.sortie:
            self.joueurB.attaque = False
            self.joueurB.levier = self.joueurB.recule_levier()
            self.joueurB.action(self.temps)
            return 'gestionB'
        if Game.Partie == 'vs':
            self.joueurB.clavier()
        # *****************************************
        # ******* Intelligence Artificielle *******
        # *****************************************
        if Game.Partie == 'solo':
            distance = abs(self.joueurB.x_loc() - self.joueurA.x_loc())
            # ***************************IA de 1,2,3,6
            if Game.IA in (0, 1, 2, 3, 6):
                if distance >= 15:
                    # quand trop loin
                    self.joueurB.occupe_state(State.rouladeAV, self.temps)
                    return 'gestionB'
                if Game.IA == 6:
                    if distance < 15:
                        if self.joueurA.state == State.decapite:
                            self.joueurB.occupe_state(State.genou, self.temps)
                            return 'gestionB'
                if Game.IA == 3:
                    if distance < 15:
                        if self.joueurB.infoDegatT > 2:
                            if self.joueurA.state == State.decapite:
                                self.joueurB.state = State.assis2
                                return 'gestionB'
                        if self.joueurA.state == State.decapite:
                            self.joueurB.state = State.protegeD
                            self.joueurB.reftemps = self.temps
                            return 'gestionB'
                if distance == 12 and self.joueurA.state == State.debout:
                    self.joueurB.occupe_state(State.decapite, self.temps)
                    return 'gestionB'
                if 9 < distance < 15:  # pour se rapprocher
                    if self.joueurA.levier == self.joueurA.recule_levier():
                        self.joueurB.state = State.debout
                        return 'gestionB'
                    self.joueurB.levier = self.joueurB.avance_levier()
                elif distance == 9:
                    if self.joueurA.attente > 100:
                        self.joueurB.levier = self.joueurB.avance_levier()
                    elif self.joueurA.state == State.rouladeAR:
                        self.joueurB.occupe_state(State.devant, self.temps)
                        return 'gestionB'
                    elif self.joueurA.occupe:
                        self.joueurB.levier = self.joueurB.avance_levier()
                elif 6 < distance < 9:  # distance de combat 1
                    # pour autoriser les croisements
                    if not Game.Demo and self.joueurA.state == State.rouladeAV:
                        self.joueurB.occupe_state(State.saute, self.temps)
                        return 'gestionB'
                    # pour se rapprocher
                    if self.joueurA.state == State.rouladeAR:
                        self.joueurB.occupe_state(State.genou, self.temps)
                        return 'gestionB'
                    if self.joueurA.levier == self.joueurA.recule_levier():
                        self.joueurB.occupe_state(State.araignee, self.temps)
                        return 'gestionB'
                    # pour eviter les degats repetitifs
                    if Game.IA > 1:
                        if self.joueurB.infoDegatG > 4:
                            if self.joueurA.state in (State.assis2, State.genou):
                                self.joueurB.occupe_state(State.genou, self.temps)
                                return 'gestionB'
                        if self.joueurB.infoDegatG > 2:
                            if self.joueurA.state in (State.assis2, State.rouladeAV):
                                self.joueurB.occupe_state(State.rouladeAV, self.temps)
                                return 'gestionB'
                        if self.joueurB.infoDegatT > 2:
                            if self.joueurA.state == State.cou:
                                self.joueurB.occupe_state(State.rouladeAV, self.temps)
                                return 'gestionB'
                        if self.joueurB.infoDegatF > 2:
                            if self.joueurA.state == State.front:
                                self.joueurB.occupe_state(State.rouladeAV, self.temps)
                                return 'gestionB'
                    # pour alterner les attaques
                    if self.joueurB.infoCoup == 0:
                        self.joueurB.occupe_state(State.coupdepied, self.temps)
                        self.joueurB.infoCoup += 1
                        return 'gestionB'
                    if self.joueurB.infoCoup == 1:
                        self.joueurB.occupe_state(State.debout, self.temps)
                        self.joueurB.infoCoup += 1
                        return 'gestionB'
                    if self.joueurB.infoCoup == 2:
                        self.joueurB.occupe_state(State.araignee, self.temps)
                        self.joueurB.infoCoup += 1
                        return 'gestionB'
                    if self.joueurB.infoCoup == 3:
                        self.joueurB.occupe_state(State.debout, self.temps)
                        self.joueurB.infoCoup += 1
                        return 'gestionB'
                    if self.joueurB.infoCoup == 4:
                        self.joueurB.occupe_state(State.assis2, self.temps)
                        self.joueurB.infoCoup += 1
                        return 'gestionB'
                    if self.joueurB.infoCoup == 5:
                        self.joueurB.occupe_state(State.genou, self.temps)
                        self.joueurB.infoCoup += 1
                        return 'gestionB'
                    if self.joueurB.infoCoup in (6, 7):
                        self.joueurB.levier = self.joueurB.avance_levier()
                        self.joueurB.infoCoup = 0
                elif distance <= 6:
                    # pour autoriser les croisements
                    if not Game.Demo and self.joueurA.state == State.saute:
                        self.joueurB.occupe_state(State.rouladeAV, self.temps)
                        return 'gestionB'
                    if Game.IA == 3:
                        if self.joueurA.state == State.devant:
                            self.joueurB.state = State.protegeD
                            self.joueurB.reftemps = self.temps
                            return 'gestionB'
                    if Game.IA == 2:
                        if self.joueurA.state == State.genou:
                            self.joueurB.occupe_state(State.saute, self.temps)
                            return 'gestionB'
                    if Game.IA > 1:
                        if self.joueurB.infoDegatG > 4:
                            if self.joueurA.state in (State.assis2, State.genou):
                                if self.joueurB.rtl:
                                    self.joueurB.occupe_state(State.coupdepied, self.temps)
                                else:
                                    self.joueurB.occupe_state(State.genou, self.temps)
                                return 'gestionB'
                            if Game.IA > 2:
                                if self.joueurA.state == State.araignee:
                                    self.joueurB.occupe_state(State.araignee, self.temps)
                                    return 'gestionB'
                        if self.joueurB.infoDegatG > 2:
                            if self.joueurA.state == State.coupdepied:
                                self.joueurB.occupe_state(State.rouladeAV, self.temps)
                                return 'gestionB'
                            if self.joueurB.rtl:
                                if self.joueurA.state in (State.assis2, State.genou):
                                    self.joueurB.occupe_state(State.rouladeAV, self.temps)
                                    return 'gestionB'
                            else:
                                if self.joueurA.state in (State.assis2, State.coupdepied):
                                    self.joueurB.occupe_state(State.genou, self.temps)
                                    return 'gestionB'

                    if self.joueurB.infoCoup == 0:
                        self.joueurB.occupe_state(State.coupdepied, self.temps)
                        self.joueurB.infoCoup += 1
                        return 'gestionB'
                    if self.joueurB.infoCoup == 1:
                        self.joueurB.occupe_state(State.coupdetete, self.temps)
                        self.joueurB.infoCoup += 1
                        return 'gestionB'
                    if self.joueurB.infoCoup == 2:
                        self.joueurB.occupe_state(State.araignee, self.temps)
                        self.joueurB.infoCoup += 1
                        return 'gestionB'
                    if self.joueurB.infoCoup == 3:
                        self.joueurB.occupe_state(State.debout, self.temps)
                        self.joueurB.infoCoup += 1
                        return 'gestionB'
                    if self.joueurB.infoCoup == 4:
                        self.joueurB.occupe_state(State.assis2, self.temps)
                        self.joueurB.infoCoup += 1
                        return 'gestionB'
                    if self.joueurB.infoCoup == 5:
                        self.joueurB.occupe_state(State.genou, self.temps)
                        self.joueurB.infoCoup += 1
                        return 'gestionB'
                    if self.joueurB.infoCoup == 6:
                        self.joueurB.occupe_state(State.debout, self.temps)
                        self.joueurB.infoCoup += 1
                        return 'gestionB'
                    if self.joueurB.infoCoup == 7:
                        self.joueurB.levier = self.joueurB.avance_levier()
                        self.joueurB.infoCoup = 0
            elif Game.IA in (4, 5, 7):
                if distance >= 15:  # quand trop loin
                    self.joueurB.occupe_state(State.rouladeAV, self.temps)
                    return 'gestionB'
                if distance < 15:
                    if Game.IA == 7:
                        if self.joueurA.state == State.decapite:
                            self.joueurB.occupe_state(State.rouladeAV, self.temps)
                            return 'gestionB'
                if distance == 12 and self.joueurA.state == State.debout:
                    self.joueurB.occupe_state(State.decapite, self.temps)
                    return 'gestionB'
                if 9 < distance < 15:  # pour se rapprocher
                    if self.joueurA.levier == self.joueurA.recule_levier():
                        self.joueurB.state = State.debout
                        return 'gestionB'
                    self.joueurB.levier = self.joueurB.avance_levier()
                elif distance == 9:
                    if self.joueurA.attente > 100:
                        self.joueurB.occupe_state(State.decapite, self.temps)
                        return 'gestionB'
                    if Game.Demo:
                        if self.joueurB.rtl:
                            if self.joueurA.attente > 25:
                                self.joueurB.occupe_state(State.decapite, self.temps)
                                return 'gestionB'
                        else:
                            if self.joueurA.attente > 100:
                                self.joueurB.occupe_state(State.decapite, self.temps)
                                return 'gestionB'
                    if self.joueurA.state == State.rouladeAR:
                        self.joueurB.occupe_state(State.genou, self.temps)
                        return 'gestionB'
                    if Game.IA < 7:
                        if self.joueurA.occupe:
                            self.joueurB.occupe_state(State.rouladeAV, self.temps)
                            return 'gestionB'
                    if Game.IA == 7:
                        if self.joueurA.occupe:
                            self.joueurB.levier = self.joueurB.avance_levier()
                elif 6 < distance < 9:  # distance de combat 1
                    # pour autoriser les croisements
                    if not Game.Demo and self.joueurA.state == State.rouladeAV:
                        self.joueurB.occupe_state(State.saute, self.temps)
                        return 'gestionB'
                    # pour se rapprocher
                    if self.joueurA.state == State.rouladeAR:
                        self.joueurB.occupe_state(State.genou, self.temps)
                        return 'gestionB'
                    if self.joueurA.levier == self.joueurA.recule_levier():
                        self.joueurB.occupe_state(State.araignee, self.temps)
                        return 'gestionB'
                    # plus l'IA est forte, plus il y des des coups imposs avant infocoupB ou infodegat
                    if Game.IA == 5:
                        if self.joueurA.state == State.front:
                            self.joueurB.state = State.protegeH
                            self.joueurB.reftemps = self.temps
                            return 'gestionB'
                    # pour eviter les degats repetitifs
                    if self.joueurB.infoDegatG > 4:
                        if self.joueurA.state in (State.assis2, State.genou, State.araignee):
                            self.joueurB.occupe_state(State.araignee, self.temps)
                            return 'gestionB'
                    if self.joueurB.infoDegatG > 2:
                        if self.joueurA.state in (State.assis2, State.genou, State.araignee):
                            self.joueurB.occupe_state(State.rouladeAV, self.temps)
                            return 'gestionB'
                    if self.joueurB.infoDegatT > 2:
                        if self.joueurA.state == State.cou:
                            self.joueurB.occupe_state(State.genou, self.temps)
                            return 'gestionB'
                    if self.joueurB.infoDegatF > 2:
                        if Game.IA < 7:
                            if self.joueurA.state == State.front:
                                self.joueurB.occupe_state(State.rouladeAV, self.temps)
                                return 'gestionB'
                    # pour alterner les attaques
                    if self.joueurB.infoCoup == 0:
                        self.joueurB.occupe_state(State.devant, self.temps)
                        self.joueurB.infoCoup += 1
                        return 'gestionB'
                    if self.joueurB.infoCoup == 1:
                        self.joueurB.occupe_state(State.front, self.temps)
                        self.joueurB.infoCoup += 1
                        return 'gestionB'
                    if self.joueurB.infoCoup == 2:
                        self.joueurB.occupe_state(State.araignee, self.temps)
                        self.joueurB.infoCoup += 1
                        return 'gestionB'
                    if self.joueurB.infoCoup == 3:
                        self.joueurB.occupe_state(State.araignee, self.temps)
                        self.joueurB.infoCoup += 1
                        return 'gestionB'
                    if self.joueurB.infoCoup == 4:
                        self.joueurB.occupe_state(State.cou, self.temps)
                        self.joueurB.infoCoup += 1
                        return 'gestionB'
                    if self.joueurB.infoCoup == 5:
                        self.joueurB.levier = self.joueurB.avance_levier()
                        self.joueurB.infoCoup = 0
                elif distance <= 6:
                    # pour autoriser les croisements
                    if not Game.Demo and self.joueurA.state == State.saute:
                        self.joueurB.occupe_state(State.rouladeAV, self.temps)
                        return 'gestionB'
                    if Game.IA > 4:
                        if self.joueurA.state == State.devant:
                            self.joueurB.state = State.protegeD
                            self.joueurB.reftemps = self.temps
                            return 'gestionB'
                    if 4 < Game.IA < 7:
                        if self.joueurA.state == State.genou:
                            self.joueurB.occupe_state(State.saute, self.temps)
                            return 'gestionB'
                    if self.joueurB.infoDegatG > 4:
                        if self.joueurA.state in (State.assis2, State.genou, State.araignee):
                            self.joueurB.occupe_state(State.araignee, self.temps)
                            return 'gestionB'
                    if self.joueurB.infoDegatG > 2:
                        if self.joueurA.state == State.coupdepied:
                            self.joueurB.occupe_state(State.rouladeAV, self.temps)
                            return 'gestionB'
                        if self.joueurA.state in (State.assis2, State.genou, State.araignee):
                            self.joueurB.occupe_state(State.rouladeAV, self.temps)
                            return 'gestionB'
                    if self.joueurB.infoCoup == 0:
                        self.joueurB.occupe_state(State.coupdepied, self.temps)
                        self.joueurB.infoCoup += 1
                        return 'gestionB'
                    if self.joueurB.infoCoup == 1:
                        self.joueurB.occupe_state(State.coupdetete, self.temps)
                        self.joueurB.infoCoup += 1
                        return 'gestionB'
                    if self.joueurB.infoCoup == 2:
                        self.joueurB.occupe_state(State.araignee, self.temps)
                        self.joueurB.infoCoup += 1
                        return 'gestionB'
                    if self.joueurB.infoCoup == 3:
                        self.joueurB.occupe_state(State.genou, self.temps)
                        self.joueurB.infoCoup += 1
                        return 'gestionB'
                    if self.joueurB.infoCoup == 4:
                        self.joueurB.occupe_state(State.genou, self.temps)
                        self.joueurB.infoCoup += 1
                        return 'gestionB'
                    if self.joueurB.infoCoup == 5:
                        self.joueurB.levier = self.joueurB.avance_levier()
                        self.joueurB.infoCoup = 0
        # redirection suivant les touches
        if self.joueurB.levier != Levier.neutre:
            self.joueurB.action(self.temps)
            return 'gestionB'
        # actions si aucune touche n'a ete touchee
        self.joueurB.protegeD = False
        self.joueurB.protegeH = False
        self.joueurB.attente += 1
        # pour se relever
        self.joueurB.assis = False
        if self.joueurB.state == State.assis2:
            self.joueurB.occupe_state(State.releve, self.temps)
            return 'gestionB'
        # attente des 5 secondes
        if self.joueurB.attente > FRAME_RATE * 5:
            self.joueurB.occupe_state(State.attente, self.temps)
            return 'gestionB'
        self.joueurB.state = State.debout
        return 'gestionB'

    def _gestionB(self):
        # ***********************************
        # *********gestion joueur 2**********
        # ***********************************
        if self.joueurB.state == State.debout:
            self.joueurB.gestion_debout(self.temps, Game.Partie == 'solo')
            return 'colision'

        if self.joueurB.state == State.attente:
            self.joueurB.gestion_attente(self.temps)
            return 'colision'

        if self.joueurB.state == State.avance:
            self.joueurB.gestion_avance(self.temps, self.joueurA,
                                        self.soncling, self.songrogne)
            return 'colision'

        if self.joueurB.state == State.recule:
            self.joueurB.gestion_recule(self.temps)
            return 'colision'

        if self.joueurB.state == State.saute:
            self.joueurB.gestion_saute(self.temps)
            return 'colision'

        if self.joueurB.state == State.assis:
            self.joueurB.gestion_assis(self.temps)
            return 'colision'

        if self.joueurB.state == State.assis2:
            self.joueurB.gestion_assis2(self.temps, self.joueurA,
                                        self.soncling, self.songrogne,
                                        Game.Partie == 'solo')
            return 'colision'

        if self.joueurB.state == State.releve:
            self.joueurB.gestion_releve(self.temps, self.joueurA,
                                        self.soncling, self.songrogne)
            return 'colision'

        if self.joueurB.state == State.rouladeAV:
            self.joueurB.gestion_rouladeAV(self.temps, self.joueurA)
            return 'colision'

        if self.joueurB.state == State.rouladeAR:
            self.joueurB.gestion_rouladeAR(self.temps)
            return 'colision'

        if self.joueurB.state == State.protegeH1:
            self.joueurB.gestion_protegeH1(self.temps)
            return 'colision'

        if self.joueurB.state == State.protegeH:
            self.joueurB.gestion_protegeH(self.temps, self.joueurA,
                                          self.soncling, self.songrogne)
            return 'colision'

        if self.joueurB.state == State.protegeD1:
            self.joueurB.gestion_protegeD1(self.temps)
            return 'colision'

        if self.joueurB.state == State.protegeD:
            self.joueurB.gestion_protegeD(self.temps)
            return 'colision'

        if self.joueurB.state == State.cou:  # ****attention au temps sinon il saute
            self.joueurB.gestion_cou(self.temps, self.joueurA,
                                     self.soncling, self.songrogne)
            return 'colision'

        if self.joueurB.state == State.devant:
            self.joueurB.gestion_devant(self.temps, self.joueurA,
                                        self.soncling, self.songrogne)
            return 'colision'

        if self.joueurB.state == State.genou:
            self.joueurB.gestion_genou(self.temps, self.joueurA,
                                       self.soncling, self.songrogne)

        if self.joueurB.state == State.araignee:
            self.joueurB.gestion_araignee(self.temps, self.joueurA,
                                          self.soncling, self.songrogne)

        if self.joueurB.state == State.coupdepied:
            self.joueurB.gestion_coupdepied(self.temps, self.joueurA)

        if self.joueurB.state == State.coupdetete:
            self.joueurB.gestion_coupdetete(self.temps)

        if self.joueurB.state == State.decapite:
            self.joueurB.gestion_decapite(self.temps)

        if self.joueurB.state == State.front:
            self.joueurB.gestion_front(self.temps, self.joueurA,
                                       self.soncling, self.songrogne)

        if self.joueurB.state == State.retourne:
            self.joueurB.gestion_retourne(self.temps)

        if self.joueurB.state == State.vainqueur:
            self.joueurB.gestion_vainqueur()

        if self.joueurB.state == State.vainqueurKO:
            self.joueurB.gestion_vainqueurKO(self.temps, self.joueurA)
            if self.temps > self.joueurB.reftemps + 230:
                self.animate_gnome()
                self.joueurB.reftemps = self.temps
                return None
            elif self.temps == self.joueurA.reftemps + 36:
                return 'colision'

        # ******degats B ******
        if self.joueurB.state == State.touche:
            rtl = self.joueurB.rtl
            self.joueurB.attente = 0
            self.joueurB.xAtt = self.joueurB.x_loc() + (4 if rtl else 0)
            self.joueurB.reset_xX_back()
            self.joueurB.reset_yX()
            if self.joueurA.state == State.coupdepied:
                self.joueurB.state = State.tombe
                return 'gestionB'

            self.serpentB.animate('bite')

            if self.joueurA.state == State.decapite and self.joueurB.decapite:
                self.joueurB.occupe_state(State.mortdecap, self.temps)
                Game.ScoreA += 250
                self.txtScoreA.msg = f'{Game.ScoreA:05}'
                self._gestion_mortB()
                return 'colision'

            self.joueurB.animate_sang(loc2px(self.joueurA.yAtt))
            self.joueurB.vie -= 1
            self.vieB(self.joueurB.vie)
            if self.joueurB.vie <= 0:
                self.joueurB.occupe_state(State.mort, self.temps)
                self._gestion_mortB()
                return 'colision'

            self.snd_play(next(self.sontouche))

            self.joueurB.occupe_state(State.touche1, self.temps)
            self.joueurB.decapite = True

        if self.joueurB.state == State.touche1:
            self.joueurB.gestion_touche1(self.temps)

        if self.joueurB.state == State.tombe:
            rtl = self.joueurB.rtl
            self.joueurB.xAttA = self.joueurB.x_loc() + (4 if rtl else 0)
            self.joueurB.attente = 0
            self.joueurB.reset_xX_back()
            self.joueurB.reset_yX()
            if self.joueurA.state != State.rouladeAV:
                self.joueurB.animate_sang(loc2px(self.joueurA.yAtt))
                self.serpentB.animate('bite')
                self.joueurB.vie -= 1
                self.vieB(self.joueurB.vie)
                Game.ScoreA += 100
                self.txtScoreA.msg = f'{Game.ScoreA:05}'

            if self.joueurB.vie <= 0:
                self.joueurB.occupe_state(State.mort, self.temps)
                self._gestion_mortB()
                return 'colision'
            if self.joueurA.state == State.coupdetete:
                Game.ScoreA += 150
                self.txtScoreA.msg = f'{Game.ScoreA:05}'
                self.snd_play('coupdetete.ogg')
            if self.joueurA.state == State.coupdepied:
                Game.ScoreA += 150
                self.txtScoreA.msg = f'{Game.ScoreA:05}'
                self.snd_play('coupdepied.ogg')
            self.joueurB.occupe_state(State.tombe1, self.temps)

        if self.joueurB.state == State.tombe1:
            self.joueurB.gestion_tombe1(self.temps, self.joueurA)

        # bruit des epees  et decapitations loupees
        if self.joueurB.state == State.clingD:
            if self.joueurA.state == State.decapite and not self.joueurB.decapite:
                self.joueurB.occupe_state(State.touche, self.temps)
                return 'gestionB'
            if self.joueurA.state == State.genou:
                self.joueurB.occupe_state(State.touche, self.temps)
                return 'gestionB'
            distance = abs(self.joueurB.x_loc() - self.joueurA.x_loc())
            if distance < 12:
                self.snd_play(next(self.soncling))
            self.joueurB.state = State.protegeD
            return 'colision'

        if self.joueurB.state == State.clingH:
            distance = abs(self.joueurB.x_loc() - self.joueurA.x_loc())
            if distance < 12:
                self.snd_play(next(self.soncling))
            self.joueurB.state = State.protegeH
            return 'colision'

        if self.joueurB.state == State.sorcier:
            self.joueurB.gestion_sorcier(self.temps)
            return 'colision'

        self._gestion_mortB()

        return 'colision'

    def _gestion_mortB(self):
        if self.joueurB.state == State.mort:
            if self.temps == self.joueurB.reftemps:
                self.chronoOn = False
                # noinspection PyTypeChecker
                self.change_layer(self.joueurB, 2)
                self.joueurB.animate('mort')
                self.joueurA.occupe_state(State.vainqueurKO, self.temps)
                self.snd_play('mortKO.ogg')

        elif self.joueurB.state == State.mortdecap:
            if self.temps == self.joueurB.reftemps + 126:
                self.animate_gnome()
                self.joueurB.reftemps = self.temps
            elif self.temps == self.joueurB.reftemps:
                self.chronoOn = False
                # noinspection PyTypeChecker
                self.change_layer(self.joueurB, 2)
                self.joueurB.animate('mortdecap')
                self.joueurA.occupe_state(State.vainqueur, self.temps)
                self.snd_play('mortdecap.ogg')

    def _colision(self, ja: Barbarian, jb: Barbarian):
        # ***************************************
        # ***********   COLISION   **************
        # ***************************************
        jax = ja.x_loc()
        jbx = jb.x_loc()
        if (abs(jbx - jax) < 4
                and not (ja.state == State.saute and jb.state == State.rouladeAV)
                and not (jb.state == State.saute and ja.state == State.rouladeAV)):
            # pour empecher que A entre dans B
            if (ja.levier == ja.avance_levier()
                    or ja.state in (State.rouladeAV, State.decapite,
                                    State.debout, State.coupdepied)):
                if ja.xLocPrev != jax:
                    ja.x = loc2px(jax - (-1 if ja.rtl else 1))

            # pour empecher que B entre dans A
            if (jb.levier == jb.avance_levier()
                    or jb.state in (State.rouladeAV, State.decapite,
                                    State.debout, State.coupdepied)):
                if jb.xLocPrev != jbx:
                    jb.x = loc2px(jbx - (-1 if jb.rtl else 1))

        left, right = self._colision_borders(ja, jb)
        if jax < left:
            ja.x = loc2px(left)
        elif jax > right:
            ja.x = loc2px(right)
        #
        left, right = self._colision_borders(jb, ja)
        if jbx < left:
            jb.x = loc2px(left)
        elif jbx > right:
            jb.x = loc2px(right)
        return None

    def _colision_borders(self, joueur: Barbarian, opponent: Barbarian):
        return ((0, 40) if any((self.entree, self.entreesorcier,
                                joueur.sortie, opponent.sortie)) else
                (5, 32) if joueur.state == State.retourne else
                (9, 32) if joueur.rtl else
                (5, 28))

    def vieA(self, num):
        self.vieA0.set_anim_frame('vie', max(0, min(6, 6 - num)))
        self.vieA1.set_anim_frame('vie', max(0, min(6, 12 - num)))

    def vieB(self, num):
        self.vieB0.set_anim_frame('vie_rtl', max(0, min(6, 6 - num)))
        self.vieB1.set_anim_frame('vie_rtl', max(0, min(6, 12 - num)))

    def _gnome(self):
        if self.joueurA.state in (State.mort, State.mortdecap):
            mort, vainqueur = self.joueurA, self.joueurB
        elif self.joueurB.state in (State.mort, State.mortdecap):
            mort, vainqueur = self.joueurB, self.joueurA
        else:
            return
        gnome = self.gnomeSprite

        if mort.state == State.mort:
            if (gnome.rect.right >= mort.rect.right + CHAR_W
                    and mort.anim != 'mortgnome'):
                mort.top_left = mort.rect.topleft
                mort.animate('mortgnome')
        elif mort.state == State.mortdecap:
            if (gnome.rect.right >= mort.rect.right + CHAR_W
                    and mort.anim != 'mortdecapgnome'):
                mort.top_left = mort.rect.topleft
                mort.animate('mortdecapgnome')
            if mort.teteSprite.alive():
                if gnome.rect.right >= mort.teteSprite.rect.center[0]:
                    mort.animate_football(self.temps)
                if not mort.teteSprite.is_stopped:
                    if self.temps == mort.reftemps + 38:
                        self.snd_play('tete.ogg')
                    elif self.temps == mort.reftemps + 83:
                        self.snd_play('tete.ogg')
                if mort.teteSprite.rect.left > SCREEN_SIZE[0]:
                    mort.stop_football()
        if gnome.alive() and px2loc(gnome.x) > 41:
            gnome.kill()
            if Game.Partie == 'vs':
                vainqueur.bonus = True
            if Game.Partie == 'solo':
                mort.kill()
                vainqueur.sortie = True
                vainqueur.occupe = False

    def tick_chrono(self, current_time, ja: Barbarian, jb: Barbarian):
        if self.chrono == 0:
            self.chrono = current_time
        elif current_time > self.chrono:
            self.chrono += 1000
            Game.Chronometre -= 1
            if Game.Chronometre < 1:
                Game.Chronometre = 0
                self.chronoOn = False
                if Game.Partie == 'vs':
                    ja.sortie = jb.sortie = True
                    ja.occupe = jb.occupe = False
                    self.tempsfini = True
            self.txtChronometre.msg = f'{Game.Chronometre:02}'

    def joueurA_bonus(self, jbx):
        if Game.Chronometre > 0:
            Game.ScoreA += 10
            Game.Chronometre -= 1
            self.txtChronometre.msg = f'{Game.Chronometre:02}'
            self.txtScoreA.msg = f'{Game.ScoreA:05}'
        elif jbx >= 37:
            self.joueurA.sortie = True
            self.joueurA.occupe = False

    def joueurB_bonus(self, jax):
        if Game.Chronometre > 0:
            Game.ScoreB += 10
            Game.Chronometre -= 1
            self.txtChronometre.msg = f'{Game.Chronometre:02}'
            self.txtScoreB.msg = f'{Game.ScoreB:05}'
        elif jax >= 37:
            self.joueurB.sortie = True
            self.joueurB.occupe = False

    def do_entree(self, jax, jbx):
        if self.serpentA.anim == 'idle' and jax >= 3:
            self.serpentA.animate('bite')
            self.serpentB.animate('bite')
        if jax >= 13:
            self.joueurA.x = loc2px(13)
        if jbx <= 22:
            self.joueurB.x = loc2px(22)
        if jax >= 13 or jbx <= 22:
            self.joueurA.set_anim_frame('debout', 0)
            self.joueurB.set_anim_frame('debout', 0)
            self.entree = False
            if Game.Partie == 'vs':
                self.chronoOn = True

    def is_sortiedA(self, jax, jbx):
        if not self.tempsfini:
            if jbx >= 35 and (jax <= 0 or 38 <= jax):
                if Game.Partie == 'solo':
                    if Game.Demo:
                        self.finish()
                    elif Game.IA < 7:
                        self.next_stage()
                    else:
                        self.start_sorcier()
                elif Game.Partie == 'vs':
                    self.next_stage()
                return True  #
        elif (jax < 2 and 38 < jbx) or (jbx < 2 and 38 < jax):
            self.next_stage()
            return True  #
        return False  #

    def is_sortiedB(self, jax, jbx):
        if not self.tempsfini:
            if jax >= 35 and (jbx <= 0 or 38 <= jbx):
                if Game.Partie == 'solo':
                    self.finish()
                elif Game.Partie == 'vs':
                    self.next_stage()
                return True  #
        return False  #

    def update(self, current_time, *args):
        ja = self.joueurA
        jb = self.joueurB
        jax = self.joueurA.x_loc()
        jbx = self.joueurB.x_loc()
        ja.xLocPrev = jax  # for collision
        jb.xLocPrev = jbx  # for collision
        super(Battle, self).update(current_time, *args)
        if self.jeu in ('gagne', 'perdu'):
            return
        if self.chronoOn:
            self.tick_chrono(current_time, ja, jb)
        #
        self.temps += 1
        self.update_internal(ja, jax, jb, jbx)
        #
        if self.opts.debug > 1:
            self.debug(ja, jb)

    def update_internal(self, ja, jax, jb, jbx):
        if ja.bonus:
            self.joueurA_bonus(jbx)
        if jb.bonus:
            self.joueurB_bonus(jax)
        if self.lancerintro:
            self.lancerintro = False
            self.snd_play('prepare.ogg')

        if self.entree:
            self.do_entree(jax, jbx)
            return  #

        if ja.sortie:
            if self.is_sortiedA(jax, jbx):
                return  #
            goto = 'clavier'
        elif jb.sortie:
            if self.is_sortiedB(jax, jbx):
                return  #
            goto = 'clavierB'
        elif self.gnome:
            self._gnome()
            return  #
        else:
            goto = self._degats()

        while goto:
            if goto == 'clavier':
                goto = self._clavier()
            elif goto == 'gestion':
                goto = self._gestion()
            elif goto == 'joueur2':
                goto = self._joueur2()
            elif goto == 'clavierB':
                goto = self._clavierB()
            elif goto == 'gestionB':
                goto = self._gestionB()
            elif goto == 'colision':
                goto = self._colision(ja, jb)
            else:
                goto = None

    def debug(self, ja, jb):
        self.jAstate.msg = f'AS: {ja.state}'
        self.jAlevier.msg = f'AL: {ja.levier}'
        self.jAtemps.msg = f'AT: {ja.reftemps} ({self.temps - ja.reftemps})'
        self.jBstate.msg = f'BS: {jb.state}'
        self.jBlevier.msg = f'BL: {jb.levier}'
        self.jBtemps.msg = f'BT: {jb.reftemps} ({self.temps - jb.reftemps})'
        self.debugTemps.msg = f'T: {self.temps}'
        distance = abs(jb.x_loc() - ja.x_loc())
        self.distance.msg = f'A <- {distance:>2} -> B'
        if self.debugAttArea:
            self.jAAtt.move_to(loc2px(ja.xAtt), loc2px(ja.yAtt))
            self.jAF.move_to(loc2px(ja.xF), loc2px(ja.yF))
            self.jAT.move_to(loc2px(ja.xT), loc2px(ja.yT))
            self.jAM.move_to(loc2px(ja.xM), loc2px(ja.yM))
            self.jAG.move_to(loc2px(ja.xG), loc2px(ja.yG))
            #
            self.jBAtt.move_to(loc2px(jb.xAtt), loc2px(jb.yAtt))
            self.jBF.move_to(loc2px(jb.xF), loc2px(jb.yF))
            self.jBT.move_to(loc2px(jb.xT), loc2px(jb.yT))
            self.jBM.move_to(loc2px(jb.xM), loc2px(jb.yM))
            self.jBG.move_to(loc2px(jb.xG), loc2px(jb.yG))
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
            Game.Country = 'europe'
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
            StaticSprite((280 * SCALE, 0), 'menu/playerB.png',
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
            StaticSprite((100 * SCALE, 40 * SCALE), 'menu/controls1.gif'),
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
            StaticSprite((100 * SCALE, 40 * SCALE), 'menu/controls2.gif'),
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
            Txt(sz, '                    ', col, loc(21, 4)),
            Txt(sz, '  Palace Software   ', col, loc(21, 5)),
            Txt(sz, '         1987       ', col, loc(21, 6)),
            Txt(sz, ' AMIGA 500 version  ', col, loc(21, 7)),
            Txt(sz, '                    ', col, loc(21, 8)),
            Txt(sz, 'created and designed', col, loc(21, 9)),
            Txt(sz, '  by STEVE BROWN    ', col, loc(21, 10)),
            Txt(sz, '                    ', col, loc(21, 11)),
            Txt(sz, '     programmer     ', col, loc(21, 12)),
            Txt(sz, ' Richard Leinfellner', col, loc(21, 13)),
            Txt(sz, '                    ', col, loc(21, 14)),
            Txt(sz, '  assistant artist  ', col, loc(21, 15)),
            Txt(sz, '                    ', col, loc(21, 16)),
            Txt(sz, '     GARY CARR      ', col, loc(21, 17)),
            Txt(sz, '                    ', col, loc(21, 18)),
            Txt(sz, '     JO WALKER      ', col, loc(21, 19)),
            Txt(sz, '                    ', col, loc(21, 20)),
            Txt(sz, '       music        ', col, loc(21, 21)),
            Txt(sz, '   RICHARD JOSEPH   ', col, loc(21, 22)),
            Txt(sz, '                    ', col, loc(21, 23)),
            Txt(sz, 'FL clone http://barbarian.1987.free.fr', col, loc(2, 25)),
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
