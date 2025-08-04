#!/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
import gc
import importlib
from typing import Any

from pygame import key, Surface, display
from pygame.locals import *

import barbariantuw.anims as anims
from barbariantuw import Game, Theme, OPTS
from barbariantuw.__main__ import BarbarianMain, arg_parser
from barbariantuw.core import Rectangle, Txt, img_cache
from barbariantuw.scenes import EmptyScene
from barbariantuw.sprites import Barbarian

BACKGROUND = Surface(Game.screen)
BACKGROUND.fill(Theme.VIEWER_BACK, BACKGROUND.get_rect())
ANIM_KEYS = [
    K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9, K_0,
    K_q, K_w, K_e, K_r, K_t, K_y, K_u, K_i, K_o, K_p,
    K_LEFTBRACKET, K_RIGHTBRACKET,
    K_g, K_h, K_j, K_k, K_l, K_SEMICOLON, K_QUOTE,
]
TXT_SPEED = '{0:0.2f}'
DIRECTIONS = {False: 'LTR', True: 'RTL'}
TOGGLE = {False: 'OFF', True: 'ON'}


def txt(msg, size, *groups):
    return Txt(12, msg, Theme.VIEWER_TXT, size, groups)


def txt_selected(msg, size, *groups):
    return Txt(12, msg, Theme.VIEWER_TXT_SELECTED, size, groups)


class AnimationViewerScene(EmptyScene):
    def __init__(self, opts, screen: Surface, *, on_quit):
        super(AnimationViewerScene, self).__init__(opts)
        self.screen = screen
        self.on_quit = on_quit
        self.canMove = True
        self.border = False
        self.target = self.create_barbarian(400, 300)
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
        self.canMoveTxt = txt_selected(f'{self.canMove}',
                                       (int(lbl.rect.right), int(lbl.rect.top)),
                                       self)
        #
        lbl = txt('(SPACE) to reload anims',
                  (10, int(lbl.rect.bottom + 5)), self)
        #
        lbl = txt('(D)irection: ', (10, int(lbl.rect.bottom + 5)), self)
        self.rtlTxt = txt_selected(DIRECTIONS[self.target.rtl],
                                   (int(lbl.rect.right), int(lbl.rect.top)),
                                   self)
        #
        lbl = txt('(<) / (>) prev/next frame (experimental)',
                  (10, int(lbl.rect.bottom + 5)), self)
        #
        lbl = txt('(B)order: ', (10, int(lbl.rect.bottom + 5)), self)
        self.borderTxt = txt_selected(f'{TOGGLE[self.border]}',
                                      (int(lbl.rect.right), int(lbl.rect.top)),
                                      self)
        self.borderGroup = Rectangle(0, 0, 200, 200, Theme.VIEWER_BORDER)
        lbl = txt('Frame: ', (10, lbl.rect.bottom + 5), self)
        self.frameTxt = txt_selected(
            f'{self.target.frameNum + 1} / {len(self.target.frames)}'
            f' ({self.target.frame.name})',
            (int(lbl.rect.right), int(lbl.rect.top)),
            self)
        self.clear(None, BACKGROUND)

    def create_anims_txt(self, anims):
        txt_list = []
        ix = 0
        for anim in anims:
            key_name = key.name(ANIM_KEYS[ix])
            txt_list.append(txt(f'({key_name}): {anim}',
                                (700, ix * 12 + 10), self))
            ix += 1
        #
        cur_ix = self.anims.index(self.target.anim)
        txt_list[cur_ix].color = Theme.VIEWER_TXT_SELECTED
        return txt_list

    def create_barbarian(self, x, y, rtl=False, anim='debout') -> Barbarian:
        return Barbarian(self.opts, x, y, 'spritesA', rtl, anim)

    def process_event(self, evt):
        super(AnimationViewerScene, self).process_event(evt)
        if evt.type == KEYUP:
            if evt.key == K_SPACE:
                self.target.kill()

                for v in img_cache.values():
                    del v
                img_cache.clear()
                importlib.reload(anims)

                speed = self.target.speed
                barb = self.create_barbarian(self.target.x,
                                             self.target.y,
                                             self.target.rtl,
                                             self.target.anim)
                barb.frameNum = self.target.frameNum - 1
                barb.frame_tick = self.target.frame_tick
                barb.frame_duration = self.target.frame_duration
                barb.frame = barb.frames[barb.frameNum]
                barb.next_frame()
                self.target.kill()
                del self.target
                gc.collect()
                self.target = barb
                self.target.speed = speed
                self.add(self.target)

            elif evt.key in ANIM_KEYS:
                ix = ANIM_KEYS.index(evt.key)
                self.animate(ix)

            elif evt.key == K_UP:
                ix = self.anims.index(self.target.anim) - 1
                self.animate(ix)

            elif evt.key == K_DOWN:
                ix = self.anims.index(self.target.anim) + 1
                self.animate(ix)

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

            elif evt.key == K_b:
                self.border = not self.border
                self.borderTxt.msg = f'{TOGGLE[self.border]}'
                if self.border:
                    self.add(self.borderGroup, layer=99)
                else:
                    self.remove(self.borderGroup)

            elif evt.key == K_ESCAPE:
                self.on_quit()

    def animate(self, ix: int):
        if ix < 0:
            self.animate(len(self.anims) - 1)
        elif ix >= len(self.anims):
            self.animate(0)
        else:
            anim = self.anims[ix]
            if self.target.anim != anim:
                prev_ix = self.anims.index(self.target.anim)
                self.animsTxtList[prev_ix].color = Theme.VIEWER_TXT
                self.target.animate(anim)
                self.animsTxtList[ix].color = Theme.VIEWER_TXT_SELECTED

    def update(self, *args: Any, **kwargs: Any) -> None:
        prev = self.target.rect.left
        super().update(*args, **kwargs)
        if not self.canMove and self.target.frame.mv and prev != self.target.rect.left:
            self.target.move(-self.target.frame.mv[0], 0)
        elif self.target.rect.left < 0:
            self.target.move(-self.target.rect.left, 0)
        elif self.target.rect.right > Game.screen[0]:
            self.target.move(Game.screen[0] - self.target.rect.right, 0)

        self.frameTxt.msg = (
            f'{self.target.frameNum + 1} / {len(self.target.frames)}'
            f' ({self.target.frame.name})'
        )
        if self.border:
            self.borderGroup.apply(self.target.rect)


if __name__ == '__main__':
    args = arg_parser().parse_args()
    args.sound = False
    args.web = False
    args.debug = 3
    for k, v in args.__dict__.items():
        OPTS.__setattr__(k, v)
    main = BarbarianMain(args)
    main.scene = AnimationViewerScene(args, main.screen, on_quit=main.quit)
    display.set_caption('Barbarian - Animation viewer')
    asyncio.run(main.main())
