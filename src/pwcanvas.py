from pwcolor import *
from graphics import *
import _graphics
from e32 import *

__all__ = ["PWCanvas"]

class PWCanvas(Image):
    def round_rectangle(self, pos, r=5, outline=None, fill=None):
        d = r * 2
        o = outline
        f = fill
        #corner circles
        self.ellipse((pos[0], pos[1], pos[0] + d, pos[1] + d), outline=o, fill=f)
        self.ellipse((pos[2] - d, pos[3] - d, pos[2], pos[3]), outline=o, fill=f)
        self.ellipse((pos[0], pos[3] - d, pos[0] + d, pos[3]), outline=o, fill=f)
        self.ellipse((pos[2] - d, pos[1], pos[2], pos[1] + d), outline=o, fill=f)
        #body rectangle
        self.rectangle((pos[0] + r, pos[1] + r,pos[2] - r, pos[3] - r), outline=None, fill=f)
        #border rectangles
        self.rectangle((pos[0] + r, pos[1], pos[2] - r, pos[1] + r), outline=None, fill=f)
        self.rectangle((pos[0] + r, pos[3] - r, pos[2] - r, pos[3]), outline=None, fill=f)
        self.rectangle((pos[0], pos[1] + r, pos[0] + r, pos[3] - r), outline=None, fill=f)
        self.rectangle((pos[2] - r, pos[1] + r, pos[2], pos[3] - r), outline=None, fill=f)
        #borders
        if fill is not None:
            self.line((pos[0] + r, pos[1], pos[2] - r, pos[1]), outline=o)
            self.line((pos[0] + r, pos[3], pos[2] - r, pos[3]), outline=o)
            self.line((pos[0], pos[1] + r, pos[0], pos[3] - r), outline=o)
            self.line((pos[2], pos[1] + r, pos[2], pos[3] - r), outline=o)

    def new(size, mode='RGB16'):
        if not Image._modemap.has_key(mode):
            raise ValueError('invalid mode')
        return PWCanvas(_graphics.ImageNew(size,Image._modemap[mode]))

    new = staticmethod(new)
