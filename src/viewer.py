#!/bin/env python3
# -*- coding: utf-8 -*-
import gc
import importlib
import sys

from pygame import key, Surface, display
from pygame.locals import *

import sprites
from main import BarbarianMain, option_parser
from scenes import EmptyScene
from settings import SCREEN_SIZE, Theme
from sprites import Barbarian, Txt, img_cache

BACKGROUND = Surface(SCREEN_SIZE)
BACKGROUND.fill(Theme.VIEWER_BACK, BACKGROUND.get_rect())
ANIM_KEYS = [
    K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9, K_0, K_q, K_w, K_e, K_r, K_t,
    K_y, K_u, K_i, K_o, K_p, K_h, K_j, K_k, K_l,
]
TXT_SPEED = '{0:0.2f}'
DIRECTIONS = {False: 'LTR', True: 'RTL'}


def txt(msg, size, *groups):
    return Txt(12, msg, Theme.VIEWER_TEXT, size, groups)


def txt_selected(msg, size, *groups):
    return Txt(12, msg, Theme.VIEWER_TEXT_SELECTED, size, groups)


class AnimationViewerScene(EmptyScene):
    def __init__(self, opts, *, on_quit):
        super(AnimationViewerScene, self).__init__(opts)
        self.on_quit = on_quit
        self.canMove = True
        self.target = self.create_barbarian(400, 200)
        self.add(self.target)
        #
        self.anims = list(self.target.anims.keys())
        self.animsTxtList = self.create_anims_txt(self.anims)
        #
        lbl = txt('Speed: ', (10, 50), self)
        self.speedTxt = txt_selected(TXT_SPEED.format(self.target.speed),
                                     (int(lbl.rect.right), int(lbl.rect.top)),
                                     self)
        lbl = txt('(S)lower / (F)aster', (10, int(lbl.rect.bottom + 5)), self)
        #
        lbl = txt('(M)ove enabled: ', (10, int(lbl.rect.bottom + 5)), self)
        self.canMoveTxt = txt(f'{self.canMove}',
                              (int(lbl.rect.right), int(lbl.rect.top)), self)
        #
        lbl = txt('(SPACE) to reload anims',
                  (10, int(lbl.rect.bottom + 5)), self)
        #
        lbl = txt('(D)irection: ', (10, int(lbl.rect.bottom + 5)), self)
        self.rtlTxt = txt_selected(DIRECTIONS[self.target.rtl],
                                   (int(lbl.rect.right), int(lbl.rect.top)),
                                   self)
        #
        txt('(<) / (>) prev/next frame (experimental)',
            (10, int(lbl.rect.bottom + 5)), self)
        #
        self.clear(None, BACKGROUND)

    def create_anims_txt(self, anims):
        txt_list = []
        ix = 0
        for anim in anims:
            key_name = key.name(ANIM_KEYS[ix])
            txt_list.append(txt(f'({key_name}): {anim}',
                                (600, ix * 12 + 10), self))
            ix += 1
        #
        cur_ix = self.anims.index(self.target.anim)
        txt_list[cur_ix].color = Theme.VIEWER_TEXT_SELECTED
        return txt_list

    def create_barbarian(self, x, y, rtl=False, anim='debout'):
        barb = Barbarian(x, y, 'spritesA', rtl, anim)
        barb.available_move = self.available_move
        return barb

    def available_move(self, dx, dy):
        if not self.canMove:
            return 0, dy
        center_x = self.target.rect.center[0]
        if center_x + dx < 60:
            return -(center_x - 60), dy
        elif center_x + dx > 740:
            return 740 - center_x, dy
        else:
            return dx, dy

    def process_event(self, evt):
        super(AnimationViewerScene, self).process_event(evt)
        if evt.type == KEYUP:
            if evt.key == K_SPACE:
                self.target.kill()

                for v in img_cache.values():
                    del v
                img_cache.clear()
                importlib.reload(sprites)

                speed = self.target.speed
                barb = self.create_barbarian(self.target.x,
                                             self.target.y,
                                             self.target.rtl,
                                             self.target.anim)
                del self.target
                gc.collect()
                self.target = barb
                self.target.speed = speed
                self.add(self.target)

            elif evt.key in ANIM_KEYS:
                ix = ANIM_KEYS.index(evt.key)
                self.select_anim(ix)

            elif evt.key == K_UP:
                ix = self.anims.index(self.target.anim) - 1
                self.select_anim(ix)

            elif evt.key == K_DOWN:
                ix = self.anims.index(self.target.anim) + 1
                self.select_anim(ix)

            elif evt.key == K_m:
                self.canMove = not self.canMove
                self.canMoveTxt.msg = self.canMove

            elif evt.key == K_s:
                self.target.speed -= 0.10
                self.speedTxt.msg = TXT_SPEED.format(self.target.speed)

            elif evt.key == K_f:
                self.target.speed += 0.10
                self.speedTxt.msg = TXT_SPEED.format(self.target.speed)

            elif evt.key == K_d:
                self.target.turn_around(not self.target.rtl)
                self.rtlTxt.msg = DIRECTIONS[self.target.rtl]

            elif evt.key == K_PERIOD:
                self.target.next_frame()

            elif evt.key == K_COMMA:
                self.target.prev_frame()

            elif evt.key == K_ESCAPE:
                self.on_quit()

    def select_anim(self, ix):
        if ix < 0:
            self.select_anim(len(self.anims) - 1)
        elif ix >= len(self.anims):
            self.select_anim(0)
        else:
            anim = self.anims[ix]
            if self.target.anim != anim:
                prev_ix = self.anims.index(self.target.anim)
                self.animsTxtList[prev_ix].color = Theme.VIEWER_TEXT
                self.target.select_anim(anim)
                self.animsTxtList[ix].color = Theme.VIEWER_TEXT_SELECTED


if __name__ == '__main__':
    (options, args) = option_parser().parse_args()
    options.sound = False
    main = BarbarianMain(options)
    main.scene = AnimationViewerScene(options, on_quit=main.quit)
    display.set_caption('Barbarian - Animation viewer')
    main.main()
    sys.exit(0)
