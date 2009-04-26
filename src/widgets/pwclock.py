import e32
import key_codes
import time
import math
from pwidget import *
from pwcolor import *
from graphics import *
from pwcanvas import *
from pwfill import *

__all__ = ["PWClock"]

minute_degree = math.pi / 30.0 #6 degrees
hour_degree = 5 * minute_degree

def matrix_multiply(m, v):
    """
    Matrix-vector multiply
    """
    rows = len(m)
    w = [0]*rows
    irange = range(len(v))
    sum = 0
    for j in range(rows):
        r = m[j]
        for i in irange:
            sum += r[i]*v[i]
        w[j],sum = sum,0
    return w

def rotate(v, t):
    c = math.cos(t)
    s = math.sin(t)
    m = [[c,-s],[s,c]]
    return matrix_multiply(m, v)

class PWClock(PWidget):
    def __init__(self, mngr, **attrs):
        self.name = u"Clock"
        self.menu = []
        PWidget.__init__(self,mngr,self.name)
        self.hands = [0,0,0]
        self.analog_bg = Image.open(u'e:\\python\\lib\\clock.png')
        mask = Image.open(u'e:\\python\\lib\\clock-mask.png')
        self.mask = Image.new(mask.size, 'L') #convert mask to 8-bits grayscale
        self.mask.blit(mask) #convert mask to 8-bits grayscale
        self.bg = PWCanvas.new(self.size)
        self.bg.clear()
        c1 = PWColor(GREEN)
        c2 = PWColor(YELLOW)
        self.bg.round_rectangle((0,0, self.size[0],self.size[1]), 
                                r=0, 
                                outline=None, 
                                fill=PWFill(c1, c2, mode=VERTICAL_GRADIENT))
        self.timer = e32.Ao_timer()
        self.timer.after(5,self.update_clock)        

    def get_name(self):
        return self.name
        
    def run(self):
        self.add_window(self)
        #self.update_clock()
    
    def update_clock(self):
        self.redraw()
        self.timer.after(0.1, self.update_clock)
    
    def update_time(self):
        now = time.localtime()
        self.day    = str(now[2])
        self.hour   = now[3]
        self.minute = now[4]
        self.second = now[5]
    
    def draw_background(self):
        self.canvas.blit(self.bg)
        self.canvas.blit(self.analog_bg, mask=self.mask)
        self.canvas.text((170,120), u"" + self.day, fill = 0, font=('dense', 14, FONT_BOLD | FONT_ANTIALIAS))
    
    def hands_vectors(self):
        self.hands[0] = rotate([0, -60], self.hour*hour_degree+(self.minute*hour_degree/60.0))
        self.hands[1] = rotate([0, -80], self.minute*minute_degree+(self.second*minute_degree/60.0))
        self.hands[2] = rotate([0, -75], self.second*minute_degree)
        self.canvas.line((113,113,113+self.hands[0][0],113+self.hands[0][1]), width=4, outline=(255,255,255))
        self.canvas.line((113,113,113+self.hands[1][0],113+self.hands[1][1]), width=4, outline=(255,255,255))
        self.canvas.line((113,113,113+self.hands[2][0],113+self.hands[2][1]), width=2, outline=(255,0,0))

    def update_canvas(self):
        self.update_time()
        self.draw_background()
        self.hands_vectors()