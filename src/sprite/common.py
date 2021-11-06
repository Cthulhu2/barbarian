# -*- coding: utf-8 -*-
from os.path import join

from pygame import image
from pygame.font import Font
from pygame.sprite import DirtySprite
from pygame.transform import scale, rotate, flip

from config import IMAGE_PATH

img_cache = {}


def get_image(name, w, h, angle, xflip, fill, blend_flags):
    key_ = sum((hash(name), hash(w), hash(h), hash(angle), hash(xflip),
                hash(fill), hash(blend_flags)))

    if key_ in img_cache:
        img = img_cache[key_]
    else:
        img = image.load(join(IMAGE_PATH, name)).convert_alpha()
        if fill and blend_flags:
            img = img.copy()
            img.fill(fill, special_flags=blend_flags)
        if w > 0 or h > 0:
            img = scale(img, (w, h))
        if angle != 0:
            img = rotate(img, angle)
        if xflip:
            img = flip(img, xflip, False)
        img_cache[key_] = img
    return img


class Txt(DirtySprite):
    font_cache = {}
    cache = {}

    def __init__(self, font_, size, msg, color_, x, y, *groups):
        super(Txt, self).__init__(*groups)
        self._x = x
        self._y = y
        self._msg = msg
        self._size = size
        self._font = font_
        self._color = color_
        self.image, self.rect = self._update_image()

    @property
    def msg(self):
        return self._msg

    @msg.setter
    def msg(self, msg):
        if self._msg != msg:
            self._msg = msg
            self.image, self.rect = self._update_image()
            self.dirty = 1

    @property
    def color(self):
        return self._msg

    @color.setter
    def color(self, color):
        if self._color != color:
            self._color = color
            self.image, self.rect = self._update_image()
            self.dirty = 1

    def _update_image(self):
        font_key = hash(self._font) + hash(self._size)
        if font_key in Txt.font_cache:
            font_ = Txt.font_cache[font_key]
        else:
            font_ = Font(self._font, self._size)
            Txt.font_cache[font_key] = font_

        key_ = font_key + hash(self.msg) + hash(self._color)
        if key_ in Txt.cache:
            img = Txt.cache[key_]
        else:
            img = font_.render(str(self.msg), True, self._color)
            Txt.cache[key_] = img
        rect = img.get_rect(topleft=(self._x, self._y))
        return img, rect
