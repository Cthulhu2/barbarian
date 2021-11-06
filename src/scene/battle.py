# -*- coding: utf-8 -*-
from typing import Optional

from pygame import Surface
from pygame.locals import *

from .common import EmptyScene
from config import SCREEN_SIZE, BLACK
from sprite.barbarian import Barbarian, Hit

BACKGROUND = Surface(SCREEN_SIZE)
BACKGROUND.fill(BLACK, BACKGROUND.get_rect())

INPUT = ['L', 'R', 'D', 'U', 'F']
KEYS_PLAYER1 = [K_6, K_7, K_8, K_9, K_0]
KEYS_PLAYER2 = [K_1, K_2, K_3, K_4, K_5]

DIST = 60


class BarbarianFighter(Barbarian):
    def __init__(self, x, y, rtl):
        super(BarbarianFighter, self).__init__(x, y, rtl)
        self.opponent = None  # type: Optional[BarbarianFighter]
        self.input = {inp: False for inp in INPUT}
        self.on_hit = None
        self.on_decapitate = None

    def is_pressed(self, *inp):
        return all(self.input[i] for i in inp)

    def available_move(self, dx, dy):
        if self.anim == 'roll_forward' and self.opponent.anim == 'jump':
            # No turn_around near a border by double distance.
            dist = DIST * 2
            if dist <= self.x + dx <= SCREEN_SIZE[0] - dist:
                return dx, dy
            elif dx < 0:
                # Left border
                return -(self.x - dist), dy
            else:
                # Right border
                return SCREEN_SIZE[0] - dist - self.x, dy

        elif DIST <= self.x + dx <= SCREEN_SIZE[0] - DIST:
            if self.anim == 'turn_around':
                return dx, dy
            #
            op_dist = self.opp_distance()
            if self.rtl and dx < 0 and op_dist + dx < DIST:
                # Opponent on left
                return -(op_dist - DIST), dy
            elif not self.rtl and dx > 0 and op_dist - dx < DIST:
                # Opponent on right
                return op_dist - DIST, dy
            else:
                # Path is clear
                return dx, dy
        elif dx < 0:
            # Left border
            return -(self.x - DIST), dy
        else:
            # Right border
            return SCREEN_SIZE[0] - DIST - self.x, dy

    def select_anim(self, anim):
        if self.anim != anim:
            super(BarbarianFighter, self).select_anim(anim)

    def opp_distance(self):
        return abs(self.x - self.opponent.x)

    def update(self, current_time, *args):
        super(BarbarianFighter, self).update(current_time, *args)
        if self.anim in ('roll_forward', 'roll_backward', 'helicopter', 'fall',
                         'hurt', 'decapitate', 'jump', 'turn_around'):
            return  # Unstoppable

        # get forward/backward-input based on rightToLeft
        fwd, bwd = ('L', 'R') if self.rtl else ('R', 'L')

        if self.is_pressed(bwd, 'D', 'F'):
            self.select_anim('overcut')

        elif self.is_pressed(fwd, 'D', 'F'):
            self.select_anim('kick')

        elif self.is_pressed(bwd, 'U', 'F'):
            self.select_anim('windmill')

        elif self.is_pressed(fwd, 'U', 'F'):
            self.select_anim('headbutt')

        elif self.is_pressed(bwd, 'D'):
            self.select_anim('roll_backward')

        elif self.is_pressed(fwd, 'D'):
            self.select_anim('roll_forward')

        elif self.is_pressed(bwd, 'U'):
            self.select_anim('high_defense')

        elif self.is_pressed(fwd, 'U'):
            self.select_anim('mid_defense')

        elif self.is_pressed(bwd, 'F'):
            self.select_anim('helicopter')

        elif self.is_pressed(fwd, 'F'):
            self.select_anim('mid_crosscut')

        elif self.is_pressed('U', 'F'):
            self.select_anim('high_crosscut')

        elif self.is_pressed('D', 'F'):
            self.select_anim('low_crosscut')

        elif self.input[bwd]:
            self.select_anim('move_backward')

        elif self.input[fwd]:
            self.select_anim('move_forward')

        elif self.input['U']:
            self.select_anim('jump')

        elif self.input['D']:
            self.select_anim('duck')

        else:
            self.select_anim('idle')

    def on_pre_action(self, anim, action):
        if action == 'check_hit':
            if self.opp_distance() > DIST * 2:
                return

            if anim == 'helicopter' and self.opponent.anim in (
                    'idle', 'high_defense',
                    'move_forward', 'move_backward'):
                self.opponent.select_anim('decapitate')
                self.opponent.on_decapitate(self.opponent, self)
            elif self.opponent.anim != 'duck':
                if self.on_hit:
                    self.on_hit(self.opponent.x, self.opponent.y)
                self.opponent.select_anim('hurt')

    def on_post_action(self, anim, action):
        super(BarbarianFighter, self).on_post_action(anim, action)
        if action == 'end':
            if anim in ('jump', 'roll_forward'):
                if (not self.rtl and self.opponent.x < self.x
                        or self.rtl and self.opponent.x > self.x):
                    self.select_anim('turn_around')
                else:
                    self.select_anim('idle')

            elif anim == 'turn_around':
                self.turn_around(not self.rtl)
                self.select_anim('idle')

            elif anim in ('fall', 'hurt', 'helicopter', 'roll_backward'):
                self.select_anim('idle')

            elif anim in ('high_defense', 'mid_defense', 'duck', 'decapitate'):
                self.is_stopped = True

        elif action == 'push' and anim == 'roll_forward':
            if (self.opp_distance() <= DIST
                    and self.opponent.anim not in ('roll_forward', 'jump')):
                self.opponent.select_anim('fall')


