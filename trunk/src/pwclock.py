import e32
import key_codes
import time
import math
from pwidget import *
from pwcolor import *
from graphics import *
from pwcanvas import *
from pwfill import *

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

class PWClock(object):
    def __init__(self, owner):
        self.name = u"Clock"
        self.hands = [0,0,0]
        self.analog_bg = Image.open('e:\\python\\lib\\clock.png')
        mask = Image.open('e:\\python\\lib\\clock-mask.png')
        self.mask = Image.new(self.analog_bg.size, 'L')
        self.canvas = PWCanvas.new(self.analog_bg.size)
        self.bg = Image.new(owner.size)
        self.bg.blit(owner)
        self.mask.blit(mask)
        self.update_time()
        self.owner = owner
    
    def update_time(self):
        now = time.localtime()
        self.hour   = now[3]
        self.minute = now[4]
        self.second = now[5]

    def redraw(self):
        self.update_time()
        self.draw_background()
        self.hands_vectors()
        self.owner.blit(self.canvas)
    
    def draw_background(self):
        self.canvas.blit(self.bg)
        self.canvas.blit(self.analog_bg, mask=self.mask)
    
    def hands_vectors(self):
        self.hands[0] = rotate([0, -60], self.hour*hour_degree+(self.minute*minute_degree/60.0))
        self.hands[1] = rotate([0, -80], self.minute*minute_degree)
        self.hands[2] = rotate([0, -75], self.second*minute_degree)
        self.canvas.line((113,113,113+self.hands[0][0],113+self.hands[0][1]), width=4, outline=(255,255,255))
        self.canvas.line((113,113,113+self.hands[1][0],113+self.hands[1][1]), width=4, outline=(255,255,255))
        self.canvas.line((113,113,113+self.hands[2][0],113+self.hands[2][1]), width=2, outline=(255,0,0))
        