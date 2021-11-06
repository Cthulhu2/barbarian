# -*- coding: utf-8 -*-
from math import sin

from .animated import rtl_anims, AnimatedSprite, Frame


class Hit(AnimatedSprite):
    anims = {
        'hit': [
            Frame('barbarian-blue/hit/hit_0.png', 0, 0, duration=50),
            Frame('barbarian-blue/hit/hit_1.png', 0, 0, duration=50),
            Frame('barbarian-blue/hit/hit_2.png', 0, 0, duration=50,
                  post_action='kill'),
        ],
    }

    def __init__(self, x, y):
        super(Hit, self).__init__((x, y), Hit.anims)

    def on_post_action(self, anim, action):
        if action == 'kill':
            self.kill()


class Blood(AnimatedSprite):
    anims = {
        'decapitate': [
            Frame('barbarian-blue/blood/blood_0.png', -2, -46, duration=150),
            Frame('barbarian-blue/blood/blood_1.png', 40, -23, duration=150),
            Frame('barbarian-blue/blood/blood_2.png', 40, -30, duration=150),
            Frame('barbarian-blue/blood/blood_3.png', 125, 47, duration=150,
                  angle=-90),
            Frame('barbarian-blue/blood/blood_4.png', 125, 47, duration=150,
                  angle=-90, post_action='hide'),
        ],
    }
    anims_rtl = rtl_anims(anims)

    def __init__(self, x, y, rtl=False):
        super(Blood, self).__init__(
            (x, y),
            Blood.anims_rtl if rtl else Blood.anims)

    def on_post_action(self, anim, action):
        if anim == 'decapitate' and action == 'hide':
            self.visible = False


class Head(AnimatedSprite):
    anims = {
        'decapitate': [
            *(Frame('barbarian-blue/head/head_0.png' if 0 <= i < 5 else
                    'barbarian-blue/head/head_1.png' if 5 <= i < 10 else
                    'barbarian-blue/head/head_2.png' if 10 <= i < 15 else
                    'barbarian-blue/head/head_3.png' if 15 <= i < 20 else
                    'barbarian-blue/head/head_4.png' if 20 <= i < 25 else
                    'barbarian-blue/head/head_5.png',
                    int(2 - i * 2),  # x= 2..-58
                    int(sin((i + 73) / 16.35) * 105 + 50),  # y = -52..-55..50
                    duration=10)
              for i in range(30)),
            Frame('barbarian-blue/head/head_5.png', -60, 50, duration=10000),

            # Frame('barbarian-blue/head/head_0.png', 2, -52, duration=150),
            # Frame('barbarian-blue/head/head_1.png', -10, -55, duration=150),
            # Frame('barbarian-blue/head/head_2.png', -20, -50, duration=150),
            # Frame('barbarian-blue/head/head_3.png', -30, -15, duration=150),
            # Frame('barbarian-blue/head/head_4.png', -45, 15, duration=150),
            # Frame('barbarian-blue/head/head_5.png', -60, 50, duration=10000),
        ],
    }
    anims_rtl = rtl_anims(anims)

    def __init__(self, x, y, rtl=False):
        super(Head, self).__init__(
            (x, y),
            Head.anims_rtl if rtl else Head.anims)


