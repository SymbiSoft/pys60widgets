from pwcolor import *

__all__ = ["PWFill","HORIZONTAL_GRADIENT","VERTICAL_GRADIENT","LINEAR_GRADIENT","RADIAL_GRADIENT"]

HORIZONTAL_GRADIENT = 1
VERTICAL_GRADIENT   = 2

LINEAR_GRADIENT = 1
RADIAL_GRADIENT = 2

class PWFill(object):
    def __init__(self, start_color, end_color, type=LINEAR_GRADIENT, mode=HORIZONTAL_GRADIENT, position=(0,0)):
        self.start_color = start_color
        self.end_color = end_color
        self.mode = mode
        self.type = type
        self.position = position