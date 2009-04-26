import e32
import key_codes
import time
from pwidget import *
from pwcolor import *
from graphics import *
from pwcanvas import *
from pwfill import *

class PWClock(object):
    def __init__(self, owner):
        self.name = u"Clock"
        self.analog_bg = Image.open('e:\\python\\lib\\clock.png')
        mask = Image.open('e:\\python\\lib\\clock-mask.png')
        self.mask = Image.new(self.analog_bg.size, 'L')
        self.mask.blit(mask)
        self.owner = owner
        
    def update_time(self):
        now = time.localtime()
        hour = now[3]
        minute = now[4]
        second = now[5]

    def redraw(self):
        self.owner.blit(self.analog_bg, target=(0,0), mask=self.mask)