from pwcolor import *
from pwcanvas import *
from graphics import *
from appuifw import *
from e32 import *

class PWProgressBar(object):
    def __init__(self, other_canvas, start=0, end=100, color=[0,0,77,255]):
        self.canvas_copy = PWCanvas.new(other_canvas.size)
        self.canvas_copy.blit(other_canvas)
        self.return_canvas = PWCanvas.new(self.canvas_copy.size)
        self.return_canvas.blit(other_canvas)
        self.start = start
        self.end = end
        self.value = 0
        self.color = PWColor(color)
        self.glow = PWColor(color)
        self.glow.combine(PWColor(WHITE), 0.35)
        self.canvas = other_canvas
        self.redraw()
    
    def close(self):
        self.canvas.blit(self.return_canvas)
    
    def set_start(self, start):
        self.start = start
        
    def set_end(self, end):
        self.end = end
    
    def set_value(self, value):
        if value > self.end:
            value = self.end
        elif value < self.start:
            value = self.start
        
        self.value = value
        self.redraw()

    def redraw(self):
        self.canvas_copy.blit(self.return_canvas)
        box_w = int(self.canvas_copy.size[0] * 0.8)
        box_h = 50
        box_l = int(self.canvas_copy.size[0] - box_w) / 2
        box_t = self.canvas_copy.size[1] - box_h - 5
        self.canvas_copy.round_rectangle((box_l, box_t, box_l + box_w, box_t + box_h), r = 5, outline=(0,0,0), fill=(255,255,255), opacity=1)
        #draw external progressbar
        box_w = box_w - 10
        box_h = 18
        box_l = box_l + 5
        box_t = box_t + 16 #sorry for these hardcoded numbers
        self.canvas_copy.rectangle((box_l, box_t, box_l + box_w, box_t + box_h), outline=(0,0,0), fill=(255,255,255))
        #draw internal progressbar
        box_w_100 = box_w - 2
        box_h = 8
        box_l = box_l + 1
        box_t = box_t + 1 #again, sorry for these hardcoded numbers
        box_w = int(((1.0 * self.value - self.start)/(1.0 * self.end - self.start)) * box_w_100)
        self.canvas_copy.rectangle((box_l, box_t, box_l + box_w, box_t + box_h), outline=None, fill=self.glow.get_color())
        box_t += box_h
        self.canvas_copy.rectangle((box_l, box_t, box_l + box_w, box_t + box_h), outline=None, fill=self.color.get_color())
        self.canvas.blit(self.canvas_copy)
        ao_sleep(0.1)