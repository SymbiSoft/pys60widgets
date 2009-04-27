from pwidget import *
from random import randint
import e32

class PWDemo(PWidget):

    def __init__(self,mngr):    
        info = {'name':u"Widget demo",
                'description':u"Python for S60 widget demo",
                'author':u"Marcelo Barros",
                'version':u"0.1"}
        PWidget.__init__(self,mngr,info)
        self.timer = e32.Ao_timer()

    def start(self):
        PWidget.start(self)
        self.timer.after(3,self.sampler)
        self.sampling = True

    def stop(self):
        PWidget.stop(self)
        self.sampling = False
        
    def sampler(self):
        if self.sampling:
            self.redraw()
            self.timer.after(3,self.sampler)
    
    def get_color(self):
        return (randint(0,255),randint(0,255),randint(0,255))
    
    def redraw(self): 
        self.canvas.clear(self.get_color())
        PWidget.redraw(self)
