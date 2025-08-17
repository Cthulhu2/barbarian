#!/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
import gc
import importlib
import sys
from argparse import Action, ArgumentParser
from os import getpid
from os.path import join

import pygame as pg

import barbariantuw.core
import barbariantuw.scenes as scenes
from barbariantuw import (
    __version__, PROG, OPTS, Game, Partie, IMG_PATH, FRAME_RATE,
)
from barbariantuw.sprites import loc2pxX
from barbariantuw.core import Txt

psutil = None
if sys.platform != 'emscripten':
    try:
        psutil = importlib.import_module('psutil')
    except ImportError:
        pass


class BarbarianMain(object):
    _scene: scenes.EmptyScene = None

    def __init__(self, opts):
        pg.joystick.init()
        self.joysticks = [pg.joystick.Joystick(x)
                          for x in range(pg.joystick.get_count())]
        pg.init()
        pgdi = pg.display.Info()
        self.desktopSize = (pgdi.current_w, pgdi.current_h)
        self.screen = pg.display.set_mode(Game.screen)
        if opts.sound:
            pg.mixer.pre_init(44100, -16, 1, 4096)
        pg.display.set_caption('BARBARIAN AMIGA (PyGame)', 'BARBARIAN')
        pg.display.set_icon(pg.image.load(join(IMG_PATH, 'menu/icone.gif'))
                            .convert_alpha())
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
        if Game.fullscreen:
            self.on_fullscreen()

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
        Game.scoreA = 0
        Game.scoreB = 0
        Game.decor = 'foret'
        Game.ia = 4
        Game.partie = Partie.demo
        self.start_battle()

    def start_battle_solo(self):
        Game.scoreA = 0
        Game.scoreB = 0
        Game.decor = 'foret'
        Game.ia = 0
        Game.partie = Partie.solo
        self.start_battle()

    def start_battle_duel(self):
        Game.scoreA = 0
        Game.scoreB = 0
        Game.ia = 0
        Game.partie = Partie.vs
        self.scene = scenes.SelectStage(self.opts,
                                        on_start=self.start_battle,
                                        on_back=self.show_menu)

    def start_battle(self):
        self.scene = scenes.Battle(self.opts,
                                   on_esc=self.show_menu,
                                   on_finish=self.finish_battle,
                                   on_next=self.next_stage)

    def finish_battle(self):
        if Game.partie == Partie.solo:
            self.show_hiscores()
        else:
            self.show_menu()

    def next_stage(self):
        if Game.partie == Partie.solo:
            Game.ia += 1
            if Game.ia == 1:
                Game.decor = 'plaine'
            if Game.ia == 2:
                Game.decor = 'foret'
            if Game.ia == 3:
                Game.decor = 'plaine'
            if Game.ia == 4:
                Game.decor = 'trone'
            if Game.ia == 5:
                Game.decor = 'arene'
            if Game.ia == 6:
                Game.decor = 'trone'
            if Game.ia == 7:
                Game.decor = 'arene'

        if Game.partie == Partie.vs:
            if Game.decor == 'plaine':
                Game.decor = 'foret'
            elif Game.decor == 'foret':
                Game.decor = 'plaine'
            elif Game.decor == 'trone':
                Game.decor = 'arene'
            elif Game.decor == 'arene':
                Game.decor = 'trone'

        self.start_battle()

    def show_opts_ver(self):
        self.scene = scenes.Version(self.opts,
                                    on_display=self.show_opts_display,
                                    on_back=self.show_menu)

    def show_opts_display(self):
        Game.save_options()
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

    def show_hiscores(self):
        self.scene = scenes.HiScores(self.opts, on_finish=self.show_menu)

    # noinspection PyTypeChecker
    @staticmethod
    def reinit(size=Game.screen, scx=Game.scx, scy=Game.scy):
        barbariantuw.core.img_cache.clear()
        Txt.cache.clear()
        gc.collect()
        #
        Game.screen = size
        Game.scx = scx
        Game.scy = scy
        Game.chw = int(320 / 40 * scx)
        Game.chh = int(200 / 25 * scy)

    def toggle_fullscreen(self, fullscreen):
        # TODO: Toggle fullscreen with multi-display
        if fullscreen and not self.opts.web and not pg.display.is_fullscreen():
            scx = self.desktopSize[0] / 320
            scy = self.desktopSize[1] / 200
            self.reinit(self.desktopSize, scx, scy)
            pg.display.set_mode(self.desktopSize)
            pg.display.toggle_fullscreen()
        if not fullscreen and not self.opts.web and pg.display.is_fullscreen():
            self.reinit()
            pg.display.toggle_fullscreen()
            pg.display.set_mode(Game.screen)

    def on_fullscreen(self):
        Game.fullscreen = True
        self.toggle_fullscreen(Game.fullscreen)
        Game.save_options()
        self.show_logo()

    def on_window(self):
        Game.fullscreen = False
        self.toggle_fullscreen(Game.fullscreen)
        Game.save_options()
        self.show_logo()

    async def main(self):
        cpu_timer = 0
        mem_timer = 0
        if not self.opts.web and psutil:
            pid = getpid()
            # noinspection PyUnresolvedReferences
            pu = psutil.Process(pid)
        slowmo = False

        clock = pg.time.Clock()

        while self.running:
            for evt in pg.event.get():
                if evt.type == pg.QUIT:
                    if not self.opts.web:
                        self.quit()

                elif evt.type == pg.JOYDEVICEREMOVED:
                    if joy := next(filter(
                            lambda j: j.get_instance_id() == evt.instance_id,
                            self.joysticks), None):
                        joy.quit()
                        self.joysticks.remove(joy)

                elif evt.type == pg.JOYDEVICEADDED:
                    self.joysticks.append(pg.joystick.Joystick(evt.device_index))
                    self.joysticks[-1].init()

                if self.opts.debug:
                    if evt.type == pg.KEYDOWN and evt.key == pg.K_BACKQUOTE:
                        slowmo = True
                        self.lblSlowmo.msg = 'SlowMo'
                    if evt.type == pg.KEYUP and evt.key == pg.K_BACKQUOTE:
                        slowmo = False
                        self.lblSlowmo.msg = ''
                self.scene.process_event(evt)

            current_time = pg.time.get_ticks()
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
            pg.display.update(dirty)
            if self.opts.web:
                await asyncio.sleep(0)
            elif slowmo:
                clock.tick(4)
            else:
                clock.tick(FRAME_RATE)

        if self.opts.sound:
            pg.mixer.stop()
            pg.mixer.quit()