class BarbarianFighterAI(BarbarianFighter):
    def __init__(self, x, y, rtl):
        super(BarbarianFighterAI, self).__init__(x, y, rtl)

    def press(self, *inp):
        for i in ('L', 'R', 'D', 'U', 'F'):
            self.input[i] = i in inp

    def update(self, current_time, *args):
        super(BarbarianFighterAI, self).update(current_time, *args)
        if self.opponent.anim == 'idle':
            if DIST * 2 < self.opp_distance():
                self.press('L')
            elif self.opp_distance() <= DIST * 2:
                self.press('R', 'F')
            else:
                self.press()
        else:
            self.press()


class BattleScene(EmptyScene):
    def __init__(self, screen):
        super(BattleScene, self).__init__(screen, BACKGROUND)
        self.player1 = BarbarianFighter(200, 400, False)
        self.player2 = BarbarianFighterAI(600, 400, True)
        self.player1.opponent = self.player2
        self.player1.on_hit = self.on_hit
        self.player1.on_decapitate = self.on_decapitate
        self.player2.opponent = self.player1
        self.player2.on_hit = self.on_hit
        self.player2.on_decapitate = self.on_decapitate
        self.add(self.player1, self.player1.stuff,
                 self.player2, self.player2.stuff)

    def process_event(self, evt):
        super(BattleScene, self).process_event(evt)

        if evt.type == KEYDOWN:
            if evt.key in KEYS_PLAYER1:
                self.player1.input[INPUT[KEYS_PLAYER1.index(evt.key)]] = True

            if evt.key in KEYS_PLAYER2:
                self.player2.input[INPUT[KEYS_PLAYER2.index(evt.key)]] = True

        elif evt.type == KEYUP:
            if evt.key in KEYS_PLAYER1:
                self.player1.input[INPUT[KEYS_PLAYER1.index(evt.key)]] = False

            if evt.key in KEYS_PLAYER2:
                self.player2.input[INPUT[KEYS_PLAYER2.index(evt.key)]] = False

    def update(self, current_time, *args):
        super(BattleScene, self).update(current_time, *args)

    def on_hit(self, x, y):
        self.add(Hit(x, y), layer=255)

    def on_decapitate(self,
                      decapitated: BarbarianFighter,
                      slayer: BarbarianFighter):
        self.change_layer(decapitated, 1)
        for s in decapitated.stuff:
            self.change_layer(s, 1)

        self.change_layer(slayer, 0)
        for s in slayer.stuff:
            self.change_layer(s, 0)
