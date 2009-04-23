from pwidget import *
from random import randint
import e32

class PWDemo(PWidget):

    def __init__(self,mngr):    
        self.name = u"Demo"
        PWidget.__init__(self,mngr,self.name)
        self.timer = e32.Ao_timer()
        self.timer.after(4,self.sampler)
        self.sampling = True

    def sampler(self):
        if self.sampling:
            self.redraw()
            self.timer.after(4,self.sampler)
    
    def get_name(self):
        return self.name

    def run(self):
        self.add_window(self)  

    def get_color(self):
        return (randint(0,255),randint(0,255),randint(0,255))
    
    def update_canvas(self): 
        self.canvas.clear(self.get_color())