class BooleanAction(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, not option_string.startswith('--no'))


def arg_parser():
    parser = ArgumentParser(prog=PROG)
    parser.add_argument('-v', '--version', action='version',
                        version=f'{PROG} {__version__}')

    parser.add_argument(
        '--no-sound', '--sound',
        dest='sound', default=True, nargs=0, action=BooleanAction,
        help='turn sound on/off (default on)')

    parser.add_argument(
        '--no-usa', '--usa',
        dest='usa', nargs=0, action=BooleanAction,
        help='USA version (default options.dat or Europe)')

    parser.add_argument(
        '--no-fullscreen', '--fullscreen',
        dest='fullscreen', nargs=0, action=BooleanAction,
        help='no/fullscreen (default options.dat or window)')

    debug = parser.add_argument_group('Debug Options', description='')

    debug.add_argument(
        '-d', '--debug',
        action='count', dest='debug', default=0,
        help='show debug info (CPU, VMS, RSS, FPS), psutil module required')
    debug.add_argument(
        '-c', '--cpu-time',
        action='store', dest='cpu_time', type=int, default=500,
        help='CPU usage refresh time (ms). Default: 500 ms')
    debug.add_argument(
        '-m', '--mem-time',
        action='store', dest='mem_time', type=int, default=500,
        help='memory usage refresh time (ms). Default: 500 ms')

    return parser


def run():
    args = arg_parser().parse_args()
    args.web = (sys.platform == 'emscripten')
    for k, v in args.__dict__.items():
        OPTS.__setattr__(k, v)
    Game.load_options()
    if args.usa is not None:
        Game.country = 'USA' if args.usa else 'EUROPE'
    if args.fullscreen is not None:
        Game.fullscreen = args.fullscreen
    asyncio.run(BarbarianMain(args).main())


if __name__ == '__main__':
    run()
