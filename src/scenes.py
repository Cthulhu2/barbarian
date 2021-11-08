# -*- coding: utf-8 -*-
from pygame import Surface
from pygame.locals import *
from pygame.sprite import LayeredDirty
from pygame.time import get_ticks

from settings import Theme, SCREEN_SIZE, SCALE
from sprites import (
    get_img, get_snd, Txt, AnimatedSprite, StaticSprite, Barbarian,
    serpent_anims, rtl_anims, loc_to_pix, loc, State, Levier, Sorcier
)


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
        self.set_timing_treshold(1000.0 / 25.0)
        back = Surface(SCREEN_SIZE)
        back.fill(Theme.BACK, back.get_rect())
        # noinspection PyTypeChecker
        self.clear(None, back)
        self.timer = get_ticks()
        self.opts = opts

        if self.opts.debug:
            self.cpu = Txt(8, 'CPU: ', Theme.DEBUG, (0, 0))
            # 'Resident Set Size', this is the non-swapped
            #   physical memory a process has used.
            self.mem_rss = Txt(8, 'Mem RSS: ', Theme.DEBUG,
                               (0, self.cpu.rect.bottom))
            # 'Virtual Memory Size', this is the total amount of
            #   virtual memory used by the process.
            self.mem_vms = Txt(8, 'Mem VMS: ', Theme.DEBUG,
                               (0, self.mem_rss.rect.bottom))
            self.fps = Txt(8, 'FPS: ', Theme.DEBUG,
                           (0, self.mem_vms.rect.bottom))
            self.add(self.cpu, self.mem_rss, self.mem_vms, self.fps, layer=99)

    def process_event(self, evt):
        pass


