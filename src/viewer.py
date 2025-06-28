#!/bin/env python3
# -*- coding: utf-8 -*-
import gc
import importlib
import sys
from typing import Any, Tuple

from pygame import key, Surface, display
from pygame.locals import *
from pygame.sprite import DirtySprite, AbstractGroup, Group
from pygame.transform import scale

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
TOGGLE = {False: 'OFF', True: 'ON'}


def txt(msg, size, *groups):
    return Txt(12, msg, Theme.VIEWER_TXT, size, groups)


def txt_selected(msg, size, *groups):
    return Txt(12, msg, Theme.VIEWER_TXT_SELECTED, size, groups)


class Rectangle(Group):
    def __init__(self,
                 x, y, w, h,
                 color: Tuple[int, int, int],
                 *groups: AbstractGroup):
        super().__init__(*groups)
        self.border_width = 1
        self.img = Surface((self.border_width, self.border_width))
        self.img.fill(color, self.img.get_rect())
        self.left = DirtySprite(self)
        self.left.image = self.img
        self.left.rect = Rect(x, y, self.border_width, h)
        self.left.visible = True
        #
        self.right = DirtySprite(self)
        self.right.image = self.img
        self.right.rect = Rect(x + w - self.border_width, y,
                               self.border_width, h)
        #
        self.top = DirtySprite(self)
        self.top.image = self.img
        self.top.rect = Rect(x, y, w, self.border_width)
        #
        self.bottom = DirtySprite(self)
        self.bottom.image = self.img
        self.bottom.rect = Rect(x, y + h - self.border_width,
                                w, self.border_width)

    def apply(self, r: Rect):
        if self.left.rect.topleft != r.topleft or self.left.rect.h != r.h:
            self.left.rect.topleft = (r.x, r.y)
            if self.left.rect.h != r.h:
                self.left.rect.h = r.h
                self.left.image = scale(self.img, self.left.rect.size)
            self.left.dirty = 1

        x = r.x + r.w - self.border_width
        if self.right.rect.topleft != (x, r.y) or self.right.rect.h != r.h:
            self.right.rect.topleft = (x, r.y)
            if self.right.rect.h != r.h:
                self.right.rect.h = r.h
                self.right.image = scale(self.img, self.right.rect.size)
            self.right.dirty = 1

        if self.top.rect.topleft != (r.x, r.y) or self.top.rect.w != r.w:
            self.top.rect.topleft = (r.x, r.y)
            if self.top.rect.w != r.w:
                self.top.rect.w = r.w
                self.top.image = scale(self.img, self.top.rect.size)
            self.top.dirty = 1

        y = r.y + r.h - self.border_width
        if self.bottom.rect.topleft != (r.x, y) or self.bottom.rect.w != r.w:
            self.bottom.rect.topleft = (r.x, y)
            if self.bottom.rect.w != r.w:
                self.bottom.rect.w = r.w
                self.bottom.image = scale(self.img, self.bottom.rect.size)
            self.bottom.dirty = 1


class AnimationViewerScene(EmptyScene):
    def __init__(self, opts, screen: Surface, *, on_quit):
        super(AnimationViewerScene, self).__init__(opts)
        self.screen = screen
        self.on_quit = on_quit
        self.canMove = True
        self.border = False
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
        lbl = txt('(<) / (>) prev/next frame (experimental)',
                  (10, int(lbl.rect.bottom + 5)), self)
        #
        lbl = txt('(B)order: ', (10, int(lbl.rect.bottom + 5)), self)
        self.borderTxt = txt_selected(f'{TOGGLE[self.border]}',
                                      (int(lbl.rect.right), int(lbl.rect.top)),
                                      self)
        self.borderGroup = Rectangle(0, 0, 200, 200, Theme.VIEWER_BORDER)
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
        txt_list[cur_ix].color = Theme.VIEWER_TXT_SELECTED
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
        super().update(*args, **kwargs)
        if self.border:
            self.borderGroup.apply(self.target.rect)


if __name__ == '__main__':
    (options, args) = option_parser().parse_args()
    options.sound = False
    main = BarbarianMain(options)
    main.scene = AnimationViewerScene(options, main.screen, on_quit=main.quit)
    display.set_caption('Barbarian - Animation viewer')
    main.main()
    sys.exit(0)
