#!/bin/env python3
# -*- coding: utf-8 -*-

# TODO: Define version in single place
# See also pyproject.toml version.

# nuitka-project: --product-name=barbariantuw
# nuitka-project: --product-version=0.1.0
# nuitka-project: --file-description="'Barbarian - The Ultimate Warrior' game clone"
# nuitka-project: --onefile
# nuitka-project: --onefile-tempdir-spec="{CACHE_DIR}/{PRODUCT}/{VERSION}"
# nuitka-project: --include-data-dir=barbariantuw/fnt=barbariantuw/fnt
# nuitka-project: --include-data-dir=barbariantuw/img=barbariantuw/img
# nuitka-project: --include-data-dir=barbariantuw/snd=barbariantuw/snd

import asyncio
import gc
import importlib
import sys
from optparse import OptionParser, OptionGroup
from os import getpid
from os.path import join

import pygame
from pygame import display, event, mixer, init, time, image

import barbariantuw.ai as ai
import barbariantuw.anims as anims
import barbariantuw.scenes as scenes
import barbariantuw.settings as settings
import barbariantuw.sprites as sprites
from barbariantuw import OPTS, Game, Partie
from barbariantuw.settings import SCREEN_SIZE, IMG_PATH, FRAME_RATE
from barbariantuw.sprites import Txt, loc2pxX

psutil = None
if sys.platform != 'emscripten':
    try:
        psutil = importlib.import_module('psutil')
    except ImportError:
        pass


