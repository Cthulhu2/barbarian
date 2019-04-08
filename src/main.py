# -*- coding: utf-8 -*-
from optparse import OptionParser, OptionGroup
from os import getpid

from psutil import Process
from pygame import display, event, mixer, init, time

from config import SCREEN_SIZE, FONT, RED


class BarbarianMain(object):
    def __init__(self):
        self.screen = display.set_mode(SCREEN_SIZE)
        mixer.pre_init(44100, -16, 1, 4096)
        init()

    def main(self, opts):
        if not opts.sound:
            mixer.quit()
        cpu_timer = 0
        mem_timer = 0
        pid = getpid()
        pu = Process(pid)

        # import after init, to load images
        #   pygame.error: cannot convert without pygame.display initialized
        from sprite.common import Txt
        if opts.viewer:
            from scene.viewer import AnimationViewerScene
            scene = AnimationViewerScene(self.screen)
            display.set_caption('Barbarian - Animation viewer')
        else:
            from scene.battle import BattleScene
            scene = BattleScene(self.screen)
            display.set_caption('Barbarian')
        clock = time.Clock()

        cpu = Txt(FONT, 8, 'CPU: ', RED, 0, 566)
        # 'Resident Set Size', this is the non-swapped
        #   physical memory a process has used.
        mem_rss = Txt(FONT, 8, 'Mem RSS: ', RED, 0, cpu.rect.bottom)
        # 'Virtual Memory Size', this is the total amount of
        #   virtual memory used by the process.
        mem_vms = Txt(FONT, 8, 'Mem VMS: ', RED, 0, mem_rss.rect.bottom)
        fps = Txt(FONT, 8, 'FPS: ', RED, 0, mem_vms.rect.bottom)
        if opts.debug:
            scene.add(cpu, mem_rss, mem_vms, fps)

        while True:
            for evt in event.get():
                scene.process_event(evt)

            # Update all the sprites
            current_time = time.get_ticks()
            if opts.debug:
                fps.msg = 'FPS: {0:.0f}'.format(clock.get_fps())

                if current_time - cpu_timer > opts.cpu_time:
                    cpu_timer = current_time
                    cpu.msg = 'CPU: {0:.1f}%'.format(pu.cpu_percent())

                if current_time - mem_timer > opts.mem_time:
                    mem_timer = current_time
                    mem = pu.memory_info()
                    resident = 'Mem RSS: {0:>7,.0f} Kb'.format(mem.rss / 1024)
                    mem_rss.msg = resident.replace(',', ' ')
                    virtual = 'Mem VMS: {0:>7,.0f} Kb'.format(mem.vms / 1024)
                    mem_vms.msg = virtual.replace(',', ' ')
            scene.update(current_time)

            # Draw the scene
            dirty = scene.draw(self.screen)
            display.update(dirty)
            clock.tick(60)


def option_parser():
    parser = OptionParser(usage='usage: %prog [options]',
                          version='%prog 0.1')

    parser.add_option('-v', '--viewer',
                      action='store_true',
                      dest='viewer',
                      default=False,
                      help='launch animation Viewer scene')
    parser.add_option('-s', '--sound',
                      action='store_true',
                      dest='sound',
                      default=False,
                      help='turn sound on. Default: false (off)')

    debug = OptionGroup(parser, 'Debug Options', description='')

    debug.add_option('-d', '--debug',
                     action='store_true',
                     dest='debug',
                     default=False,
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

    BarbarianMain().main(options)
