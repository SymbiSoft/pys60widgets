import re
from graphics import Image

__all__ = ["PWColor","WHITE","BLACK","RED","GREEN","BLUE","YELLOW","MAGENTA","CYAN","GRAY"]

WHITE   = [255,255,255,255]
BLACK   = [0,0,0,255]
RED     = [255,0,0,255]
GREEN   = [0,255,0,255]
BLUE    = [0,0,255,255]
YELLOW  = [255,255,0,255]
MAGENTA = [255,0,255,255]
CYAN    = [0,255,255,255]
GRAY    = [128,128,128,255]

class PWColor(object):
    """ Color representation with some operations
    """
    def __init__(self, scolor=[0,0,0,255]):
        self.set_color(scolor)

    def set_color(self, scolor):
        """ Use: #RRGGBBAA or [R, G, B, A]
            default color: black (#000000ff) (0, 0, 0, 255)
        """
        if isinstance(scolor, str):
            #RRGGBBAA
            regex = re.compile(u"#{0,1}([0-9a-f]{2})([0-9a-f]{2})([0-9a-f]{2})([0-9a-f]{2}){0,1}", re.IGNORECASE)
            m = regex.match(scolor)
            if m:
                if m.group(4):
                    alpha = int("0x" + m.group(4), 16)
                else:
                    alpha = 255

                self.color = [int("0x" + m.group(1), 16), 
                              int("0x" + m.group(2), 16),
                              int("0x" + m.group(3), 16),
                              alpha]
            else:
                self.color = [0,0,0,255]
        elif isinstance(scolor, list):
            # [R, G, B, A]
            self.color = [ max(0,int(c)) for c in scolor ]
        else:
            self.color = [0,0,0,255]

    def get_color(self):
        return (self.color[0],self.color[1],self.color[2])
    
    def combine(self, other, perc):
        self.color = map(lambda a,b: int(a*(1-perc)+0.5) + int(b*perc+0.5), self.color, other.color)

    def inverse(self):
        return  map(lambda a,b: a ^ b, self.color, [255,255,255,255])

    def xor(self, other):
        return  map(lambda a,b: a ^ b, self.color, other.color)

    def __str__(self):
        return "#" + "".join([ "%02X" % c for c in self.color ])

    def __eq__(self, other):
        return self.color == other.color

    def __ne__(self, other):
        return self.color != other.color
        
    def gradient(self, img, other, orientation = (0,0)):
        """ Creates a gradient on given image with two colors
            orientation: 0 => horizontal, 
                            0 :> left to right (self to other)
                            1 :> right to left (other to self)
                         1 => vertical,
                            0 :> top to bottom (self to other)
                            1 :> bottom to top (other to self)
            size: (with, height)
        """
        if orientation[1] == 0:
            c1 = self.get_color()
            c2 = other.get_color()
        else:
            c1 = other.get_color()
            c2 = self.get_color()
        
        if orientation[0] == 0:
            d = img.size[0]
            for i in range(d):
                c = map(lambda a,b: (a*(d-i) + b*i)/d, c1, c2)
                img.line(((i,0),(i,d)),outline=tuple(c))
        else:
            d = img.size[1]
            for i in range(d):
                c = map(lambda a,b: (a*(d-i) + b*i)/d, c1, c2)
                img.line(((0,i),(d,i)),outline=tuple(c))