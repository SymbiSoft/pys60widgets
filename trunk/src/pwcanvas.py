from pwcolor import *
from graphics import *
from PWFill import *
from e32 import *
import _graphics

__all__ = ["PWCanvas"]

class PWCanvas(Image):
    def round_rectangle(self, pos, r=5, outline=None, fill=None, opacity=1):
        o = outline
        f = fill
        op = int(opacity * 255)
        #create alpha mask if needed
        if isinstance(f, PWFill) or (op < 255):
            size = (pos[2]-pos[0], pos[3]-pos[1])
            alpha_pos = (0,0,size[0],size[1])
            alpha = PWCanvas.new(size,'L')
            alpha.clear(0)
            self._round_rectangle(alpha, alpha_pos, r, fill=(op,op,op))

        if isinstance(f, tuple): 
            #solid color
            if op == 255: 
                #simple round_rectangle solid colored
                self._round_rectangle(self, pos, r, outline=o, fill=f)
            else: 
                #use mask to make rectangle transparent
                rrect = PWCanvas.new(size)
                self._round_rectangle(rrect, alpha_pos, r, fill=f)
                self.blit(rrect, target=(pos[0],pos[1]), mask=alpha)
        elif isinstance(f, PWFill):
            #create the gradient and apply the mask
            gradient = PWCanvas.new(size)
            fill.gradient_fill(gradient)
            self.blit(gradient, target=(pos[0],pos[1]), mask=alpha)

    def _round_rectangle(self, canvas, pos, r=5, outline=None, fill=None):
        """Draws a rounded rectangle on a PWCanvas using the following parameters:
            * canvas = a PWCanvas object or Image object
            * r = corner radius
            * outline = color of outline
            * fill = an RGB tuple or 0xRRGGBB integer
        """
        #Just to make things shorter ;)
        o = outline
        f = fill
        if r > 0:
            d = r * 2 #diameter
            #corner circles
            canvas.ellipse((pos[0], pos[1], pos[0] + d, pos[1] + d), outline=o, fill=f)
            canvas.ellipse((pos[2] - d, pos[3] - d, pos[2], pos[3]), outline=o, fill=f)
            canvas.ellipse((pos[0], pos[3] - d, pos[0] + d, pos[3]), outline=o, fill=f)
            canvas.ellipse((pos[2] - d, pos[1], pos[2], pos[1] + d), outline=o, fill=f)
            #border rectangles
            canvas.rectangle((pos[0] + r, pos[1], pos[2] - r, pos[1] + r), outline=None, fill=f)
            canvas.rectangle((pos[0] + r, pos[3] - r, pos[2] - r, pos[3]), outline=None, fill=f)
            canvas.rectangle((pos[0], pos[1] + r, pos[0] + r, pos[3] - r), outline=None, fill=f)
            canvas.rectangle((pos[2] - r, pos[1] + r, pos[2], pos[3] - r), outline=None, fill=f)
            #body
            canvas.rectangle((pos[0] + r, pos[1] + r,pos[2] - r, pos[3] - r), outline=None, fill=f)
            #borders
            if fill is not None:
                canvas.line((pos[0] + r, pos[1], pos[2] - r, pos[1]), outline=o)
                canvas.line((pos[0] + r, pos[3], pos[2] - r, pos[3]), outline=o)
                canvas.line((pos[0], pos[1] + r, pos[0], pos[3] - r), outline=o)
                canvas.line((pos[2], pos[1] + r, pos[2], pos[3] - r), outline=o)
        else:
            #if r == 0 than the round_rectangle is just a rectangle. Let's make things simple
            canvas.rectangle(pos, outline=None, fill=f)

    def new(size, mode='RGB16'):
        """ rewrite the static "new" method to
        return a PWCanvas instead of an Image"""
        if not Image._modemap.has_key(mode):
            raise ValueError('invalid mode')
        return PWCanvas(_graphics.ImageNew(size,Image._modemap[mode]))

    new = staticmethod(new)