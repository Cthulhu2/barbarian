# -*- coding: utf-8 -*-
import importlib

from pygame import key, Surface
from pygame.locals import *

from .common import EmptyScene
from config import DARK_GRAY, GREEN, WHITE, SCREEN_SIZE, FONT
from sprite.common import img_cache, Txt
import sprite.barbarian


BACKGROUND = Surface(SCREEN_SIZE)
BACKGROUND.fill(DARK_GRAY, BACKGROUND.get_rect())
ANIM_KEYS = [
    K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9, K_0, K_q, K_w, K_e, K_r, K_t,
    K_y, K_u, K_i, K_o, K_p, K_h, K_j, K_k, K_l,
]
TXT_SPEED = '{0:0.2f}'
DIRECTIONS = {False: 'LTR', True: 'RTL'}


class AnimationViewerScene(EmptyScene):
    def __init__(self, screen):
        super(AnimationViewerScene, self).__init__(screen, BACKGROUND)
        self.canMove = True
        self.target = self.create_barbarian()
        self.add(self.target, *self.target.stuff)
        #
        self.anims = list(sorted(self.target.anims.keys()))
        self.animsTxtList = self.create_anims_txt(self.anims)
        #
        lbl = Txt(FONT, 8, 'Speed: ', WHITE, 10, 10, self)
        self.speedTxt = Txt(FONT, 8, TXT_SPEED.format(self.target.speed),
                            GREEN, lbl.rect.right, 10, self)
        Txt(FONT, 8, '(S)lower / (F)aster', WHITE, 10, 23, self)
        #
        lbl = Txt(FONT, 8, '(M)ove enabled: ', WHITE, 10, 40, self)
        self.canMoveTxt = Txt(FONT, 8, self.canMove,
                              GREEN, lbl.rect.right, 40, self)
        #
        Txt(FONT, 8, '(SPACE) to reload anims', WHITE, 10, 57, self)
        #
        lbl = Txt(FONT, 8, '(D)irection: ', WHITE, 10, 74, self)
        self.rtlTxt = Txt(FONT, 8, DIRECTIONS[self.target.rtl],
                          GREEN, lbl.rect.right, 74, self)
        #
        Txt(FONT, 8, '(<) / (>) prev/next frame (experimental)',
            WHITE, 10, 91, self)

    def create_anims_txt(self, anims):
        txt_list = []
        ix = 0
        for anim in anims:
            key_name = key.name(ANIM_KEYS[ix])
            txt_list.append(
                Txt(FONT, 8, '({0}): {1}'.format(key_name, anim),
                    WHITE, 600, ix * 8 + 10, self))
            ix += 1
        #
        cur_ix = self.anims.index(self.target.anim)
        txt_list[cur_ix].color = GREEN
        return txt_list

    def create_barbarian(self, rtl=False, anim='idle'):
        barb = sprite.barbarian.Barbarian(400, 400, rtl, anim)
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

                for k_ in filter(lambda k: str(k).startswith('barbarian'),
                                 img_cache.keys()):
                    del img_cache[k_]
                importlib.reload(sprite.barbarian)

                speed = self.target.speed
                self.target = self.create_barbarian(self.target.rtl,
                                                    self.target.anim)
                self.target.speed = speed
                self.add(self.target, self.target.stuff)

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
                for s in self.target.stuff:
                    s.next_frame()

            elif evt.key == K_COMMA:
                self.target.prev_frame()
                for s in self.target.stuff:
                    s.prev_frame()

    def select_anim(self, ix):
        if ix < 0:
            self.select_anim(len(self.anims) - 1)
        elif ix >= len(self.anims):
            self.select_anim(0)
        else:
            anim = self.anims[ix]
            if self.target.anim != anim:
                prev_ix = self.anims.index(self.target.anim)
                self.animsTxtList[prev_ix].color = WHITE
                self.target.select_anim(anim)
                self.animsTxtList[ix].color = GREEN
