# -*- coding: utf-8 -*-
from pygame import Rect
from pygame.sprite import DirtySprite
from pygame.time import get_ticks

from .common import get_image


class Frame(object):
    __slots__ = ('rect', 'duration', 'image', 'move_base', 'name',
                 'dx', 'dy', 'w', 'h', 'angle',
                 'xflip', 'fill', 'blend_flags',
                 'pre_action', 'post_action')

    def __init__(self, name, dx=0, dy=0, w=0, h=0,
                 duration=200, angle=0, xflip=False,
                 fill=None, blend_flags=None, move_base=None,
                 pre_action=None, post_action=None):
        self.duration = duration
        self.image = get_image(name, w, h, angle, xflip,
                               fill, blend_flags)
        self.rect = self.image.get_rect().move(dx, dy)
        self.move_base = move_base
        #
        self.name = name
        self.dx = dx
        self.dy = dy
        self.w = w
        self.h = h
        self.angle = angle
        self.xflip = xflip
        self.fill = fill
        self.blend_flags = blend_flags
        self.pre_action = pre_action
        self.post_action = post_action

    def rtl(self):
        dx = -self.dx
        move_base = None
        if self.move_base:
            move_base = (-self.move_base[0], self.move_base[1])
        xflip = not self.xflip

        return Frame(self.name, dx, self.dy, self.w, self.h,
                     self.duration, self.angle, xflip, self.fill,
                     self.blend_flags, move_base,
                     self.pre_action, self.post_action)


class Anim(object):
    __slots__ = 'name', 'frames'

    def __init__(self, name, *frames):
        self.name = name
        self.frames = frames


class AnimatedSprite(DirtySprite):
    def __init__(self, center, animations, *groups):
        super(AnimatedSprite, self).__init__(*groups)
        self.anims = animations
        self.animTimer = get_ticks()
        self._animSpeed = 1.0
        self._animStopped = False

        self.anim = next(iter(self.anims))
        self.frames = self.anims[self.anim]
        self.frameNum = 0
        self.frame = self.frames[self.frameNum]
        self.frame_duration = self.frame.duration / self.animSpeed

        self.image = self.frame.image
        self.rect = Rect(0, 0, 0, 0)
        self.center = center
        self._update_rect()

    def _get_x(self):
        return self.center[0]

    def _set_x(self, x):
        self.center = (x, self.center[1])
        self._update_rect()

    x = property(_get_x, _set_x)

    def _get_y(self):
        return self.center[1]

    def _set_y(self, y):
        self.center = (self.center[0], y)
        self._update_rect()

    y = property(_get_y, _set_y)

    def _get_anim_speed(self):
        return self._animSpeed

    def _set_anim_speed(self, speed):
        self._animSpeed = round(min(3, max(0, speed)), 3)
        self.frame_duration = self._calc_duration(self.frame.duration)

    animSpeed = property(lambda self: self._get_anim_speed(),
                         lambda self, speed: self._set_anim_speed(speed))

    def _get_anim_stopped(self):
        return self._animStopped

    def _set_anim_stopped(self, stop):
        self._animStopped = stop

    animStopped = property(lambda self: self._get_anim_stopped(),
                           lambda self, stop: self._set_anim_stopped(stop))

    def select_anim(self, anim):
        if anim in self.anims:
            self.animStopped = False
            self.anim = anim
            self.frames = self.anims[anim]
            self.animTimer = get_ticks()
            self.frameNum = -1
            self.frame = None
            self.next_frame()
            self.visible = True
        else:
            self.visible = False

    def update(self, current_time, *args):
        if self.visible and not self.animStopped:
            passed = current_time - self.animTimer
            if passed > self.frame_duration and self.animSpeed > 0:
                self.animTimer = current_time
                self.next_frame()

    def _calc_duration(self, duration):
        if self.animSpeed > 0:
            return duration / self.animSpeed
        else:
            return duration

    def on_pre_action(self, anim, action):
        pass

    def on_post_action(self, anim, action):
        pass

    def prev_frame(self):
        self.frameNum -= 1
        if self.frameNum == -1:
            self.frameNum = len(self.frames) - 1

        prev = self.frames[self.frameNum]
        if self.frame != prev:
            if self.frame.post_action:
                self.on_post_action(self.anim, self.frame.post_action)
            if self.frame.move_base:  # Undo the current frame move_base
                dx, dy = self.available_move(-self.frame.move_base[0],
                                             -self.frame.move_base[1])
                self.move(dx, dy)
            self.frame = prev
            self.frame_duration = self._calc_duration(self.frame.duration)
            self.image = self.frame.image

            self._update_rect()
            if self.frame.pre_action:
                self.on_pre_action(self.anim, self.frame.pre_action)
            self.dirty = 1

    def next_frame(self):
        self.frameNum += 1
        if self.frameNum == len(self.frames):
            self.frameNum = 0
        next_ = self.frames[self.frameNum]
        if self.frame != next_:
            if self.frame and self.frame.post_action:
                cur_anim = self.anim
                self.on_post_action(self.anim, self.frame.post_action)
                if cur_anim != self.anim or self.animStopped:
                    # Animation changed or stopped, don't process next frame
                    return

            self.frame = next_
            self.frame_duration = self._calc_duration(self.frame.duration)
            self.image = self.frame.image
            if self.frame.move_base:
                dx, dy = self.available_move(self.frame.move_base[0],
                                             self.frame.move_base[1])
                self.move(dx, dy)
            self._update_rect()
            if self.frame.pre_action:
                self.on_pre_action(self.anim, self.frame.pre_action)
            self.dirty = 1

    def _update_rect(self):
        self.rect.size = self.frame.rect.size
        self.rect.center = self.center
        self.rect.move_ip(self.frame.rect.x, self.frame.rect.y)

    @staticmethod
    def available_move(dx, dy):
        return dx, dy

    def move(self, dx, dy):
        self.center = (self.center[0] + dx, self.center[1] + dy)
        self.rect.move_ip(dx, dy)
        self.dirty = 1


def rtl_anims(anims):
    rtl = {}
    for anim, frames in anims.items():
        rtl[anim] = [f.rtl() for f in frames]
    return rtl
