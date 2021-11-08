# -*- coding: utf-8 -*-
import gc
import sys
from optparse import OptionParser, OptionGroup
from os import getpid
from os.path import join

import pygame
from psutil import Process
from pygame import display, event, mixer, init, time, image

import scenes
from settings import SCREEN_SIZE, IMG_PATH


class BarbarianMain(object):
    def __init__(self, opts):
        self.screen = display.set_mode(SCREEN_SIZE)
        if opts.sound:
            mixer.pre_init(44100, -16, 1, 4096)
        init()
        display.set_caption('BARBARIAN AMIGA (PyGame)', 'BARBARIAN')
        icon = image.load(join(IMG_PATH, 'menu/icone.gif')).convert_alpha()
        display.set_icon(icon)
        self.opts = opts
        self.scene = scenes.Logo(opts, on_load=self.show_menu)
        self.running = True
        self.scoreA = 0
        self.scoreB = 0

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
        self.running = False

    def show_menu(self):
        self.scene = self.menu()
        gc.collect()

    def start_battle_demo(self):
        scenes.Game.Decor = 'foret'
        scenes.Game.Demo = True
        scenes.Game.IA = 4
        scenes.Game.Partie = "solo"
        scenes.Game.Sorcier = False
        self.start_battle()

    def start_battle_solo(self):
        scenes.Game.Decor = 'foret'
        scenes.Game.Demo = False
        scenes.Game.IA = 0
        scenes.Game.Partie = "solo"
        scenes.Game.Sorcier = False
        self.start_battle()

    def start_battle_duel(self):
        scenes.Game.Demo = False
        scenes.Game.IA = 0
        scenes.Game.Partie = "vs"
        scenes.Game.Chronometre = 60
        scenes.Game.Sorcier = False
        self.scene = scenes.SelectStage(self.opts,
                                        on_start=self.start_battle,
                                        on_back=self.show_menu)
        gc.collect()

    def start_battle(self):
        self.scene = scenes.Battle(self.opts,
                                   on_esc=self.cancel_battle,
                                   on_menu=self.show_menu,
                                   on_fin=self.finish_battle)
        gc.collect()

    def cancel_battle(self):
        self.scoreA = 0
        self.scoreB = 0
        self.show_menu()

    def finish_battle(self):
        if scenes.Game.Partie == 'solo':
            if scenes.Game.Demo:
                self.show_menu()
                return
        if scenes.Game.Partie == 'vs':
            scenes.Game.Chronometre = 60
            if scenes.Game.Decor == 'plaine':
                scenes.Game.Decor = 'foret'
            elif scenes.Game.Decor == 'foret':
                scenes.Game.Decor = 'plaine'
            elif scenes.Game.Decor == 'trone':
                scenes.Game.Decor = 'arene'
            elif scenes.Game.Decor == 'arene':
                scenes.Game.Decor = 'trone'
            self.start_battle()

    def show_opts_ver(self):
        self.scene = scenes.Version(self.opts,
                                    on_display=self.show_opts_display)
        gc.collect()

    def show_opts_display(self):
        self.scene = scenes.Display(self.opts,
                                    on_fullscreen=self.on_fullscreen,
                                    on_window=self.on_window)
        gc.collect()

    def show_ctrl_keys(self):
        self.scene = scenes.ControlsKeys(self.opts,
                                         on_next=self.show_ctrl_moves)
        gc.collect()

    def show_ctrl_moves(self):
        self.scene = scenes.ControlsMoves(self.opts,
                                          on_next=self.show_ctrl_fight)
        gc.collect()

    def show_ctrl_fight(self):
        self.scene = scenes.ControlsFight(self.opts, on_next=self.show_menu)
        gc.collect()

    def show_credits(self):
        self.scene = scenes.Credits(self.opts, on_back=self.show_menu)
        gc.collect()

    def show_history(self):
        self.scene = scenes.History(self.opts, on_back=self.show_menu)
        gc.collect()

    def on_fullscreen(self):
        # TODO: Toggle fullscreen with multi-display
        self.scene = self.menu()
        gc.collect()

    def on_window(self):
        # TODO: Toggle fullscreen with multi-display
        self.scene = self.menu()
        gc.collect()

    def main(self):
        cpu_timer = 0
        mem_timer = 0
        pid = getpid()
        pu = Process(pid)

        clock = time.Clock()

        while self.running:
            for evt in event.get():
                if evt.type == pygame.QUIT:
                    self.quit()
                self.scene.process_event(evt)

            current_time = time.get_ticks()
            if self.opts.debug:
                self.scene.fps.msg = f'FPS: {clock.get_fps():.0f}'

                if current_time - cpu_timer > self.opts.cpu_time:
                    cpu_timer = current_time
                    self.scene.cpu.msg = f'CPU: {pu.cpu_percent():.1f}%'

                if current_time - mem_timer > self.opts.mem_time:
                    mem_timer = current_time
                    mem = pu.memory_info()
                    resident = f'Mem RSS: {mem.rss / 1024:>7,.0f} Kb'
                    self.scene.mem_rss.msg = resident.replace(',', ' ')
                    virtual = f'Mem VMS: {mem.vms / 1024:>7,.0f} Kb'
                    self.scene.mem_vms.msg = virtual.replace(',', ' ')
            self.scene.update(current_time)

            dirty = self.scene.draw(self.screen)
            display.update(dirty)
            clock.tick(60)

        if self.opts.sound:
            pygame.mixer.stop()
            pygame.mixer.quit()
        pygame.quit()


def option_parser():
    parser = OptionParser(usage='usage: %prog [options]',
                          version='%prog 0.1')

    parser.add_option('-s', '--sound',
                      action='store_true',
                      dest='sound',
                      default=True,
                      help='turn sound on. Default: false (off)')

    debug = OptionGroup(parser, 'Debug Options', description='')

    debug.add_option('-d', '--debug',
                     action='store_true',
                     dest='debug',
                     default=True,
                     help='show debug info (CPU, VMS, RSS, FPS)')
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


if __name__ == '__main__':
    (options, args) = option_parser().parse_args()

    BarbarianMain(options).main()
    sys.exit(0)