class Logo(EmptyScene):
    def __init__(self, opts, *, on_load):
        super(Logo, self).__init__(opts)
        self.usaLogo = False
        self.titre = False
        self.load = False
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

        get_img('sprites/feu1.gif', color=(255, 0, 255))
        get_img('sprites/feu2.gif', color=(255, 0, 255))
        get_img('sprites/feu3.gif', color=(255, 0, 255))

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
            elif 4000 < passed < 8000:
                self.show_titre()
                self.do_load()
            else:
                self.on_load()
        else:
            if passed < 4000:
                self.show_titre()
                self.do_load()
            else:
                self.on_load()


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
        self.add(
            StaticSprite((0, 104 * SCALE),
                         f'stage/{Game.Decor}ARBREG.gif'),
            StaticSprite((272 * SCALE, 104 * SCALE),
                         f'stage/{Game.Decor}ARBRED.gif'),
            layer=2)

        self.joueurA = Barbarian(loc_to_pix(1), loc_to_pix(15),
                                 'spritesA',
                                 rtl=Game.Rtl)
        self.joueurB = Barbarian(loc_to_pix(36), loc_to_pix(15),
                                 f'spritesB/spritesB{Game.IA}',
                                 rtl=not Game.Rtl)
        sz = 8 * SCALE
        if Game.Partie == 'solo' and not Game.Demo:
            self.add(Txt(sz, 'ONE  PLAYER', Theme.TXT, loc(16, 25)))
        elif Game.Partie == 'vs':
            self.add(Txt(sz, 'TWO PLAYER', Theme.TXT, loc(16, 25)))
        elif Game.Demo:
            self.add(Txt(sz, 'DEMONSTRATION', Theme.TXT, loc(14, 25)))

        self.txtScoreA = Txt(sz, f'{Game.ScoreA:05}', Theme.TXT, loc(13, 8))
        self.txtScoreB = Txt(sz, f'{Game.ScoreB:05}', Theme.TXT, loc(24, 8))
        self.add(self.txtScoreA, self.txtScoreB)

        if Game.Partie == 'vs':
            self.txtChronometre = Txt(sz, f'{Game.Chronometre:02}',
                                      Theme.TXT, loc(19, 8))
            self.add(self.txtChronometre)

        elif Game.Partie == 'solo':
            self.add(Txt(sz, f'{Game.IA:02}', Theme.TXT, loc(20, 8)))
        self.add(self.joueurA, self.joueurB)
        self.joueurA.select_anim('avance')
        self.joueurB.select_anim('avance')
        self.serpentA = AnimatedSprite((11 * SCALE, 22 * SCALE),
                                       serpent_anims())
        self.serpentB = AnimatedSprite((275 * SCALE, 22 * SCALE),
                                       rtl_anims(serpent_anims()))
        self.add(self.serpentA, self.serpentB)
        self.entree = True
        self.entreesorcier = False
        self.lancerintro = True
        self.temps = 0
        self.tempsfini = False
        self.sense = 'normal'  # inverse

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

        if Game.Demo:
            return

        # TODO: Joystick events
        if evt.type == KEYDOWN:
            # Joueur A
            if evt.key == K_UP:
                self.joueurA.inc_clavier_y()
            elif evt.key == K_DOWN:
                self.joueurA.dec_clavier_y()
            elif evt.key == K_LEFT:
                self.joueurA.dec_clavier_x()
            elif evt.key == K_RIGHT:
                self.joueurA.inc_clavier_x()
            elif evt.key == K_RSHIFT:
                self.joueurA.attaque = True
            # Joueur B
            elif evt.key == K_i:
                self.joueurB.inc_clavier_y()
            elif evt.key == K_j:
                self.joueurB.dec_clavier_y()
            elif evt.key == K_k:
                self.joueurB.dec_clavier_x()
            elif evt.key == K_l:
                self.joueurB.inc_clavier_x()
            elif evt.key == K_SPACE:
                self.joueurB.attaque = True

        if evt.type == KEYUP:
            # Joueur A
            if evt.key == K_RSHIFT:
                self.joueurA.attaque = False
            # Joueur B
            elif evt.key == K_SPACE:
                self.joueurB.attaque = False

    def update(self, current_time, *args):
        super(Battle, self).update(current_time, *args)
        passed = current_time - self.timer
        if passed < 50:
            return
        self.timer = current_time

        # debout:
        self.temps += 1
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
                self.serpentA.select_anim('bite')
                self.serpentB.select_anim('bite')
            if jax >= 13:
                self.joueurA.x = loc_to_pix(13)
            if jbx <= 22:
                self.joueurB.x = loc_to_pix(22)
            if jax >= 13 or jbx <= 22:
                self.joueurA.set_anim_frame('debout', 0)
                self.joueurB.set_anim_frame('debout', 0)
                self.entree = False
            return

        if self.joueurA.sortie:
            if not self.tempsfini:
                if jax < 2 and jbx >= 37:
                    if Game.Partie == 'solo':
                        if Game.Demo:
                            self.finish()
                            return
                        if Game.IA < 7:
                            self.next_stage()
                        else:
                            Game.Sorcier = True
                            self.sense = 'inverse'
                            self.joueurB = Sorcier(loc_to_pix(8),
                                                   loc_to_pix(15))
                            self.add(self.joueurB)
                            self.joueurA.state = State.debout
                            self.joueurA.x = loc_to_pix(36)
                            self.entree = False
                            self.joueurA.sortie = False
                            self.entreesorcier = True
                            self.joueurB.occupe = True
                            self.joueurB.reftemps = self.temps
                    return
            elif ((self.sense == 'normal' and jax < 2 and jbx >= 37)
                  or (self.sense == 'inverse' and jbx < 2 and jax >= 37)):
                Game.Chronometre = 60
                self.next_stage()
                return

        # degats:
        # degats sur joueurA
        if Game.Sorcier:
            if self.joueurA.x_loc() < 29:
                if self.joueurB.xT < self.joueurB.xAtt <= self.joueurB.xT + 2:
                    if self.joueurB.yAtt == self.joueurA.yT:
                        self.gnome = False
                        if self.jeu == 'perdu':
                            pass
                            # GOTO gestion
                        self.joueurA.state = State.mortSORCIER
                        self.joueurA.occupe = True
                        self.joueurB.reftemps = self.temps
                        self.joueurA.sang = False
                        self.joueurB.state = State.sorcierFINI
                        self.joueurB.occupe = True
                        self.joueurB.reftemps = self.temps
                        self.joueurB.sang = False
                        self.jeu = 'perdu'
                        # GOTO gestion
                if self.joueurA.xG <= self.joueurB.xAtt <= self.joueurA.xG + 2:
                    if self.joueurB.yAtt == self.joueurA.yG:
                        self.gnome = False
                        if self.jeu == 'perdu':
                            pass
                            # GOTO gestion
                        self.joueurA.state = State.mortSORCIER
                        self.joueurA.occupe = True
                        self.joueurA.reftemps = self.temps
                        self.joueurA.sang = False
                        self.joueurB.state = State.sorcierFINI
                        self.joueurB.occupe = True
                        self.joueurB.reftemps = self.temps
                        self.joueurB.sang = False
                        self.jeu = 'perdu'
                        # GOTO gestion
            if self.joueurA.occupe:
                pass
                # GOTO gestion
            self.joueurA.sang = False
        # GOTO clavier


        # clavier:
        self.joueurA.clavier()
        self.joueurB.clavier()

        # gestion:

        if Game.Demo:
            distance = jbx - jax
            if distance >= 15:  # quand trop loin
                self.joueurA.select_anim('roulade')
                self.joueurA.occupe = True
            if distance == 12 and self.joueurB.anim == 'debout':
                self.joueurA.select_anim('decapite')
                self.joueurA.occupe = True

            if distance == 9:
                if self.joueurB.attente > 100:
                    self.joueurA.state = State.decapite
                    self.joueurA.occupe = True
                if self.joueurB.state == State.roulade:
                    self.joueurA.state = State.genou
                    self.joueurA.occupe = True
                if self.joueurB.occupe:
                    self.joueurA.state = State.roulade
                    self.joueurA.occupe = True

            if 6 < distance < 9:
                # distance de combat 1
                # pour se rapprocher
                if self.joueurB.state == 'roulade':
                    self.joueurA.state = 'genou'
                    self.joueurA.occupe = True
                if self.joueurB.levier == Levier.gauche:
                    self.joueurA.state = 'araignee'
                    self.joueurA.occupe = True
                if self.joueurB.state == 'front':
                    self.joueurA.state = 'protegeH'
                # pour eviter les degats repetitifs
                if self.joueurA.infoDegatG > 4:
                    if self.joueurB.state in ('assis2', 'genou'):
                        self.joueurA.state = 'genou'
                        self.joueurA.occupe = True
                    if self.joueurA.infoDegatG > 2:
                        if self.joueurB.state in ('assis2', 'genou'):
                            self.joueurA.state = 'rouladeAV'
                            self.reftemps = self.temps
                            self.joueurA.occupe = True
                    if self.joueurA.infoDegatT > 2:
                        if self.joueurB.state == 'cou':
                            self.joueurA.state = 'genou'
                            self.reftemps = self.temps
                            self.joueurA.occupe = True

    #                 IF infoAdegatF > 2 THEN
    #                     IF joueurB$ = "front" THEN joueurA$ = "rouladeAV": reftemps = temps: Aoccupe$ = "oui": GOTO gestion
    #                 END IF
    #
    #                 'pour alterner les attaques
    #
    #                 IF infocoupA = 0 THEN joueurA$ = "devant": infocoupA = infocoupA + 1: reftemps = temps: Aoccupe$ = "oui": GOTO gestion
    #                 IF infocoupA = 1 THEN joueurA$ = "front": infocoupA = infocoupA + 1: reftemps = temps: Aoccupe$ = "oui": GOTO gestion
    #                 IF infocoupA = 2 THEN joueurA$ = "araignee": infocoupA = infocoupA + 1: reftemps = temps: Aoccupe$ = "oui": GOTO gestion
    #                 IF infocoupA = 3 THEN joueurA$ = "araignee": infocoupA = infocoupA + 1: reftemps = temps: Aoccupe$ = "oui": GOTO gestion
    #                 IF infocoupA = 4 THEN joueurA$ = "cou": infocoupA = infocoupA + 1: reftemps = temps: Aoccupe$ = "oui": GOTO gestion
    #                 IF infocoupA = 5 THEN levier1$ = "gauche": infocoupA = 0: GOTO action
    #
    #
    #             END IF
    #             IF distance <= 6 THEN
    #
    #                 IF joueurB$ = "devant" THEN joueurA$ = "protegeD": reftemps = temps: GOTO gestion
    #
    #                 IF infoAdegatG > 4 THEN
    #                     IF joueurB$ = "assis2" OR joueurB$ = "genou" THEN joueurA$ = "genou": reftemps = temps: Aoccupe$ = "oui": GOTO gestion
    #                 END IF
    #                 IF infoAdegatG > 2 THEN
    #                     IF joueurB$ = "coupdepied" THEN joueurA$ = "rouladeAV": reftemps = temps: Aoccupe$ = "oui": GOTO gestion
    #                     IF joueurB$ = "assis2" OR joueurB$ = "genou" THEN joueurA$ = "rouladeAV": reftemps = temps: Aoccupe$ = "oui": GOTO gestion
    #                 END IF
    #
    #                 IF infocoupA = 0 THEN joueurA$ = "coupdepied": infocoupA = infocoupA + 1: reftemps = temps: Aoccupe$ = "oui": GOTO gestion
    #                 IF infocoupA = 1 THEN joueurA$ = "coupdetete": infocoupA = infocoupA + 1: reftemps = temps: Aoccupe$ = "oui": GOTO gestion
    #                 IF infocoupA = 2 THEN joueurA$ = "araignee": infocoupA = infocoupA + 1: reftemps = temps: Aoccupe$ = "oui": GOTO gestion
    #                 IF infocoupA = 3 THEN joueurA$ = "genou": infocoupA = infocoupA + 1: reftemps = temps: Aoccupe$ = "oui": GOTO gestion
    #                 IF infocoupA = 4 THEN joueurA$ = "genou": infocoupA = infocoupA + 1: reftemps = temps: Aoccupe$ = "oui": GOTO gestion
    #                 IF infocoupA = 5 THEN levier1$ = "gauche": infocoupA = 0: GOTO action
    #
    #
    #             END IF