class BarbarianMain(object):
    _scene: scenes.EmptyScene = None

    def __init__(self, opts):
        init()
        pgdi = display.Info()
        self.desktopSize = (pgdi.current_w, pgdi.current_h)
        self.screen = display.set_mode(SCREEN_SIZE)
        if opts.sound:
            mixer.pre_init(44100, -16, 1, 4096)
        display.set_caption('BARBARIAN AMIGA (PyGame)', 'BARBARIAN')
        icon = image.load(join(IMG_PATH, 'menu/icone.gif')).convert_alpha()
        display.set_icon(icon)
        self.opts = opts
        self.running = True
        #
        self.debugGrp = []
        if self.opts.debug:
            self.cpu = Txt.Debug(0, 0)
            # 'Resident Set Size', this is the non-swapped
            #   physical memory a process has used.
            self.mem_rss = Txt.Debug(0, self.cpu.rect.bottom)
            # 'Virtual Memory Size', this is the total amount of
            #   virtual memory used by the process.
            self.mem_vms = Txt.Debug(0, self.mem_rss.rect.bottom)
            self.fps = Txt.Debug(0, self.mem_vms.rect.bottom)
            self.lblSlowmo = Txt.Debug(loc2pxX(18), 10)
        self.show_logo()

    @property
    def scene(self) -> scenes.EmptyScene:
        return self._scene

    @scene.setter
    def scene(self, scene: scenes.EmptyScene):
        if self._scene:
            for s in self._scene.sprites():
                s.kill()
                del s
            del self._scene
        #
        self._scene = scene
        if self.opts.debug:
            # noinspection PyTypeChecker
            self.scene.add(self.cpu, self.mem_rss, self.mem_vms, self.fps,
                           self.lblSlowmo,
                           layer=99)
        gc.collect()

    def menu(self):
        return scenes.Menu(self.opts,
                           on_demo=self.start_battle_demo,
                           on_solo=self.start_battle_solo,
                           on_duel=self.start_battle_duel,
                           on_options=self.show_opts_ver,
                           on_controls=self.show_ctrl_keys,
                           on_history=self.show_history,
                           on_credits=self.show_credits,
                           on_quit=self.quit)

    def quit(self):
        if not self.opts.web:
            self.running = False

    def show_logo(self):
        self.scene = scenes.Logo(self.opts, on_load=self.show_menu)

    def show_menu(self):
        self.scene = self.menu()

    def start_battle_demo(self):
        Game.ScoreA = 0
        Game.ScoreB = 0
        Game.Decor = 'foret'
        Game.IA = 4
        Game.Partie = Partie.demo
        self.start_battle()

    def start_battle_solo(self):
        Game.ScoreA = 0
        Game.ScoreB = 0
        Game.Decor = 'foret'
        Game.IA = 0
        Game.Partie = Partie.solo
        self.start_battle()

    def start_battle_duel(self):
        Game.ScoreA = 0
        Game.ScoreB = 0
        Game.IA = 0
        Game.Partie = Partie.vs
        self.scene = scenes.SelectStage(self.opts,
                                        on_start=self.start_battle,
                                        on_back=self.show_menu)

    def start_battle(self):
        self.scene = scenes.Battle(self.opts,
                                   on_esc=self.cancel_battle,
                                   on_menu=self.show_menu,
                                   on_next=self.next_stage)

    def cancel_battle(self):
        self.show_menu()

    def next_stage(self):
        if Game.Partie == Partie.solo:
            Game.IA += 1
            if Game.IA == 1:
                Game.Decor = 'plaine'
            if Game.IA == 2:
                Game.Decor = 'foret'
            if Game.IA == 3:
                Game.Decor = 'plaine'
            if Game.IA == 4:
                Game.Decor = 'trone'
            if Game.IA == 5:
                Game.Decor = 'arene'
            if Game.IA == 6:
                Game.Decor = 'trone'
            if Game.IA == 7:
                Game.Decor = 'arene'

        if Game.Partie == Partie.vs:
            if Game.Decor == 'plaine':
                Game.Decor = 'foret'
            elif Game.Decor == 'foret':
                Game.Decor = 'plaine'
            elif Game.Decor == 'trone':
                Game.Decor = 'arene'
            elif Game.Decor == 'arene':
                Game.Decor = 'trone'

        self.start_battle()

    def show_opts_ver(self):
        self.scene = scenes.Version(self.opts,
                                    on_display=self.show_opts_display,
                                    on_back=self.show_menu)

    def show_opts_display(self):
        self.scene = scenes.Display(self.opts,
                                    on_fullscreen=self.on_fullscreen,
                                    on_window=self.on_window,
                                    on_back=self.show_opts_ver)

    def show_ctrl_keys(self):
        self.scene = scenes.ControlsKeys(self.opts,
                                         on_next=self.show_ctrl_moves)

    def show_ctrl_moves(self):
        self.scene = scenes.ControlsMoves(self.opts,
                                          on_next=self.show_ctrl_fight)

    def show_ctrl_fight(self):
        self.scene = scenes.ControlsFight(self.opts, on_next=self.show_menu)

    def show_credits(self):
        self.scene = scenes.Credits(self.opts, on_back=self.show_menu)

    def show_history(self):
        self.scene = scenes.History(self.opts, on_back=self.show_menu)

    # noinspection PyTypeChecker
    @staticmethod
    def reinit(size=settings.SCREEN_SIZE, scx=settings.SCALE_X, scy=settings.SCALE_Y):
        anims.img_cache.clear()
        Txt.cache.clear()
        gc.collect(generation=0)
        #
        settings.SCREEN_SIZE = size
        settings.SCALE_X = scx
        settings.SCALE_Y = scy
        settings.CHAR_W = int(320 / 40 * scx)
        settings.CHAR_H = int(200 / 25 * scy)
        #
        importlib.reload(anims)
        importlib.reload(sprites)
        importlib.reload(ai)
        importlib.reload(scenes)

    def on_fullscreen(self):
        # TODO: Toggle fullscreen with multi-display
        if not self.opts.web and not pygame.display.is_fullscreen():
            scx = self.desktopSize[0] / 320
            scy = self.desktopSize[1] / 200
            self.reinit(self.desktopSize, scx, scy)
            pygame.display.set_mode(self.desktopSize)
            pygame.display.toggle_fullscreen()
        self.show_logo()

    def on_window(self):
        if not self.opts.web and pygame.display.is_fullscreen():
            self.reinit()
            pygame.display.toggle_fullscreen()
            pygame.display.set_mode(SCREEN_SIZE)
        self.show_logo()

    async def main(self):
        cpu_timer = 0
        mem_timer = 0
        if not self.opts.web and psutil:
            pid = getpid()
            # noinspection PyUnresolvedReferences
            pu = psutil.Process(pid)
        slowmo = False

        clock = time.Clock()

        while self.running:
            for evt in event.get():
                if evt.type == pygame.QUIT:
                    if not self.opts.web:
                        self.quit()
                if self.opts.debug:
                    if evt.type == pygame.KEYDOWN and evt.key == pygame.K_BACKSPACE:
                        slowmo = True
                        self.lblSlowmo.msg = 'SlowMo'
                    if evt.type == pygame.KEYUP and evt.key == pygame.K_BACKSPACE:
                        slowmo = False
                        self.lblSlowmo.msg = ''
                self.scene.process_event(evt)

            current_time = time.get_ticks()
            if not self.opts.web and self.opts.debug:
                self.fps.msg = f'FPS: {clock.get_fps():.0f}'
                if psutil:
                    if current_time - cpu_timer > self.opts.cpu_time:
                        cpu_timer = current_time
                        # noinspection PyUnboundLocalVariable
                        self.cpu.msg = f'CPU: {pu.cpu_percent():.1f}%'

                    if current_time - mem_timer > self.opts.mem_time:
                        mem_timer = current_time
                        mem = pu.memory_info()
                        resident = f'Mem RSS: {mem.rss / 1024:>7,.0f} Kb'
                        self.mem_rss.msg = resident.replace(',', ' ')
                        virtual = f'Mem VMS: {mem.vms / 1024:>7,.0f} Kb'
                        self.mem_vms.msg = virtual.replace(',', ' ')
            self._scene.update(current_time)

            dirty = self._scene.draw(self.screen)
            display.update(dirty)
            if self.opts.web:
                await asyncio.sleep(0)
            elif slowmo:
                clock.tick(4)
            else:
                clock.tick(FRAME_RATE)

        if self.opts.sound:
            pygame.mixer.stop()
            pygame.mixer.quit()


def option_parser():
    parser = OptionParser(usage='usage: %prog [options]',
                          version='%prog 0.1')

    parser.add_option('--no-sound',
                      action='store_false',
                      dest='sound',
                      default=True,
                      help='turn sound off')

    debug = OptionGroup(parser, 'Debug Options', description='')

    debug.add_option('-d', '--debug',
                     action='count',
                     dest='debug',
                     default=0,
                     help='show debug info (CPU, VMS, RSS, FPS),'
                          ' psutil module required')
    debug.add_option('-c', '--cpu-time',
                     action='store',
                     dest='cpu_time',
                     type='int',
                     default=500,
                     help='CPU usage refresh time (ms). Default: 500 ms')
    debug.add_option('-m', '--mem-time',
                     action='store',
                     dest='mem_time',
                     type='int',
                     default=500,
                     help='memory usage refresh time (ms). Default: 500 ms')

    parser.add_option_group(debug)
    return parser


def run():
    (options, args) = option_parser().parse_args()
    options.web = (sys.platform == 'emscripten')
    for k, v in options.__dict__.items():
        OPTS.ensure_value(k, v)
    asyncio.run(BarbarianMain(options).main())


if __name__ == '__main__':
    run()
