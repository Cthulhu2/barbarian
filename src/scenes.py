# -*- coding: utf-8 -*-
from itertools import cycle

from pygame import Surface
from pygame.locals import *
from pygame.sprite import LayeredDirty
from pygame.time import get_ticks

from settings import Theme, SCREEN_SIZE, SCALE, FRAME_RATE, CHAR_W, CHAR_H
from sprites import (
    get_snd, Txt, AnimatedSprite, StaticSprite, Barbarian,
    loc2px, loc, State, Levier, Sorcier, Rectangle
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
    return Rectangle(0, 0, CHAR_W * SCALE, CHAR_H * SCALE, color, border_width, lbl)


class Battle(EmptyScene):
    def __init__(self, opts, *,
                 on_esc,
                 on_next,
                 on_menu):
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
        if self.opts.debug:
            self.jAstate = Txt.Debug(loc2px(10), 0)
            self.jBstate = Txt.Debug(loc2px(25), 0)
            self.jAlevier = Txt.Debug(loc2px(10), self.jAstate.rect.bottom)
            self.jBlevier = Txt.Debug(loc2px(25), self.jBstate.rect.bottom)
            self.jAtemps = Txt.Debug(loc2px(10), self.jAlevier.rect.bottom)
            self.jBtemps = Txt.Debug(loc2px(25), self.jBlevier.rect.bottom)
            self.debugTemps = Txt.Debug(loc2px(18), 0)
            # noinspection PyTypeChecker
            self.add(self.jAstate, self.jAlevier, self.jAtemps,
                     self.jBstate, self.jBlevier, self.jBtemps,
                     self.debugTemps, layer=99)
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
        # noinspection PyTypeChecker
        self.add(
            StaticSprite((0, 104 * SCALE),
                         f'stage/{Game.Decor}ARBREG.gif'),
            StaticSprite((272 * SCALE, 104 * SCALE),
                         f'stage/{Game.Decor}ARBRED.gif'),
            layer=2)

        self.joueurA = Barbarian(opts, loc2px(1), loc2px(14),
                                 'spritesA',
                                 rtl=Game.Rtl)
        self.joueurB = Barbarian(opts, loc2px(36), loc2px(14),
                                 f'spritesB/spritesB{Game.IA}',
                                 rtl=not Game.Rtl)
        sz = int(CHAR_H * SCALE)
        if Game.Partie == 'solo' and not Game.Demo:
            Txt(sz, 'ONE  PLAYER', Theme.TXT, loc(16, 25), self)
        elif Game.Partie == 'vs':
            Txt(sz, 'TWO PLAYER', Theme.TXT, loc(16, 25), self)
        elif Game.Demo:
            Txt(sz, 'DEMONSTRATION', Theme.TXT, loc(14, 25), self)

        self.txtScoreA = Txt(sz, f'{Game.ScoreA:05}', Theme.TXT, loc(13, 8), self)
        self.txtScoreB = Txt(sz, f'{Game.ScoreB:05}', Theme.TXT, loc(24, 8), self)

        if Game.Partie == 'vs':
            self.txtChronometre = Txt(sz, f'{Game.Chronometre:02}',
                                      Theme.TXT, loc(19, 8))
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
        self.entree = True
        self.entreesorcier = False
        self.lancerintro = True
        self.lancerfin = True
        self.temps = 0
        self.tempsfini = False
        self.sense = 'normal'  # inverse
        self.gnome = False
        self.soncling = cycle(['block1.ogg', 'block2.ogg', 'block3.ogg'])
        self.songrogne = cycle([0, 0, 0, 'grogne1.ogg', 0, 0, 'grogne1.ogg'])
        self.sontouche = cycle(['touche.ogg', 'touche2.ogg', 'touche3.ogg'])
        self.vieA0 = AnimatedSprite((43.3 * SCALE, 0), anims.vie(), self)
        self.vieA1 = AnimatedSprite((43.3 * SCALE, 11 * SCALE), anims.vie(), self)
        self.vieB0 = AnimatedSprite((276.3 * SCALE, 0), anims.vie(), self)
        self.vieB1 = AnimatedSprite((276.3 * SCALE, 11 * SCALE), anims.vie(), self)

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
        if evt.type == KEYUP and evt.key == K_F12 and self.opts.debug:
            self.debugAttArea = not self.debugAttArea
            if self.debugAttArea:
                self.add(
                    self.jAAtt, self.jAF, self.jAT, self.jAM, self.jAG,
                    self.jBAtt, self.jBF, self.jBT, self.jBM, self.jBG,
                    layer=99)
            else:
                self.remove(
                    self.jAAtt, self.jAF, self.jAT, self.jAM, self.jAG,
                    self.jBAtt, self.jBF, self.jBT, self.jBM, self.jBG)

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

    def _debut(self):
        jax = self.joueurA.x_loc()
        jbx = self.joueurB.x_loc()
        if self.joueurA.bonus:
            Game.ScoreA += 10
            Game.Chronometre -= 1
            if Game.Chronometre <= 0:
                Game.ScoreA -= 10
                if jbx >= 37:
                    self.joueurA.sortie = True
                    self.joueurA.occupe = False
            self.txtScoreA.msg = f'{Game.ScoreA:05}'
        if self.joueurB.bonus:
            Game.ScoreB += 10
            Game.Chronometre -= 1
            if Game.Chronometre <= 0:
                Game.Chronometre = 0
                Game.ScoreB -= 10
                if jax >= 37:
                    self.joueurB.sortie = True
                    self.joueurB.occupe = False
            self.txtScoreB.msg = f'{Game.ScoreB:05}'

        if self.lancerintro:
            get_snd('prepare.ogg').play()
            self.lancerintro = False

        if self.entree:
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
            return None

        if self.joueurA.sortie:
            if not self.tempsfini:
                if jax < 2 and jbx >= 37:
                    if Game.Partie == 'solo':
                        if Game.Demo:
                            self.finish()
                            return None
                        if Game.IA < 7:
                            self.next_stage()
                        else:
                            Game.Sorcier = True
                            self.sense = 'inverse'
                            self.joueurB = Sorcier(loc2px(8),
                                                   loc2px(15))
                            self.add(self.joueurB)
                            self.joueurA.state = State.debout
                            self.joueurA.x = loc2px(36)
                            self.entree = False
                            self.joueurA.sortie = False
                            self.entreesorcier = True
                            self.joueurB.occupe = True
                            self.joueurB.reftemps = self.temps
                    return None
            elif ((self.sense == 'normal' and jax < 2 and jbx >= 37)
                  or (self.sense == 'inverse' and jbx < 2 and jax >= 37)):
                Game.Chronometre = 60
                # SLEEP 1
                self.next_stage()
                return None
        if self.joueurB.sortie:
            if not self.tempsfini:
                if jax >= 37 and jbx >= 37:
                    # SLEEP 1
                    if Game.Partie == 'solo':  # ********** partie solo finie
                        if Game.Demo:
                            self.finish()
                            return None
                        Game.IA = 0
                        Game.ScoreA = 0
                        Game.ScoreB = 0
                        Game.Decor = 'foret'
                        self.finish()
                        return None
                    if Game.Partie == 'vs':
                        self.next_stage()
                        return None
            return 'clavierB'
        if self.gnome:
            return 'gnome'
        return 'degats'

    def _degats(self):
        # degats sur joueurA
        if Game.Sorcier:
            if self.joueurA.x_loc() < 29:
                if self.joueurA.xT < self.joueurB.xAtt <= self.joueurA.xT + 2:
                    if self.joueurB.yAtt == self.joueurA.yT:
                        self.gnome = False
                        if self.jeu == 'perdu':
                            return 'gestion'
                        self.joueurA.state = State.mortSORCIER
                        self.joueurA.occupe = True
                        self.joueurB.reftemps = self.temps
                        self.joueurA.sang = False
                        self.joueurB.state = State.sorcierFINI
                        self.joueurB.occupe = True
                        self.joueurB.reftemps = self.temps
                        self.joueurB.sang = False
                        self.jeu = 'perdu'
                        return 'gestion'
                if self.joueurA.xG <= self.joueurB.xAtt <= self.joueurA.xG + 2:
                    if self.joueurB.yAtt == self.joueurA.yG:
                        self.gnome = False
                        if self.jeu == 'perdu':
                            return 'gestion'
                        self.joueurA.state = State.mortSORCIER
                        self.joueurA.occupe = True
                        self.joueurA.reftemps = self.temps
                        self.joueurA.sang = False
                        self.joueurB.state = State.sorcierFINI
                        self.joueurB.occupe = True
                        self.joueurB.reftemps = self.temps
                        self.joueurB.sang = False
                        self.jeu = 'perdu'
                        return 'gestion'
            if self.joueurA.occupe:
                return 'gestion'
            self.joueurA.sang = False
            return 'clavier'

        if self.sense == 'normal':
            if self.joueurA.x_loc() < self.joueurB.x_loc():
                xAttB = self.joueurB.xAtt
                yAttB = self.joueurB.yAtt
                if xAttB <= self.joueurA.xF and yAttB == self.joueurA.yF:
                    if self.joueurA.state == State.protegeH:
                        self.joueurA.state = State.clingH
                        return 'gestion'
                    self.joueurA.state = State.tombe
                    self.joueurA.infoDegatF += 1
                    return 'gestion'

                if xAttB <= self.joueurA.xT and yAttB == self.joueurA.yT:
                    if self.joueurB.state == State.coupdetete:
                        self.joueurA.state = State.tombe
                        return 'gestion'
                    self.joueurA.state = State.touche
                    Game.ScoreB += 250
                    self.joueurA.infoDegatT += 1
                    return 'gestion'

                if xAttB <= self.joueurA.xM and yAttB == self.joueurA.yM:
                    if self.joueurA.state == State.protegeD:
                        self.joueurA.state = State.clingD
                        return 'gestion'
                    self.joueurA.state = State.touche
                    Game.ScoreB += 250
                    return 'gestion'

                if xAttB <= self.joueurA.xG and yAttB == self.joueurA.yG:
                    if self.joueurB.state == State.araignee:
                        self.joueurA.state = State.tombe
                        return 'gestion'
                    if self.joueurB.state == State.rouladeAV:
                        self.joueurA.state = State.tombe
                        return 'gestion'
                    if self.joueurA.state == State.protegeD:
                        self.joueurA.state = State.clingD
                        return 'gestion'
                    if self.joueurB.state == State.coupdepied:
                        self.joueurA.state = State.tombe
                        self.joueurA.infoDegatG += 1
                        return 'gestion'
                    self.joueurA.state = State.touche
                    Game.ScoreB += 100
                    self.joueurA.infoDegatG += 1
                    return 'gestion'

        if self.sense == 'inverse':
            if self.joueurA.x_loc() > self.joueurB.x_loc():
                xAttB = self.joueurB.xAtt
                yAttB = self.joueurB.yAtt
                if xAttB >= self.joueurA.xF and yAttB == self.joueurA.yF:
                    if self.joueurA.state == State.protegeH:
                        self.joueurA.state = State.clingH
                        return 'gestion'
                    self.joueurA.state = State.tombe
                    return 'gestion'

                if xAttB >= self.joueurA.xT and yAttB == self.joueurA.yT:
                    if self.joueurB.state == State.coupdetete:
                        self.joueurA.state = State.tombe
                        return 'gestion'
                    self.joueurA.state = State.touche
                    Game.ScoreB += 250
                    return 'gestion'

                if xAttB >= self.joueurA.xM and yAttB == self.joueurA.yM:
                    if self.joueurA.state == State.protegeD:
                        self.joueurA.state = State.clingD
                        return 'gestion'
                    self.joueurA.state = State.touche
                    Game.ScoreB += 250
                    return 'gestion'

                if xAttB <= self.joueurA.xG and yAttB == self.joueurA.yG:
                    if self.joueurB.state == State.araignee:
                        self.joueurA.state = State.tombe
                        return 'gestion'
                    if self.joueurB.state == State.rouladeAV:
                        self.joueurA.state = State.tombe
                        return 'gestion'
                    if self.joueurA.state == State.protegeD:
                        self.joueurA.state = State.clingD
                        return 'gestion'
                    if self.joueurB.state == State.coupdepied:
                        self.joueurA.state = State.tombe
                        return 'gestion'
                    self.joueurA.state = State.touche
                    Game.ScoreB += 100
                    return 'gestion'

        if self.joueurA.occupe:
            return 'gestion'
        self.joueurA.sang = False
        return 'clavier'

    def _clavier(self):
        self.joueurA.clavierX = 7
        self.joueurA.clavierY = 7
        self.joueurA.levier = Levier.neutre
        if not Game.Demo:
            self.joueurA.clavier()

        if Game.Demo:
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
                    self.joueurA.levier = Levier.gauche
                    return 'action'

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
                    self.joueurA.occupe_state(State.coupdepied, self.temps)
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
                    self.joueurA.occupe_state(State.genou, self.temps)
                    return 'gestion'
                if self.joueurA.infoCoup == 5:
                    self.joueurA.infoCoup = 0
                    self.joueurA.levier = Levier.gauche
                    return 'action'

            if self.sense == 'inverse':
                self.on_menu()
                return None

        # redirection suivant les touches
        if self.joueurA.levier != Levier.neutre:
            return 'action'

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

    def _action(self):
        self.joueurA.attente = 1  # remise a zero de l'attente
        # *********************************************************
        # ***************** ACTIONS suivant clavier ***************
        # *********************************************************

        # droite, gauche, decapite, devant
        if self.joueurA.levier == Levier.droite:
            self.joueurA.action_droite(self.temps)
            return 'gestion'
        if self.joueurA.levier == Levier.gauche:
            self.joueurA.action_gauche(self.temps)
            return 'gestion'

        # saute, attaque cou
        if self.joueurA.levier == Levier.haut:
            self.joueurA.action_haut(self.temps)
            return 'gestion'

        # assis, attaque genou
        if self.joueurA.levier == Levier.bas:
            if self.joueurA.assis:
                self.joueurA.state = State.assis2
                return 'gestion'
            # attaque ???
            self.joueurA.occupe_state(State.assis, self.temps)
            return 'gestion'

        # roulade AV, coup de pied
        if self.sense == 'normal':
            if self.joueurA.levier == Levier.basD:
                self.joueurA.occupe_state(State.rouladeAV, self.temps)
                if self.joueurA.attaque:
                    self.joueurA.occupe_state(State.coupdepied, self.temps)
        if self.sense == 'inverse':
            if self.joueurA.levier == Levier.basG:
                self.joueurA.occupe_state(State.rouladeAV, self.temps)
                if self.joueurA.attaque:
                    self.joueurA.occupe_state(State.coupdepied, self.temps)
        # roulade AR, coup sur front
        if self.sense == 'normal':
            if self.joueurA.levier == Levier.basG:
                self.joueurA.occupe_state(State.rouladeAR, self.temps)
                if self.joueurA.attaque:
                    self.joueurA.occupe_state(State.front, self.temps)
        if self.sense == 'inverse':
            if self.joueurA.levier == Levier.basD:
                self.joueurA.occupe_state(State.rouladeAR, self.temps)
                if self.joueurA.attaque:
                    self.joueurA.occupe_state(State.front, self.temps)

        # protection haute, araignee
        if self.sense == 'normal':
            if self.joueurA.levier == Levier.hautG:
                if self.joueurA.protegeH:
                    self.joueurA.state = State.protegeH
                    return 'gestion'
                self.joueurA.occupe_state(State.protegeH1, self.temps)
                if self.joueurA.attaque and not Game.Demo:
                    self.joueurA.occupe_state(State.araignee, self.temps)
        if self.sense == 'inverse':
            if self.joueurA.levier == Levier.hautG:  # hautD ???
                if self.joueurA.protegeH:
                    self.joueurA.state = State.protegeH
                    return 'gestion'
                self.joueurA.occupe_state(State.protegeH1, self.temps)
                if self.joueurA.attaque and not Game.Demo:
                    self.joueurA.occupe_state(State.araignee, self.temps)

        # protection devant, coup de tete
        if self.sense == 'normal':
            if self.joueurA.levier == Levier.hautD:
                if self.joueurA.protegeD:
                    self.joueurA.state = State.protegeD
                    return 'gestion'
                self.joueurA.occupe_state(State.protegeD1, self.temps)
                if self.joueurA.attaque and not Game.Demo:
                    self.joueurA.occupe_state(State.coupdetete, self.temps)
        if self.sense == 'inverse':
            if self.joueurA.levier == Levier.hautD:  # hautG ???
                if self.joueurA.protegeD:
                    self.joueurA.state = State.protegeD
                    return 'gestion'
                self.joueurA.occupe_state(State.protegeD1, self.temps)
                if self.joueurA.attaque and not Game.Demo:
                    self.joueurA.occupe_state(State.coupdetete, self.temps)
        return 'gestion'

    def _gestion(self):
        # ********************************************
        # *************GESTION DES ETATS**************
        # ********************************************
        if self.joueurA.state == State.attente:
            self.joueurA.gestion_attente(self.temps)
            return 'joueur2'

        if self.joueurA.state == State.debout:
            self.joueurA.gestion_debout()
            if Game.Demo and self.joueurA.state == State.debout:
                if self.temps > self.joueurA.reftemps + 20:
                    self.joueurA.occupe = False

        if self.joueurA.state == State.avance:
            self.joueurA.reset_xX()
            self.joueurA.xAtt = self.joueurA.x_loc()
            if self.joueurA.attaque:
                self.joueurA.occupe_state(State.devant, self.temps)
                return 'gestion'
            if self.joueurA.anim != 'avance':
                self.joueurA.animate('avance')

        if self.joueurA.state == State.recule:
            self.joueurA.reset_xX()
            self.joueurA.xAtt = self.joueurA.x_loc()
            if self.joueurA.attaque:
                self.joueurA.occupe_state(State.decapite, self.temps)
                return 'gestion'
            if self.joueurA.anim != 'recule':
                self.joueurA.animate('recule')

        if self.joueurA.state == State.saute:
            rtl = self.joueurA.rtl
            self.joueurA.xAtt = self.joueurA.x_loc() + (4 if rtl else 0)
            self.joueurA.reset_xX()
            self.joueurA.decapite = False
            self.joueurA.yG = self.joueurA.yM
            self.joueurA.yAtt = 14
            if self.joueurA.attaque:
                self.joueurA.occupe_state(State.cou, self.temps)
                return 'joueur2'

            if self.temps > self.joueurA.reftemps + 45:
                self.joueurA.occupe = False
                self.joueurA.state = State.debout
                return 'joueur2'
            if self.temps > self.joueurA.reftemps + 40:
                self.joueurA.xM = self.joueurA.x_loc() + (0 if rtl else 4)
                self.joueurA.xG = self.joueurA.x_loc() + (0 if rtl else 4)
                return 'joueur2'
            if self.temps > self.joueurA.reftemps + 30:
                self.joueurA.xM = self.joueurA.x_loc() + (0 if rtl else 4)
                self.joueurA.xG = self.joueurA.x_loc() + (1 if rtl else 1)
                self.joueurA.decapite = True
                return 'joueur2'
            if self.temps > self.joueurA.reftemps + 13:
                self.joueurA.xM = self.joueurA.x_loc() + (3 if rtl else 1)
                self.joueurA.xG = self.joueurA.x_loc() + (3 if rtl else 1)
                return 'joueur2'
            if self.temps > self.joueurA.reftemps + 2:
                self.joueurA.xM = self.joueurA.x_loc() + (0 if rtl else 4)
                self.joueurA.xG = self.joueurA.x_loc() + (3 if rtl else 1)
            if self.joueurA.anim != 'saute':
                self.joueurA.animate('saute')

        if self.joueurA.state == State.assis:
            rtl = self.joueurA.rtl
            self.joueurA.xAtt = self.joueurA.x_loc() + (4 if rtl else 0)
            self.joueurA.xF = self.joueurA.x_loc() + (4 if rtl else 0)
            self.joueurA.xT = self.joueurA.x_loc() + (4 if rtl else 0)
            self.joueurA.xM = self.joueurA.x_loc() + (4 if rtl else 0)
            self.joueurA.xG = self.joueurA.x_loc() + (0 if rtl else 4)
            self.joueurA.set_anim_frame('assis', 0)
            if self.temps > self.joueurA.reftemps + 10:
                self.joueurA.state = State.assis2
                return 'joueur2'
            if self.joueurA.attaque:
                self.joueurA.occupe_state(State.genou, self.temps)

        if self.joueurA.state == State.assis2:
            self.joueurA.occupe = False
            self.joueurA.assis = True
            rtl = self.joueurA.rtl
            self.joueurA.xAtt = self.joueurA.x_loc() + (4 if rtl else 0)
            self.joueurA.xF = self.joueurA.x_loc() + (4 if rtl else 0)
            self.joueurA.xT = self.joueurA.x_loc() + (4 if rtl else 0)
            self.joueurA.xM = self.joueurA.x_loc() + (0 if rtl else 4)
            self.joueurA.xG = self.joueurA.x_loc() + (0 if rtl else 4)
            self.joueurA.set_anim_frame('assis', 1)
            if self.joueurA.attaque:
                self.joueurA.occupe_state(State.genou, self.temps)
            if Game.Demo:
                if self.temps > self.joueurA.reftemps + 20:
                    self.joueurA.occupe = False
                return 'joueur2'

        if self.joueurA.state == State.releve:
            rtl = self.joueurA.rtl
            self.joueurA.xAtt = self.joueurA.x_loc() + (4 if rtl else 0)
            self.joueurA.yAtt = 14
            self.joueurA.xF = self.joueurA.x_loc() + (4 if rtl else 0)
            self.joueurA.xT = self.joueurA.x_loc() + (4 if rtl else 0)
            self.joueurA.xM = self.joueurA.x_loc() + (0 if rtl else 4)
            self.joueurA.xG = self.joueurA.x_loc() + (0 if rtl else 4)
            self.joueurA.set_anim_frame('releve', 0)
            if self.temps > self.joueurA.reftemps + 10:
                self.joueurA.state = State.debout
                self.joueurA.occupe = False
                return 'joueur2'
            if self.joueurA.attaque:
                self.joueurA.occupe_state(State.genou, self.temps)

        if self.joueurA.state == State.rouladeAV:
            rtl = self.joueurA.rtl
            self.joueurA.xF = self.joueurA.x_loc() + (4 if rtl else 0)
            self.joueurA.xT = self.joueurA.x_loc() + (4 if rtl else 0)
            self.joueurA.xM = self.joueurA.x_loc() + (4 if rtl else 0)
            self.joueurA.xG = self.joueurA.x_loc() + (4 if rtl else 0)
            self.joueurA.yG = 20
            self.joueurA.yAtt = self.joueurA.yG
            self.joueurA.xAtt = self.joueurA.x_loc() + (4 if rtl else 0)
            self.joueurA.yT = self.joueurA.yG
            if self.joueurA.attaque:
                self.joueurA.yT = 16
                self.joueurA.occupe_state(State.coupdepied, self.temps)
                return 'gestion'
            elif self.temps > self.joueurA.reftemps + 33:
                self.joueurA.xT = self.joueurA.x_loc() + (0 if rtl else 4)
                self.joueurA.xM = self.joueurA.x_loc() + (0 if rtl else 4)
                self.joueurA.yT = 16
                self.joueurA.occupe = False
                self.joueurA.state = State.finderoulade
                # return 'finderoulade'  # vvv
            elif self.temps == self.joueurA.reftemps + 17:
                self.joueurA.xAtt = self.joueurA.x_loc() + (-1 if rtl else 5)
                return 'joueur2'
            elif self.temps == self.joueurA.reftemps + 14:
                self.joueurA.xAtt = self.joueurA.x_loc() + (-1 if rtl else 5)
                return 'joueur2'
            elif self.temps == self.joueurA.reftemps + 2:
                if self.opts.sound:
                    get_snd('roule.ogg').play()
                self.joueurA.animate('rouladeAV', 2)
                return 'joueur2'
            else:
                return 'joueur2'

        if self.joueurA.state == State.finderoulade:
            rtl = self.joueurA.rtl
            jax = self.joueurA.x_loc()
            jbx = self.joueurB.x_loc()
            if (not rtl and jax > jbx - 1) or (rtl and jax < jbx + 1):
                self.joueurA.occupe_state(State.retourne, self.temps)
                self.joueurB.occupe_state(State.retourne, self.temps)
                self.joueurA.yAtt = 14
                self.joueurB.yAtt = 14
                return 'affichage'
            if (not rtl and jax < jbx) or (rtl and jax > jbx):
                self.joueurA.state = State.debout
                self.joueurA.xAtt = self.joueurA.x_loc() + (4 if rtl else 0)
                self.joueurA.yAtt = 17
                self.joueurA.reset_xX()
                self.joueurA.yF = 15
                self.joueurA.yT = 16
                self.joueurA.yM = 18
                self.joueurA.yG = 20
                return 'joueur2'

        if self.joueurA.state == State.rouladeAR:
            rtl = self.joueurA.rtl
            self.joueurA.xF = self.joueurA.x_loc() + (4 if rtl else 0)
            self.joueurA.xT = self.joueurA.x_loc() + (4 if rtl else 0)
            self.joueurA.xM = self.joueurA.x_loc() + (4 if rtl else 0)
            self.joueurA.xG = self.joueurA.x_loc() + (4 if rtl else 0)
            self.joueurA.yG = 20
            self.joueurA.yAtt = self.joueurA.yG
            self.joueurA.xAtt = self.joueurA.x_loc() + (0 if rtl else 4)
            if self.joueurA.attaque:
                self.joueurA.occupe_state(State.front, self.temps)
                return 'gestion'
            if self.temps > self.joueurA.reftemps + 33:
                self.joueurA.xT = self.joueurA.x_loc() + (0 if rtl else 4)
                self.joueurA.xM = self.joueurA.x_loc() + (0 if rtl else 4)
                self.joueurA.occupe = False
                self.joueurA.state = State.debout
                return 'joueur2'
            elif self.temps == self.joueurA.reftemps + 2:
                if self.opts.sound:
                    get_snd('roule.ogg').play()
                self.joueurA.animate('rouladeAR', 2)
                return 'joueur2'
            else:
                return 'joueur2'

        if self.joueurA.state == State.protegeH1:
            rtl = self.joueurA.rtl
            self.joueurA.reset_xX()
            self.joueurA.xAtt = self.joueurA.x_loc() + (4 if rtl else 0)
            self.joueurA.yG = 20
            if self.joueurA.attaque:
                self.joueurA.occupe_state(State.araignee, self.temps)
                return 'gestion'
            if self.temps > self.joueurA.reftemps + 5:
                self.joueurA.protegeH = True
                self.joueurA.state = State.protegeH
                self.joueurA.occupe = False
                return 'joueur2'
            if self.temps > self.joueurA.reftemps + 2:
                return 'joueur2'
            if self.temps == self.joueurA.reftemps + 2:
                if self.opts.sound:
                    get_snd('protege.ogg').play()
                self.joueurA.animate('protegeH', 2)
                return 'joueur2'

        if self.joueurA.state == State.protegeH:
            self.joueurA.gestion_protegeH(self.temps)

        if self.joueurA.state == State.protegeD1:
            rtl = self.joueurA.rtl
            self.joueurA.xAtt = self.joueurA.x_loc() + (4 if rtl else 0)
            self.joueurA.yG = 20
            self.joueurA.reset_xX()
            self.joueurA.decapite = False
            self.joueurA.set_anim_frame('protegeD', 0)
            if self.joueurA.attaque:
                self.joueurA.occupe_state(State.coupdetete, self.temps)
                return 'gestion'
            if self.temps > self.joueurA.reftemps + 5:
                self.joueurA.state = State.protegeD
                self.joueurA.protegeD = True
                self.joueurA.occupe = False
            if self.temps > self.joueurA.reftemps + 2:
                return 'joueur2'
            if self.temps > self.joueurA.reftemps + 1:
                if self.opts.sound:
                    get_snd('protege.ogg').play()

        if self.joueurA.state == State.protegeD:
            self.joueurA.gestion_protegeD(self.temps)

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
            self.joueurA.gestion_coupdepied(self.temps)

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
            self.joueurA.gestion_vainqueur(self.temps)

        if self.joueurA.state == State.vainqueurKO:
            self.joueurA.gestion_vainqueurKO(self.temps, self.joueurB)
            if self.temps > self.joueurA.reftemps + 230:
                self.gnome = True
                self.joueurA.reftemps = self.temps
                self.xGNOME = 1
                self.xSPRt = 270
                return 'affichage'
            elif self.temps == self.joueurA.reftemps + 36:
                return 'colision'

        # ******degats******
        if self.joueurA.state == State.touche:
            rtl = self.joueurA.rtl
            self.joueurA.attente = 0
            self.joueurA.xAtt = self.joueurA.x_loc() + (4 if rtl else 0)
            self.joueurA.xF = self.joueurA.x_loc() + (4 if rtl else 0)
            self.joueurA.xT = self.joueurA.x_loc() + (4 if rtl else 0)
            self.joueurA.xM = self.joueurA.x_loc() + (4 if rtl else 0)
            self.joueurA.xG = self.joueurA.x_loc() + (4 if rtl else 0)
            self.joueurA.yF = 15
            self.joueurA.yT = 16
            self.joueurA.yM = 18
            self.joueurA.yG = 20
            if self.joueurB.state == State.coupdepied:
                self.joueurA.state = State.tombe
                return 'gestion'

            self.joueurA.sang = True
            self.serpentA.animate('bite')

            if self.joueurB.state == State.decapite and self.joueurA.decapite:
                self.joueurA.occupe_state(State.mortdecap, self.temps)
                self.xSPRt = self.joueurA.x_loc() + 3
                Game.ScoreB += 250
                self.joueurA.sang = False
                return 'mort'

            self.joueurA.vie -= 1
            if self.joueurA.vie <= 0:
                self.joueurA.occupe_state(State.mort, self.temps)
                self.joueurA.sang = True
                return 'mort'

            self.snd_play(next(self.sontouche))

            self.joueurA.occupe_state(State.touche1, self.temps)
            self.joueurA.decapite = True

        if self.joueurA.state == State.touche1:
            self.joueurA.gestion_touche1(self.temps)

        if self.joueurA.state == State.tombe:
            rtl = self.joueurA.rtl
            self.joueurA.xAttA = self.joueurA.x_loc() + (4 if rtl else 0)
            self.joueurA.attente = 0
            self.joueurA.xF = self.joueurA.x_loc() + (4 if rtl else 0)
            self.joueurA.xT = self.joueurA.x_loc() + (4 if rtl else 0)
            self.joueurA.xM = self.joueurA.x_loc() + (4 if rtl else 0)
            self.joueurA.xG = self.joueurA.x_loc() + (4 if rtl else 0)
            self.joueurA.yF = 15
            self.joueurA.yT = 16
            self.joueurA.yM = 18
            self.joueurA.yG = 20
            if self.joueurB.state != State.rouladeAV:
                self.joueurA.sang = True
                self.serpentA.animate('bite')
                self.joueurA.vie -= 1
                Game.ScoreB += 100

            if self.joueurA.vie <= 0:
                self.joueurA.occupe_state(State.mort, self.temps)
                if self.joueurB.state in (State.coupdetete, State.coupdepied):
                    self.joueurA.sang = False
                return 'mort'
            if self.joueurB.state == State.coupdetete:
                Game.ScoreB += 150
                self.joueurA.sang = False
                self.snd_play('coupdetete.ogg')
            if self.joueurB.state == State.coupdepied:
                Game.ScoreB += 150
                self.joueurA.sang = False
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

        goto = self._gestion_mort()

        return goto

    def _gestion_mort(self):
        if self.joueurA.state == State.mort:
            if self.temps > self.joueurA.reftemps + 16:
                self.joueurA.is_stopped = True
            elif self.temps > self.joueurA.reftemps + 15:
                self.joueurA.sang = False
            elif self.temps == self.joueurA.reftemps:
                self.joueurA.animate('mort')
                self.joueurB.occupe_state(State.vainqueurKO, self.temps)
                if self.lancerfin:
                    self.snd_play('mortKO.ogg')
                    self.lancerfin = False

        if self.joueurA.state == State.mortdecap:
            if self.temps == self.joueurA.reftemps:
                # noinspection PyTypeChecker
                self.change_layer(self.joueurA, 2)
                self.joueurA.animate('mortdecap')
                self.joueurB.occupe_state(State.vainqueur, self.temps)
                if self.lancerfin:
                    self.snd_play('mortdecap.ogg')
                    self.lancerfin = False

        return 'joueur2'

    def _joueur2(self):
        # debut joueur 2
        if Game.Sorcier:
            self.joueurB.sang = False
            if self.joueurA.x_loc() <= self.joueurB.x_loc() + 4:
                self.joueurB.occupe_state(State.marianna, self.temps)
                self.joueurA.occupe_state(State.fini, self.temps)
                # spriteB$ = "marianna": spriteA$ = "vainqueur3R"
                self.joueurB.x = loc2px(13)
                self.joueurA.x = loc2px(20)
                self.jeu = 'gagne'
                return None  # 'debut'
            if self.joueurB.occupe:
                return 'gestionB'
            self.joueurB.sang = False
            return 'clavierB'

        # ************degats sur joueurB************
        if self.sense == 'normal':
            if self.joueurB.x_loc() > self.joueurA.x_loc():
                if (self.joueurA.xAtt >= self.joueurB.xF
                        and self.joueurA.yAtt == self.joueurB.yF):
                    if self.joueurB.state == State.protegeH:
                        self.joueurB.state = State.clingH
                        return 'gestionB'
                    self.joueurB.state = State.tombe
                    self.joueurB.infoDegatF += 1
                    return 'gestionB'

                if (self.joueurA.xAtt >= self.joueurB.xT
                        and self.joueurA.yAtt == self.joueurB.yT):
                    if self.joueurA.state == State.coupdetete:
                        self.joueurB.state = State.tombe
                        return 'gestionB'
                    self.joueurB.state = State.touche
                    Game.ScoreA += 250
                    self.joueurB.infoDegatT += 1
                    return 'gestionB'

                if (self.joueurA.xAtt >= self.joueurB.xM
                        and self.joueurA.yAtt == self.joueurB.yM):
                    if self.joueurB.state == State.protegeD:
                        self.joueurB.state = State.clingD
                        return 'gestionB'
                    self.joueurB.state = State.touche
                    Game.ScoreA += 250
                    return 'gestionB'

                if (self.joueurA.xAtt >= self.joueurB.xG
                        and self.joueurA.yAtt == self.joueurB.yG):
                    if self.joueurA.state in (State.araignee, State.rouladeAV,
                                              State.protegeD):
                        self.joueurB.state = State.tombe
                        return 'gestionB'
                    if self.joueurA.state == State.coupdepied:
                        self.joueurB.state = State.tombe
                        self.joueurB.infoDegatG += 1
                        return 'gestionB'
                    self.joueurB.state = State.touche
                    Game.ScoreA += 100
                    self.joueurB.infoDegatG += 1
                    return 'gestionB'

        if self.sense == 'inverse':
            if self.joueurB.x_loc() < self.joueurA.x_loc():
                if (self.joueurA.xAtt <= self.joueurB.xF
                        and self.joueurA.yAtt == self.joueurB.yF):
                    if self.joueurB.state == State.protegeH:
                        self.joueurB.state = State.clingH
                        return 'gestionB'
                    self.joueurB.state = State.tombe
                    self.joueurB.infoDegatF += 1
                    return 'gestionB'

                if (self.joueurA.xAtt <= self.joueurB.xT
                        and self.joueurA.yAtt == self.joueurB.yT):
                    if self.joueurA.state == State.coupdetete:
                        self.joueurB.state = State.tombe
                        return 'gestionB'
                    self.joueurB.state = State.touche
                    Game.ScoreA += 250
                    self.joueurB.infoDegatT += 1
                    return 'gestionB'

                if (self.joueurA.xAtt <= self.joueurB.xM
                        and self.joueurA.yAtt == self.joueurB.yM):
                    if self.joueurB.state == State.protegeD:
                        self.joueurB.state = State.clingD
                        return 'gestionB'
                    self.joueurB.state = State.touche
                    Game.ScoreA += 250
                    return 'gestionB'

                if (self.joueurA.xAtt <= self.joueurB.xG
                        and self.joueurA.yAtt == self.joueurB.yG):
                    if self.joueurA.state == State.araignee:
                        self.joueurB.state = State.tombe
                        return 'gestionB'
                    if self.joueurA.state == State.rouladeAV:
                        self.joueurB.state = State.tombe
                        return 'gestionB'
                    if self.joueurB.state == State.protegeD:
                        self.joueurB.state = State.clingD
                        return 'gestionB'
                    if self.joueurA.state == State.coupdepied:
                        self.joueurB.state = State.tombe
                        self.joueurB.infoDegatG += 1
                        return 'gestionB'
                    self.joueurB.state = State.touche
                    Game.ScoreA += 100
                    self.joueurB.infoDegatG += 1
                    return 'gestionB'

        if self.joueurB.occupe:
            return 'gestionB'
        self.joueurB.sang = False
        return 'clavierB'

    def _clavierB(self):
        self.joueurB.clavierX = 7
        self.joueurB.clavierY = 7
        self.joueurB.levier = Levier.neutre
        if Game.Partie == 'vs':
            self.joueurB.clavier()
        if self.joueurB.sortie:
            if self.tempsfini:
                if self.sense == 'inverse':
                    self.joueurB.levier = Levier.gauche
                    return 'actionB'
            self.sense = 'normal'
            self.joueurB.levier = Levier.droite
            return 'actionB'
        # *****************************************
        # ******* Intelligence Artificielle *******
        # *****************************************
        if State.finderoulade in (self.joueurA.state, self.joueurB.state):
            return 'gestionB'

        if Game.Partie == 'solo':
            # ***************************IA de 1,2,3,6
            if Game.IA in (0, 1, 2, 3, 6):
                if self.sense == 'normal':
                    distance = abs(self.joueurB.x_loc() - self.joueurA.x_loc())
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
                                self.joueurB.reftempsB = self.temps
                                return 'gestionB'
                    if distance == 12 and self.joueurA.state == State.debout:
                        self.joueurB.occupe_state(State.decapite, self.temps)
                        return 'gestionB'
                    if 9 < distance < 15:  # pour se rapprocher
                        if self.joueurA.levier == Levier.gauche:
                            self.joueurB.state = State.debout
                            return 'gestionB'
                        self.joueurB.levier = Levier.gauche
                        return 'actionB'
                    if distance == 9:
                        if self.joueurA.attente > 100:
                            self.joueurB.levier = Levier.gauche
                            return 'actionB'
                        if self.joueurA.state == State.rouladeAR:
                            self.joueurB.occupe_state(State.devant, self.temps)
                            return 'gestionB'
                        if self.joueurA.occupe:
                            self.joueurB.levier = Levier.gauche
                            return 'actionB'
                    if 6 < distance < 9:  # distance de combat 1
                        # pour autoriser les croisements
                        if not Game.Demo and self.joueurA.state == State.rouladeAV:
                            self.joueurB.occupe_state(State.saute, self.temps)
                            return 'gestionB'
                        # pour se rapprocher
                        if self.joueurA.state == State.rouladeAR:
                            self.joueurB.occupe_state(State.genou, self.temps)
                            return 'gestionB'
                        if self.joueurA.levier == Levier.gauche:
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
                        if self.joueurB.infoCoup == 6:
                            self.joueurB.levier = Levier.gauche
                            self.joueurB.infoCoup = 0
                            return 'actionB'
                    if distance <= 6:
                        # pour autoriser les croisements
                        if not Game.Demo and self.joueurA.state == State.saute:
                            self.joueurB.occupe_state(State.rouladeAV, self.temps)
                            return 'gestionB'
                        if Game.IA == 3:
                            if self.joueurA.state == State.devant:
                                self.joueurB.state = State.protegeD
                                self.joueurB.reftempsB = self.temps
                                return 'gestionB'
                        if Game.IA == 2:
                            if self.joueurA.state == State.genou:
                                self.joueurB.occupe_state(State.saute, self.temps)
                                return 'gestionB'
                        if Game.IA > 1:
                            if self.joueurB.infoDegatG > 4:
                                if self.joueurA.state in (State.assis2, State.genou):
                                    self.joueurB.occupe_state(State.coupdepied, self.temps)
                                    return 'gestionB'
                                if Game.IA > 2:
                                    if self.joueurA.state == State.araignee:
                                        self.joueurB.occupe_state(State.araignee, self.temps)
                                        return 'gestionB'
                            if self.joueurB.infoDegatG > 2:
                                if self.joueurA.state == State.coupdepied:
                                    self.joueurB.occupe_state(State.rouladeAV, self.temps)
                                    return 'gestionB'
                                if self.joueurA.state in (State.assis2, State.genou):
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
                            self.joueurB.levier = Levier.gauche
                            self.joueurB.infoCoup = 0
                            return 'actionB'
                # if sens$ = 'inverse': ...
            if Game.IA in (4, 5, 7):
                if self.sense == 'normal':
                    distance = abs(self.joueurB.x_loc() - self.joueurA.x_loc())
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
                        if self.joueurA.levier == Levier.gauche:
                            self.joueurB.state = State.debout
                            return 'gestionB'
                        self.joueurB.levier = Levier.gauche
                        return 'actionB'
                    if distance == 9:
                        if self.joueurA.attente > 100:
                            self.joueurB.occupe_state(State.decapite, self.temps)
                            return 'gestionB'
                        if Game.Demo:
                            if self.joueurA.attente > 25:
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
                                self.joueurB.levier = Levier.gauche
                                return 'actionB'
                    if 6 < distance < 9:  # distance de combat 1
                        # pour autoriser les croisements
                        if not Game.Demo and self.joueurA.state == State.rouladeAV:
                            self.joueurB.occupe_state(State.saute, self.temps)
                            return 'gestionB'
                        # pour se rapprocher
                        if self.joueurA.state == State.rouladeAR:
                            self.joueurB.occupe_state(State.genou, self.temps)
                            return 'gestionB'
                        if self.joueurA.levier == Levier.gauche:
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
                            self.joueurB.levier = Levier.gauche
                            self.joueurB.infoCoup = 0
                            return 'actionB'
                    if distance <= 6:
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
                        if self.joueurB.infoCoup == 6:
                            self.joueurB.levier = Levier.gauche
                            self.joueurB.infoCoup = 0
                            return 'action'
                # if sens$ = 'inverse': ...
        # redirection suivant les touches
        if self.joueurB.levier != Levier.neutre:
            return 'actionB'
        # actions si aucune touche n'a ete touchee
        self.joueurB.spriteAvance = 0
        self.joueurB.spriteRecule = 0
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

    def _actionB(self):
        # *****************************************
        # *************actions joueur 2************
        # *****************************************
        self.joueurB.attente = 1
        if Game.Partie == 'solo':  # ****** IA mode ******
            # droite,gauche, decapite, devant (normal)  IA
            if self.sense == 'normal':
                if self.joueurB.levier == Levier.gauche:
                    self.joueurB.protegeD = False
                    if self.joueurB.state == State.avance:
                        return 'gestionB'
                    self.joueurB.state = State.avance
                    self.joueurB.reftemps = self.temps

                if self.joueurB.levier == Levier.droite:
                    self.joueurB.protegeH = False
                    if self.joueurB.state == State.recule:
                        return 'gestionB'
                    self.joueurB.state = State.recule
                    self.joueurB.reftemps = self.temps
            # droite, gauche, decapite, devant (inverse)  ******* IA mode ********
            if self.sense == 'inverse':
                if self.joueurB.levier == Levier.droite:
                    self.joueurB.protegeD = False
                    if self.joueurB.state == State.avance:
                        return 'gestionB'
                    self.joueurB.state = State.avance
                    self.joueurB.reftemps = self.temps

                if self.joueurB.levier == Levier.gauche:
                    self.joueurB.protegeH = False
                    if self.joueurB.state == State.recule:
                        return 'gestionB'
                    self.joueurB.state = State.recule
                    self.joueurB.reftemps = self.temps

            return 'gestionB'

        # droite, gauche, decapite, devant
        if self.joueurB.levier == Levier.droite:
            self.joueurB.action_droite(self.temps)
            return 'gestionB'
        if self.joueurB.levier == Levier.gauche:
            self.joueurB.action_gauche(self.temps)
            return 'gestionB'

        # saute, attaque cou
        if self.joueurB.levier == Levier.haut:
            self.joueurB.action_haut(self.temps)
            return 'gestionB'

        # assis, attaque genou
        if self.joueurB.levier == Levier.bas:
            if self.joueurB.attaque:
                self.joueurB.occupe_state(State.genou, self.temps)
                return 'gestionB'
            if self.joueurB.assis:
                self.joueurB.state = State.assis2
                return 'gestionB'
            self.joueurB.occupe_state(State.assis, self.temps)
            return 'gestionB'

        # roulade AV, coup de pied
        if self.sense == 'normal':
            if self.joueurB.levier == Levier.basG:
                self.joueurB.occupe_state(State.rouladeAV, self.temps)
                if self.joueurB.attaque:
                    self.joueurB.occupe_state(State.coupdepied, self.temps)
        if self.sense == 'inverse':
            if self.joueurB.levier == Levier.basD:
                self.joueurB.occupe_state(State.rouladeAV, self.temps)
                if self.joueurB.attaque:
                    self.joueurB.occupe_state(State.coupdepied, self.temps)

        # roulade AR, coup sur front
        if self.sense == 'normal':
            if self.joueurB.levier == Levier.basD:
                self.joueurB.occupe_state(State.rouladeAR, self.temps)
                if self.joueurB.attaque:
                    self.joueurB.occupe_state(State.front, self.temps)
        if self.sense == 'inverse':
            if self.joueurB.levier == Levier.basG:
                self.joueurB.occupe_state(State.rouladeAR, self.temps)
                if self.joueurB.attaque:
                    self.joueurB.occupe_state(State.front, self.temps)

        # protection Haute, araignee
        if self.sense == 'normal':
            if self.joueurB.levier == Levier.hautD:
                if self.joueurB.protegeH:
                    self.joueurB.state = State.protegeH
                    return 'gestionB'
                self.joueurB.occupe_state(State.protegeH1, self.temps)
                if self.joueurB.attaque:
                    self.joueurB.occupe_state(State.araignee, self.temps)

        if self.sense == 'inverse':
            if self.joueurB.levier == Levier.hautG:
                if self.joueurB.protegeH:
                    self.joueurB.state = State.protegeH
                    return 'gestionB'
                self.joueurB.occupe_state(State.protegeH1, self.temps)
                if self.joueurB.attaque:
                    self.joueurB.occupe_state(State.araignee, self.temps)

        # protection devant, coup de tete
        if self.sense == 'normal':
            if self.joueurB.levier == Levier.hautG:
                if self.joueurB.protegeD:
                    self.joueurB.state = State.protegeD
                    return 'gestionB'
                self.joueurB.occupe_state(State.protegeD1, self.temps)
                if self.joueurB.attaque:
                    self.joueurB.occupe_state(State.coupdetete, self.temps)
        if self.sense == 'inverse':
            if self.joueurB.levier == Levier.hautD:
                if self.joueurB.protegeD:
                    self.joueurB.state = State.protegeD
                    return 'gestionB'
                self.joueurB.occupe_state(State.protegeD1, self.temps)
                if self.joueurB.attaque:
                    self.joueurB.occupe_state(State.coupdetete, self.temps)
        return 'gestionB'

    def _gestionB(self):
        # ***********************************
        # *********gestion joueur 2**********
        # ***********************************
        if self.joueurB.state == State.debout:
            self.joueurB.gestion_debout()
            if Game.Partie == 'solo':
                if self.temps > self.joueurB.reftemps + 20:
                    self.joueurB.occupe = False

        if self.joueurB.state == State.attente:
            self.joueurB.gestion_attente(self.temps)
            return 'collision'

        if self.joueurB.state == State.avance:
            self.joueurB.reset_xX()
            self.joueurB.xAtt = self.joueurB.x_loc() + 4
            if self.joueurB.attaque:
                self.joueurB.occupe_state(State.devant, self.temps)
                return 'gestionB'
            if self.joueurB.anim != 'avance':
                self.joueurB.animate('avance')

        if self.joueurB.state == State.recule:
            self.joueurB.reset_xX()
            self.joueurB.xAtt = self.joueurB.x_loc() + 4
            if self.joueurB.attaque:
                self.joueurB.occupe_state(State.decapite, self.temps)
                return 'gestionB'
            if self.joueurB.anim != 'recule':
                self.joueurB.animate('recule')

        if self.joueurB.state == State.saute:
            rtl = self.joueurB.rtl
            self.joueurB.xAtt = self.joueurB.x_loc() + (4 if rtl else 0)
            self.joueurB.reset_xX()
            self.joueurB.decapite = False
            self.joueurB.yG = self.joueurB.yM
            self.joueurB.yAtt = 14
            if self.joueurB.attaque:
                self.joueurB.occupe_state(State.cou, self.temps)
                return 'colision'

            if self.temps > self.joueurB.reftemps + 45:
                self.joueurB.occupe = False
                self.joueurB.state = State.debout
                return 'colision'
            if self.temps > self.joueurB.reftemps + 40:
                self.joueurB.xM = self.joueurB.x_loc() + (0 if rtl else 4)
                self.joueurB.xG = self.joueurB.x_loc() + (0 if rtl else 4)
                return 'colision'
            if self.temps > self.joueurB.reftemps + 30:
                self.joueurB.xM = self.joueurB.x_loc() + (0 if rtl else 4)
                self.joueurB.xG = self.joueurB.x_loc() + (3 if rtl else 3)
                self.joueurB.decapite = True
                return 'colision'
            if self.temps > self.joueurB.reftemps + 13:
                self.joueurB.xM = self.joueurB.x_loc() + (3 if rtl else 1)
                self.joueurB.xG = self.joueurB.x_loc() + (3 if rtl else 1)
                return 'colision'
            if self.temps > self.joueurB.reftemps + 2:
                self.joueurB.xM = self.joueurB.x_loc() + (0 if rtl else 4)
                self.joueurB.xG = self.joueurB.x_loc() + (3 if rtl else 1)
            if self.joueurB.anim != 'saute':
                self.joueurB.animate('saute')

        if self.joueurB.state == State.assis:
            rtl = self.joueurB.rtl
            self.joueurB.xAtt = self.joueurB.x_loc() + (4 if rtl else 0)
            self.joueurB.xF = self.joueurB.x_loc() + (4 if rtl else 0)
            self.joueurB.xT = self.joueurB.x_loc() + (4 if rtl else 0)
            self.joueurB.xM = self.joueurB.x_loc() + (4 if rtl else 0)
            self.joueurB.xG = self.joueurB.x_loc() + (0 if rtl else 4)
            self.joueurB.set_anim_frame('assis', 0)
            if self.temps > self.joueurB.reftemps + 10:
                self.joueurB.state = State.assis2
                return 'colision'
            if self.joueurB.attaque:
                self.joueurB.occupe_state(State.genou, self.temps)

        if self.joueurB.state == State.assis2:
            self.joueurB.assis = True
            rtl = self.joueurB.rtl
            self.joueurB.xAtt = self.joueurB.x_loc() + (4 if rtl else 0)
            self.joueurB.xF = self.joueurB.x_loc() + (4 if rtl else 0)
            self.joueurB.xT = self.joueurB.x_loc() + (4 if rtl else 0)
            self.joueurB.xM = self.joueurB.x_loc() + (0 if rtl else 4)
            self.joueurB.xG = self.joueurB.x_loc() + (0 if rtl else 4)
            self.joueurB.set_anim_frame('assis', 1)
            if self.joueurB.attaque:
                self.joueurB.occupe_state(State.genou, self.temps)
            if Game.Partie == "solo":
                if self.temps > self.joueurB.reftemps + 20:
                    self.joueurB.occupe = False
                return 'colision'
            self.joueurB.occupe = False

        if self.joueurB.state == State.releve:
            rtl = self.joueurB.rtl
            self.joueurB.xAtt = self.joueurB.x_loc() + (4 if rtl else 0)
            self.joueurB.yAtt = 14
            self.joueurB.xF = self.joueurB.x_loc() + (4 if rtl else 0)
            self.joueurB.xT = self.joueurB.x_loc() + (4 if rtl else 0)
            self.joueurB.xM = self.joueurB.x_loc() + (0 if rtl else 4)
            self.joueurB.xG = self.joueurB.x_loc() + (0 if rtl else 4)
            self.joueurB.set_anim_frame('releve', 0)
            if self.temps > self.joueurA.reftemps + 10:
                self.joueurB.state = State.debout
                self.joueurB.occupe = False
                return 'colision'
            if self.joueurB.attaque:
                self.joueurB.occupe_state(State.genou, self.temps)

        if self.joueurB.state == State.rouladeAV:
            rtl = self.joueurB.rtl
            self.joueurB.xF = self.joueurB.x_loc() + (4 if rtl else 0)
            self.joueurB.xT = self.joueurB.x_loc() + (4 if rtl else 0)
            self.joueurB.xM = self.joueurB.x_loc() + (4 if rtl else 0)
            self.joueurB.xG = self.joueurB.x_loc() + (4 if rtl else 0)
            self.joueurB.yG = 20
            self.joueurB.yAtt = self.joueurB.yG
            self.joueurB.xAtt = self.joueurB.x_loc() + (4 if rtl else 0)
            self.joueurB.yT = self.joueurB.yG
            if self.joueurB.attaque:
                self.joueurB.yT = 16
                self.joueurB.occupe_state(State.coupdepied, self.temps)
                return 'colision'
            elif self.temps > self.joueurB.reftemps + 33:
                self.joueurB.xT = self.joueurB.x_loc() + (0 if rtl else 4)
                self.joueurB.xM = self.joueurB.x_loc() + (0 if rtl else 4)
                self.joueurB.yT = 16
                self.joueurB.occupe = False
                self.joueurB.state = State.finderoulade
                # return 'finderouladeB'  # vvv
            elif self.temps == self.joueurB.reftemps + 17:
                self.joueurB.xAtt = self.joueurB.x_loc() + (-1 if rtl else 5)
                return 'colision'
            elif self.temps == self.joueurB.reftemps + 14:
                self.joueurB.xAtt = self.joueurB.x_loc() + (-1 if rtl else 5)
                return 'colision'
            elif self.temps == self.joueurB.reftemps + 2:
                if self.opts.sound:
                    get_snd('roule.ogg').play()
                self.joueurB.animate('rouladeAV', 2)
                return 'colision'
            else:
                return 'colision'

        if self.joueurB.state == State.finderoulade:
            rtl = self.joueurB.rtl
            jax = self.joueurA.x_loc()
            jbx = self.joueurB.x_loc()
            if (not rtl and jbx > jax - 1) or (rtl and jbx < jax + 1):
                self.joueurA.occupe_state(State.retourne, self.temps)
                self.joueurB.occupe_state(State.retourne, self.temps)
                self.joueurB.yAtt = 14
                self.joueurB.yAtt = 14
                return 'affichage'
            if (not rtl and jbx < jax) or (rtl and jbx > jax):
                self.joueurB.state = State.debout
                self.joueurB.xAtt = self.joueurB.x_loc() + (4 if rtl else 0)
                self.joueurB.yAtt = 17
                self.joueurB.reset_xX()
                self.joueurB.yF = 15
                self.joueurB.yT = 16
                self.joueurB.yM = 18
                self.joueurB.yG = 20
                return 'colision'

        if self.joueurB.state == State.rouladeAR:
            rtl = self.joueurB.rtl
            self.joueurB.xF = self.joueurB.x_loc() + (4 if rtl else 0)
            self.joueurB.xT = self.joueurB.x_loc() + (4 if rtl else 0)
            self.joueurB.xM = self.joueurB.x_loc() + (4 if rtl else 0)
            self.joueurB.xG = self.joueurB.x_loc() + (4 if rtl else 0)
            self.joueurB.yG = 20
            self.joueurB.yAtt = self.joueurB.yG
            self.joueurB.xAtt = self.joueurB.x_loc() + (0 if rtl else 4)
            if self.joueurB.attaque:
                self.joueurB.occupe_state(State.front, self.temps)
                return 'gestionB'
            if self.temps > self.joueurB.reftemps + 33:
                self.joueurB.xT = self.joueurB.x_loc() + (0 if rtl else 4)
                self.joueurB.xM = self.joueurB.x_loc() + (0 if rtl else 4)
                self.joueurB.occupe = False
                self.joueurB.state = State.debout
                return 'colision'
            elif self.temps == self.joueurB.reftemps + 2:
                if self.opts.sound:
                    get_snd('roule.ogg').play()
                self.joueurB.animate('rouladeAR', 2)
                return 'colision'
            else:
                return 'colision'

        if self.joueurB.state == State.protegeH1:
            rtl = self.joueurB.rtl
            self.joueurB.reset_xX()
            self.joueurB.xAtt = self.joueurB.x_loc() + (4 if rtl else 0)
            self.joueurB.yG = 20
            if self.joueurB.attaque:
                self.joueurB.occupe_state(State.araignee, self.temps)
                return 'gestionB'
            if self.temps > self.joueurB.reftemps + 5:
                self.joueurB.protegeH = True
                self.joueurB.state = State.protegeH
                self.joueurB.occupe = False
                return 'colision'
            if self.temps > self.joueurB.reftemps + 2:
                return 'colision'
            if self.temps == self.joueurB.reftemps + 2:
                if self.opts.sound:
                    get_snd('protege.ogg').play()
                self.joueurB.animate('protegeH', 2)
                return 'colision'

        if self.joueurB.state == State.protegeH:
            self.joueurB.gestion_protegeH(self.temps)

        if self.joueurB.state == State.protegeD1:
            rtl = self.joueurB.rtl
            self.joueurB.xAtt = self.joueurB.x_loc() + (4 if rtl else 0)
            self.joueurB.yG = 20
            self.joueurB.reset_xX()
            self.joueurB.decapite = False
            self.joueurB.set_anim_frame('protegeD', 0)
            if self.joueurB.attaque:
                self.joueurB.occupe_state(State.coupdetete, self.temps)
                return 'gestionB'
            if self.temps > self.joueurB.reftemps + 5:
                self.joueurB.state = State.protegeD
                self.joueurB.protegeD = True
                self.joueurB.occupe = False
            if self.temps > self.joueurB.reftemps + 2:
                return 'colision'
            if self.temps > self.joueurB.reftemps + 1:
                if self.opts.sound:
                    get_snd('protege.ogg').play()

        if self.joueurB.state == State.protegeD:
            self.joueurB.gestion_protegeD(self.temps)

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
            self.joueurB.gestion_coupdepied(self.temps)

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
            self.joueurB.gestion_vainqueur(self.temps)

        if self.joueurB.state == State.vainqueurKO:
            self.joueurB.gestion_vainqueurKO(self.temps, self.joueurA)
            if self.temps > self.joueurB.reftemps + 230:
                self.gnome = True
                self.joueurB.reftemps = self.temps
                self.xGNOME = 1
                self.xSPRt = 270
                return 'affichage'
            elif self.temps == self.joueurA.reftemps + 36:
                return 'colision'

        # ******degats B ******
        if self.joueurB.state == State.touche:
            rtl = self.joueurB.rtl
            self.joueurB.attente = 0
            self.joueurB.xAtt = self.joueurB.x_loc() + (4 if rtl else 0)
            self.joueurB.xF = self.joueurB.x_loc() + (4 if rtl else 0)
            self.joueurB.xT = self.joueurB.x_loc() + (4 if rtl else 0)
            self.joueurB.xM = self.joueurB.x_loc() + (4 if rtl else 0)
            self.joueurB.xG = self.joueurB.x_loc() + (4 if rtl else 0)
            self.joueurB.yF = 15
            self.joueurB.yT = 16
            self.joueurB.yM = 18
            self.joueurB.yG = 20
            if self.joueurA.state == State.coupdepied:
                self.joueurB.state = State.tombe
                return 'gestionB'

            self.joueurB.sang = True
            self.serpentB.animate('bite')

            if self.joueurA.state == State.decapite and self.joueurB.decapite:
                self.joueurB.occupe_state(State.mortdecap, self.temps)
                self.xSPRt = self.joueurB.x_loc() + 3
                Game.ScoreA += 250
                self.joueurA.sang = False
                return 'mortB'

            self.joueurB.vie -= 1
            if self.joueurB.vie <= 0:
                self.joueurB.occupe_state(State.mort, self.temps)
                self.joueurB.sang = True
                return 'mortB'

            self.snd_play(next(self.sontouche))

            self.joueurB.occupe_state(State.touche1, self.temps)
            self.joueurB.decapite = True

        if self.joueurB.state == State.touche1:
            self.joueurB.gestion_touche1(self.temps)

        if self.joueurB.state == State.tombe:
            rtl = self.joueurB.rtl
            self.joueurB.xAttA = self.joueurB.x_loc() + (4 if rtl else 0)
            self.joueurB.attente = 0
            self.joueurB.xF = self.joueurB.x_loc() + (4 if rtl else 0)
            self.joueurB.xT = self.joueurB.x_loc() + (4 if rtl else 0)
            self.joueurB.xM = self.joueurB.x_loc() + (4 if rtl else 0)
            self.joueurB.xG = self.joueurB.x_loc() + (4 if rtl else 0)
            self.joueurB.yF = 15
            self.joueurB.yT = 16
            self.joueurB.yM = 18
            self.joueurB.yG = 20
            if self.joueurA.state != State.rouladeAV:
                self.joueurB.sang = True
                self.serpentB.animate('bite')
                self.joueurB.vie -= 1
                Game.ScoreA += 100

            if self.joueurB.vie <= 0:
                self.joueurB.occupe_state(State.mort, self.temps)
                if self.joueurA.state in (State.coupdetete, State.coupdepied):
                    self.joueurB.sang = False
                return 'mortB'
            if self.joueurB.state == State.coupdetete:
                Game.ScoreA += 150
                self.joueurB.sang = False
                self.snd_play('coupdetete.ogg')
            if self.joueurB.state == State.coupdepied:
                Game.ScoreA += 150
                self.joueurB.sang = False
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

        goto = self._gestion_mortB()

        return goto

    def _gestion_mortB(self):
        if self.joueurB.state == State.mort:
            self.joueurB.reset_xX()
            if self.temps == self.joueurB.reftemps + 16:
                self.joueurB.sang = False
            elif self.temps == self.joueurB.reftemps:
                self.joueurB.animate('mort')
                self.joueurA.occupe_state(State.vainqueurKO, self.temps)
                if self.lancerfin:
                    self.snd_play('mortKO.ogg')
                    self.lancerfin = False

        if self.joueurB.state == State.mortdecap:
            if self.temps == self.joueurB.reftemps:
                # noinspection PyTypeChecker
                self.change_layer(self.joueurB, 2)
                self.joueurB.animate('mortdecap')
                self.joueurA.occupe_state(State.vainqueur, self.temps)
                if self.lancerfin:
                    self.snd_play('mortdecap.ogg')
                    self.lancerfin = False

        return 'colision'

    def _colision(self):
        return 'affichage'

    def _affichage(self):
        self.vieA0.set_anim_frame('vie', max(0, 6 - self.joueurA.vie))
        self.vieA1.set_anim_frame('vie', max(0, min(6, 12 - self.joueurA.vie)))
        self.vieB0.set_anim_frame('vie_rtl', max(0, 6 - self.joueurB.vie))
        self.vieB1.set_anim_frame('vie_rtl', max(0, min(6, 12 - self.joueurB.vie)))
        return None

    def update(self, current_time, *args):
        super(Battle, self).update(current_time, *args)
        self.temps += 1
        goto = 'debut'
        while goto:
            if goto == 'debut':
                goto = self._debut()
            elif goto == 'degats':
                goto = self._degats()
            elif goto == 'clavier':
                goto = self._clavier()
            elif goto == 'action':
                goto = self._action()
            elif goto == 'gestion':
                goto = self._gestion()
            elif goto == 'mort':
                goto = self._gestion_mort()
            elif goto == 'joueur2':
                goto = self._joueur2()
            elif goto == 'clavierB':
                goto = self._clavierB()
            elif goto == 'actionB':
                goto = self._actionB()
            elif goto == 'gestionB':
                goto = self._gestionB()
            elif goto == 'mortB':
                goto = self._gestion_mortB()
            elif goto == 'colision':
                goto = self._colision()
            elif goto == 'affichage':
                goto = self._affichage()
            else:
                goto = None
        if self.opts.debug:
            self.jAstate.msg = f'AS: {self.joueurA.state}'
            self.jAlevier.msg = f'AL: {self.joueurA.levier}'
            self.jAtemps.msg = f'AT: {self.joueurA.reftemps}'
            self.jBstate.msg = f'BS: {self.joueurB.state}'
            self.jBlevier.msg = f'BL: {self.joueurB.levier}'
            self.jBtemps.msg = f'BT: {self.joueurB.reftemps}'
            self.debugTemps.msg = f'T: {self.temps}'
            if self.debugAttArea:
                self.jAAtt.move_to(loc2px(self.joueurA.xAtt), loc2px(self.joueurA.yAtt))
                self.jAF.move_to(loc2px(self.joueurA.xF), loc2px(self.joueurA.yF))
                self.jAT.move_to(loc2px(self.joueurA.xT), loc2px(self.joueurA.yT))
                self.jAM.move_to(loc2px(self.joueurA.xM), loc2px(self.joueurA.yM))
                self.jAG.move_to(loc2px(self.joueurA.xG), loc2px(self.joueurA.yG))
                self.jBAtt.move_to(loc2px(self.joueurB.xAtt), loc2px(self.joueurB.yAtt))
                self.jBF.move_to(loc2px(self.joueurB.xF), loc2px(self.joueurB.yF))
                self.jBT.move_to(loc2px(self.joueurB.xT), loc2px(self.joueurB.yT))
                self.jBM.move_to(loc2px(self.joueurB.xM), loc2px(self.joueurB.yM))
                self.jBG.move_to(loc2px(self.joueurB.xG), loc2px(self.joueurB.yG))


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
        sz = 8 * SCALE
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
        sz = 8 * SCALE
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
        sz = 8 * SCALE
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
        sz = 8 * SCALE
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
        sz = 8 * SCALE
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
