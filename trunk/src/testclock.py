from pwcolor import *
from appuifw import *
from pwcanvas import *
from pwfill import *
from pwclock import *
import e32

class Teste(object):
    def __init__(self):
        app.screen = 'full'
        self.image = PWCanvas.new((240,320))
        self.image.clear()
        self.c1 = PWColor(GREEN)
        self.c2 = PWColor(YELLOW)
        self.image.round_rectangle((0,0, 240, 320), r=0, outline=None, fill=PWFill(self.c1, self.c2, mode=VERTICAL_GRADIENT))
        self.clock = PWClock(self.image)
        self.canvas = Canvas(redraw_callback = self.handle_redraw)
        app.exit_handler = self.close_app
        self.timer = e32.Ao_timer()
        
    def redraw(self):
        self.clock.redraw()
        self.canvas.blit(self.image)

    def handle_redraw(self, rect):
        self.redraw()
        
    def close_app(self):
        Teste.__lock.signal()

    def run(self):
        self.redraw()
        app.body = self.canvas
        while 1 == 1:
            self.redraw()
            self.timer.after(0.1)
        
t = Teste()
t.run()