from pwcolor import *
from appuifw import *
from pwcanvas import *
from pwfill import *
from random import randint
from pwprogressbar import *
import e32

class Teste(object):
    def __init__(self):
        app.screen = 'full'
        self.image = PWCanvas.new((240,320))
        self.image.clear()
        self.c1 = PWColor(GREEN)
        self.c2 = PWColor(YELLOW)
        self.c1.gradient(self.image, self.c2,(1,0))
        self.image.round_rectangle((10,10, 100, 200), r=10, outline=(0,0,255), fill=PWFill(PWColor(BLUE), PWColor(RED), mode=VERTICAL_GRADIENT), opacity=1)
        self.image.round_rectangle((110,10, 210, 200), r=10, outline=None, fill=(0,0,255), opacity=0.2)
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