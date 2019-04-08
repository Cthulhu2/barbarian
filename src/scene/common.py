# -*- coding: utf-8 -*-
import sys

from pygame.locals import *
from pygame.sprite import LayeredDirty
from pygame.time import get_ticks


class EmptyScene(LayeredDirty):
    def __init__(self, screen, background, *sprites_, **kwargs):
        super(EmptyScene, self).__init__(*sprites_, **kwargs)
        self.set_timing_treshold(1000.0 / 25.0)
        self.clear(screen, background)
        self.timer = get_ticks()

    @staticmethod
    def process_event(evt):
        if evt.type == QUIT or (evt.type == KEYUP and evt.key == K_ESCAPE):
            sys.exit()
