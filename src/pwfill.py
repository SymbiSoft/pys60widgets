from pwcolor import *

__all__ = ["PWFill","HORIZONTAL_GRADIENT","VERTICAL_GRADIENT","LINEAR_GRADIENT","RADIAL_GRADIENT"]

HORIZONTAL_GRADIENT = 0
VERTICAL_GRADIENT   = 1

LINEAR_GRADIENT = 0
RADIAL_GRADIENT = 1

class PWFill(object):
    def __init__(self, start_color, end_color, type=LINEAR_GRADIENT, mode=HORIZONTAL_GRADIENT, position=(0,0)):
        self.start_color = start_color
        self.end_color = end_color
        self.mode = mode
        self.type = type
        self.position = position
    
    def gradient_fill(self, img):
        c1 = self.start_color.get_color()
        c2 = self.end_color.get_color()
        if self.mode == HORIZONTAL_GRADIENT:
            d = img.size[0]
            for i in range(d):
                c = map(lambda a,b: (a*(d-i) + b*i)/d, c1, c2)
                img.line(((i,0),(i,d)),outline=tuple(c))
        else:
            d = img.size[1]
            for i in range(d):
                c = map(lambda a,b: (a*(d-i) + b*i)/d, c1, c2)
                img.line(((0,i),(d,i)),outline=tuple(c))

    def getclass(self):
        return PWFill

    __class__ = property(getclass)