class Version(_MenuBackScene):
    def __init__(self, opts, *, on_display):
        super(Version, self).__init__(opts, 'menu/version.png')
        self.on_display = on_display

    def process_event(self, evt):
        if evt.type != KEYUP:
            return
        elif evt.key == K_1:
            Game.Country = 'europe'
            self.on_display()
        elif evt.key == K_2:
            Game.Country = 'USA'
            self.on_display()


class Display(_MenuBackScene):
    def __init__(self, opts, *, on_fullscreen, on_window):
        super(Display, self).__init__(opts, 'menu/display.png')
        self.on_fullscreen = on_fullscreen
        self.on_window = on_window

    def process_event(self, evt):
        if evt.type != KEYUP:
            return
        elif evt.key == K_1:
            self.on_fullscreen()
        elif evt.key == K_2:
            self.on_window()


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
        self.add(StaticSprite((0, 0), 'menu/playerA.png',
                              color=(255, 255, 255)))
        self.add(StaticSprite((280 * SCALE, 0), 'menu/playerB.png',
                              color=(255, 255, 255)))

        sz = 8 * SCALE
        self.add(
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
        )

    def process_event(self, evt):
        if evt.type != KEYUP:
            return
        elif evt.key in (K_KP_ENTER, K_RETURN, K_ESCAPE, K_SPACE):
            self.on_next()


