from pwcolor import *
from appuifw import *
from graphics import Image
from random import randint
from pwprogressbar import *
import e32

class Teste(object):
    def __init__(self):
        app.screen = 'full'
        self.image = Image.new((240,320))
        self.image.clear()
        self.c1 = PWColor(GREEN)
        self.c2 = PWColor(YELLOW)
        self.c1.gradient(self.image, self.c2,(1,0))
        self.canvas = Canvas(redraw_callback = self.handle_redraw)
        app.menu = [(u"Progressbar", self.progress),(u"Exit", self.close_app)]
        app.exit_handler = self.close_app
        Teste.__lock = e32.Ao_lock()
        
    def redraw(self):
        self.canvas.blit(self.image)

    def handle_redraw(self, rect):
        self.redraw()
        
    def close_app(self):
        Teste.__lock.signal()
        
    def progress(self):
        p = PWProgressBar(self.image, 0, 100)
        for i in range(101):
            p.set_value(i)
            self.redraw()
        p.close()

    def run(self):
        self.redraw()
        app.body = self.canvas
        Teste.__lock.wait()

t = Teste()
t.run()