class Barbarian(AnimatedSprite):
    anims = {
        'idle': [
            Frame('barbarian-blue/idle.png', duration=3000),
            *((Frame('barbarian-blue/cry_0.png', 2, 1),
               Frame('barbarian-blue/cry_1.png', 2, 1)) * 2),
            Frame('barbarian-blue/cry_0.png', 2, 1),
        ],
        'cry': [
            Frame('barbarian-blue/idle.png'),
            *((Frame('barbarian-blue/cry_0.png', 2, 1),
               Frame('barbarian-blue/cry_1.png', 2, 1)) * 2),
            Frame('barbarian-blue/cry_0.png', 2, 1),
        ],
        'win': [
            Frame('barbarian-blue/idle.png'),
            Frame('barbarian-blue/win_0.png', 6, -2, duration=300),
            Frame('barbarian-blue/win_1.png', 4, -2, duration=300),
            Frame('barbarian-blue/win_2.png', 2, -9, duration=1000),
            Frame('barbarian-blue/win_1.png', 4, -2, duration=100),
            Frame('barbarian-blue/win_0.png', 6, -2,
                  post_action='end'),
        ],
        'loose': [
            Frame('barbarian-blue/idle.png'),
            Frame('barbarian-blue/duck_0.png', 0, 9, duration=100),
            Frame('barbarian-blue/loose_0.png', 0, 36, duration=300),
            Frame('barbarian-blue/loose_1.png', 12, 36, duration=100),
            Frame('barbarian-blue/loose_2.png', 0, 45, duration=300),
        ],
        'decapitate': [
            Frame('barbarian-blue/idle.png', duration=10,
                  pre_action='start'),
            Frame('barbarian-blue/decapitate_0.png', 0, 11, duration=150,
                  pre_action='show_blood_n_head'),
            Frame('barbarian-blue/decapitate_1.png', 40, 26, duration=300),
            Frame('barbarian-blue/decapitate_2.png', 62, 47,
                  post_action='end', duration=1000),
        ],
        'fall': [
            Frame('barbarian-blue/idle.png'),
            Frame('barbarian-blue/fall_0.png', 0, 7, move_base=(-14, 0)),
            Frame('barbarian-blue/fall_1.png', 0, 42, move_base=(-14, 0)),
            Frame('barbarian-blue/fall_2.png', -1, 25),
            Frame('barbarian-blue/duck_0.png', 0, 9, duration=100,
                  post_action='end'),
        ],
        'jump': [
            Frame('barbarian-blue/idle.png'),
            *(Frame('barbarian-blue/jump_0.png', 0, -dy, duration=1)
              for dy in range(0, 20, 2)),
            *(Frame('barbarian-blue/jump_1.png', 15, -dy,
                    duration=int(1 + dy))
              for dy in range(20, 30, 1)),
            *(Frame('barbarian-blue/jump_1.png', 15, -dy,
                    duration=int(1 + dy / 2))
              for dy in range(30, 20, -1)),
            *(Frame('barbarian-blue/jump_0.png', 0, -dy, duration=1)
              for dy in range(20, 0, -3)),
            Frame('barbarian-blue/idle.png', duration=1,
                  post_action='end')
        ],
        'hurt': [
            Frame('barbarian-blue/idle.png', duration=1),
            Frame('barbarian-blue/hurt_0.png', 4, 1, duration=10,
                  move_base=(-10, 0)),
            # https://www.mathe-fa.de
            *(Frame('barbarian-blue/hurt_0.png',
                    4 - x, int(1 - sin((x - 1) / 4) * 5),
                    duration=7)
              for x in range(14)),
            *(Frame('barbarian-blue/hurt_1.png', -15 - x, -5 + x,
                    duration=10)
              for x in range(1, 10, 1)),
            Frame('barbarian-blue/hurt_1.png', -26, 5, duration=50,
                  post_action='end'),
        ],
        'move_forward': [
            # Frame('barbarian-blue/idle.png'),
            Frame('barbarian-blue/move_0.png', 10, -3),
            Frame('barbarian-blue/move_1.png', -7, -3, move_base=(41, 0)),
            Frame('barbarian-blue/move_2.png', 14, -2),
            Frame('barbarian-blue/move_1.png', -7, -3, move_base=(41, 0)),
        ],
        'move_backward': [
            # Frame('barbarian-blue/idle.png'),
            Frame('barbarian-blue/move_0.png', -2, -3),
            Frame('barbarian-blue/move_1.png', 8, -3, move_base=(-37, 0)),
            Frame('barbarian-blue/move_2.png', -4, -2),
            Frame('barbarian-blue/move_1.png', 5, -3, move_base=(-30, 0)),
        ],
        'roll_forward': [
            Frame('barbarian-blue/idle.png'),
            Frame('barbarian-blue/roll_0.png', 0, 20, duration=150),
            *(Frame('barbarian-blue/roll_2.png',
                    15, int(50 + 8 * sin(3.14 * r / 5)), duration=10,
                    angle=int(90 - r * 90 / 5), move_base=(6, 0))
              for r in range(0, 5, 1)),
            Frame('barbarian-blue/roll_2.png', 1, 52, duration=10,
                  move_base=(20, 0), post_action='push'),
            *(Frame('barbarian-blue/roll_2.png',
                    -5, int(52 + sin(3.14 * r / 5)), duration=10,
                    angle=int(-r * 90 / 5), move_base=(6, 0))
              for r in range(1, 5, 1)),
            Frame('barbarian-blue/roll_4.png', 0, 15, duration=150,
                  move_base=(30, 0)),
            Frame('barbarian-blue/idle.png', duration=1,
                  post_action='end'),
            # Frame('barbarian-blue/roll_0.png', 0, 20, duration=100),
            # Frame('barbarian-blue/roll_1.png', 0, 50, duration=100,
            #       move_base=(30, 0)),
            # Frame('barbarian-blue/roll_2.png', 0, 50, duration=100,
            #       move_base=(20, 0)),
            # Frame('barbarian-blue/roll_3.png', 0, 50, duration=100,
            #       move_base=(30, 0)),
            # Frame('barbarian-blue/roll_4.png', 0, 15, duration=100,
            #       move_base=(30, 0)),
        ],
        'roll_backward': [
            Frame('barbarian-blue/idle.png'),
            Frame('barbarian-blue/roll_4.png', -5, 15, duration=150),
            *(Frame('barbarian-blue/roll_2.png',
                    -2, int(52 + sin(3.14 * r / 5)), duration=10,
                    angle=int(-r * 90 / 5), move_base=(-6, 0))
              for r in range(5, 1, -1)),
            Frame('barbarian-blue/roll_2.png', 8, 50, duration=10,
                  move_base=(-20, 0)),
            *(Frame('barbarian-blue/roll_2.png',
                    14, int(49 + 3 * sin(3.14 * r / 5)), duration=10,
                    angle=int(90 - r * 90 / 5), move_base=(-6, 0))
              for r in range(5, 0, -1)),
            Frame('barbarian-blue/roll_0.png', 0, 20, duration=150,
                  move_base=(-30, 0)),
            Frame('barbarian-blue/idle.png', duration=1,
                  post_action='end')
            # Frame('barbarian-blue/roll_4.png', -5, 15, duration=100),
            # Frame('barbarian-blue/roll_3.png', 0, 50, duration=100,
            #       move_base=(-30, 0)),
            # Frame('barbarian-blue/roll_2.png', 0, 50, duration=100,
            #       move_base=(-20, 0)),
            # Frame('barbarian-blue/roll_1.png', 0, 50, duration=100,
            #       move_base=(-30, 0)),
            # Frame('barbarian-blue/roll_0.png', 0, 20, duration=100,
            #       move_base=(-30, 0)),
        ],
        'high_defense': [
            Frame('barbarian-blue/idle.png'),
            Frame('barbarian-blue/hdef_0.png', -3, 3,
                  post_action='end'),
        ],
        'mid_defense': [
            Frame('barbarian-blue/idle.png'),
            Frame('barbarian-blue/hdef_0.png', -3, 3, duration=100),
            Frame('barbarian-blue/mdef_0.png', -4, 1,
                  post_action='end'),
        ],
        'headbutt': [
            Frame('barbarian-blue/idle.png'),
            Frame('barbarian-blue/headbutt_0.png', 7, 0, duration=100),
            Frame('barbarian-blue/headbutt_1.png', 7, -1, move_base=(12, 0),
                  pre_action='check_hit'),
        ],
        'kick': [
            Frame('barbarian-blue/idle.png'),
            Frame('barbarian-blue/kick_0.png', -7, -2),
            Frame('barbarian-blue/kick_1.png', 3, -2,
                  pre_action='check_hit'),
        ],
        'overcut': [
            Frame('barbarian-blue/idle.png'),
            Frame('barbarian-blue/overcut_0.png', -6, -2, duration=100),
            Frame('barbarian-blue/overcut_1.png', 5, -16, duration=50),
            Frame('barbarian-blue/overcut_2.png', 22, -2,
                  pre_action='check_hit'),
        ],
        'high_crosscut': [
            Frame('barbarian-blue/idle.png'),
            Frame('barbarian-blue/hdef_0.png', -3, 3, duration=100),
            Frame('barbarian-blue/hcrosscut_0.png', -5, -1, duration=50),
            Frame('barbarian-blue/hcrosscut_1.png', 19, 0,
                  pre_action='check_hit'),
        ],
        'mid_crosscut': [
            Frame('barbarian-blue/idle.png'),
            Frame('barbarian-blue/mcrosscut_0.png', 0, -2, duration=100),
            Frame('barbarian-blue/mcrosscut_1.png', -4, 4, duration=50),
            Frame('barbarian-blue/mcrosscut_2.png', 20, 4,
                  pre_action='check_hit'),
        ],
        'duck': [
            Frame('barbarian-blue/idle.png'),
            Frame('barbarian-blue/duck_0.png', 0, 9, duration=100),
            Frame('barbarian-blue/duck_1.png', -5, 19,
                  post_action='end'),
        ],
        'low_crosscut': [
            Frame('barbarian-blue/idle.png'),
            Frame('barbarian-blue/duck_0.png', 0, 9, duration=100),
            Frame('barbarian-blue/duck_1.png', -5, 19),
            Frame('barbarian-blue/lcrosscut_0.png', 6, 20, duration=100),
            Frame('barbarian-blue/duck_1.png', -5, 19, duration=50),
            Frame('barbarian-blue/lcrosscut_1.png', 30, 19,
                  pre_action='check_hit'),
            Frame('barbarian-blue/duck_1.png', -5, 19),
        ],
        'windmill': [
            # Frame('barbarian-blue/idle.png'),
            Frame('barbarian-blue/windmill_0.png', 3, 0, duration=100),
            Frame('barbarian-blue/windmill_1.png', 7, 1, duration=100),
            Frame('barbarian-blue/windmill_2.png', 1, 0, duration=100),
            Frame('barbarian-blue/windmill_3.png', 17, 0, duration=100,
                  pre_action='check_hit'),
        ],
        'helicopter': [
            Frame('barbarian-blue/idle.png'),
            Frame('barbarian-blue/heli_0.png', 12, -5),
            Frame('barbarian-blue/heli_1.png', 0, -5, move_base=(58, 0)),
            Frame('barbarian-blue/heli_2.png', -11, -5, move_base=(64, 0)),
            Frame('barbarian-blue/hcrosscut_1.png', 18, 0,
                  pre_action='check_hit'),
            Frame('barbarian-blue/idle.png', duration=1,
                  post_action='end'),
        ],
        'turn_around': [
            Frame('barbarian-blue/heli_0.png', 12, -5),
            Frame('barbarian-blue/heli_1.png', 0, -5, move_base=(58, 0)),
            Frame('barbarian-blue/heli_2.png', -11, -5, move_base=(64, 0)),
            Frame('barbarian-blue/idle.png', xflip=True, duration=1,
                  post_action='end'),
        ],
    }
    anims_rtl = rtl_anims(anims)

    def __init__(self, x, y, rtl=False, anim='idle'):
        super(Barbarian, self).__init__(
            (x, y),
            Barbarian.anims_rtl if rtl else Barbarian.anims)
        self.decapitated_blood = Blood(x, y, rtl)
        self.decapitated_head = Head(x, y, rtl)
        self.stuff = [self.decapitated_blood, self.decapitated_head]
        for s in self.stuff:
            s.visible = False
        #
        self.rtl = rtl
        self.select_anim(anim)

    @AnimatedSprite.speed.setter
    def speed(self, speed):
        for s in self.stuff:
            s.speed = speed
        super(Barbarian, Barbarian).speed.fset(self, speed)

    @AnimatedSprite.is_stopped.setter
    def is_stopped(self, stop):
        for s in self.stuff:
            s.is_stopped = stop
        super(Barbarian, Barbarian).is_stopped.fset(self, stop)

    def select_anim(self, anim):
        super(Barbarian, self).select_anim(anim)
        for s in self.stuff:
            s.select_anim(anim)

    def move(self, dx, dy):
        for s in self.stuff:
            s.move(dx, dy)
        super(Barbarian, self).move(dx, dy)

    def turn_around(self, rtl):
        self.anims = Barbarian.anims_rtl if rtl else Barbarian.anims
        self.decapitated_blood.anims = Blood.anims_rtl if rtl else Blood.anims
        self.decapitated_head.anims = Head.anims_rtl if rtl else Head.anims
        self.select_anim(self.anim)
        self.rtl = rtl

    def on_pre_action(self, anim, action):
        if anim == 'decapitate':
            if action == 'start':
                self.decapitated_blood.visible = False
                self.decapitated_head.visible = False
            elif action == 'show_blood_n_head':
                self.decapitated_blood.select_anim(anim)
                self.decapitated_head.select_anim(anim)

    def kill(self):
        for s in self.stuff:
            s.kill()
        super(Barbarian, self).kill()