class ControlsMoves(EmptyScene):
    def __init__(self, opts, *, on_next):
        super(ControlsMoves, self).__init__(opts)
        self.on_next = on_next
        self.add(StaticSprite((100 * SCALE, 40 * SCALE), 'menu/controls1.gif'))

        sz = 8 * SCALE
        self.add(
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
        )

    def process_event(self, evt):
        if evt.type != KEYUP:
            return
        elif evt.key in (K_KP_ENTER, K_RETURN, K_ESCAPE, K_SPACE):
            self.on_next()


class ControlsFight(EmptyScene):
    def __init__(self, opts, *, on_next):
        super(ControlsFight, self).__init__(opts)
        self.on_next = on_next
        self.add(StaticSprite((100 * SCALE, 40 * SCALE), 'menu/controls2.gif'))

        sz = 8 * SCALE
        self.add(
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
        )

    def process_event(self, evt):
        if evt.type != KEYUP:
            return
        elif evt.key in (K_KP_ENTER, K_RETURN, K_ESCAPE, K_SPACE):
            self.on_next()


class Credits(EmptyScene):
    def __init__(self, opts, *, on_back):
        super(Credits, self).__init__(opts)
        self.on_back = on_back
        self.add(StaticSprite((0, 0), 'menu/team.png'))

        sz = 8 * SCALE
        col = Theme.OPTS_TXT
        self.add(
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
        )

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
        self.add(
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
        )

    def process_event(self, evt):
        if evt.type != KEYUP:
            return
        elif evt.key in (K_KP_ENTER, K_RETURN, K_ESCAPE, K_SPACE):
            self.on_back()
