import os
import sys
import sysinfo
import e32
import key_codes
from pwidgetcfg import *
from appuifw import *
import graphics
from pwidget import PWidget

__all__ = [ "PWM" ]

class PWidgetMngr(object):
    
    def __init__(self):
        app.screen = "full"
        self.layouts = { u"4x3":self.layout_4x3 }
        self.canvas_ctrl = None
        self.size = sysinfo.display_pixels()
        self.canvas = None
        self.window_list = []
        self.active_win = None
        self.bind_list = {}
        self.background = None
        self.active_focus = 0
        self.widgets = {}         
        self.canvas_ctrl = Canvas(redraw_callback = self.redraw,
                                  event_callback = self.event,
                                  resize_callback = self.resize)
        self.size = sysinfo.display_pixels()
        self.canvas = graphics.Image.new(self.size)
        app.body = self.canvas_ctrl
        self.menu = [ (u"Exit",self.close_app) ]
        app.menu = self.menu
        self.lock = e32.Ao_lock()
        self.bind(self,key_codes.EKeyLeftArrow, self.focus_next)
        self.bind(self,key_codes.EKeyRightArrow, self.focus_prev)
        app.exit_handler = self.close_app
        self.load_widgets()

    def get_size(self):
        return self.size
    
    def close_app(self):
        # TODO: call all widgets saying that the app is closing
        self.lock.signal()
        app.set_tabs( [], None )
        app.menu = []
        app.body = None
        app.set_exit()

    def set_background(self,background):    
        if background:
            self.background = background

    def bind(self,win,key,funct):
        if funct is None:
            try:
                del self.bind_list[key][win]
            except:
                pass # forgive me, Zen of Python
        else:
            if not self.bind_list.has_key(key):
                self.bind_list[key] = {}
            self.bind_list[key][win] = {'win':win,'cbk':funct}
            self.canvas_ctrl.bind(key,lambda: self.bind_dispatch(key))

    def bind_dispatch(self,key):
        for updt in self.bind_list[key].values():
            updt['cbk']()
       #     if updt['widget']:
       #         w=updt['win']
       #         self.canvas.blit(w.get_canvas(),target=w.get_position(),source=((0,0),w.get_size()))
       # if updt['widget']:                
       #     self.update_canvas()
            
    def load_widgets(self):
        try:
            files = os.listdir(PW_WIDGETS_DIR)
        except:
            note(u"Impossible to open %s" % PW_WIDGETS_DIR,"error")
            return
        
        [ self.try_import(f[:f.rfind(".py")]) for f in files if f.endswith(".py") ]

        self.widgets = {}        
        for widget in PWidget.__subclasses__():
            if widget not in self.widgets:
                # instanciate and add the widget to the interface
                self.widgets[widget] = widget(self)
                self.widgets[widget].run()
               
    def try_import(self,module):            
        try:
            __import__(module)
        except:
            return False
        else:
            return True

    def add_window(self,win):
        self.window_list.append(win)
        self.active_focus = len(self.window_list) - 1

    def update_canvas(self):
        #self.draw_focus()
        self.canvas_ctrl.blit(self.canvas)
        
    def redraw(self,rect=None):
        if self.background:
            self.canvas.blit(self.background)
        else:
            self.canvas.clear((255,255,255))
        # generating a repaint respecting focus order
        #nw = len(self.window_list)
        #order = [ c%nw for c in range(self.active_focus+1,self.active_focus+1+nw) ]
        if self.window_list:
            self.layouts[u"4x3"](range(len(self.window_list)))
        self.update_canvas()
        
    def layout_4x3(self,order):
        """
        """
        ws = 5
        ww = (self.size[0]-ws)/4 - ws
        wh = (self.size[1]-ws)/3 - ws
        y = ws
        n = 0
        for col in range(4):
            x = ws
            for lin in range(3):
                # focus
                if n == self.active_focus:
                    self.canvas.rectangle((x-2,y-2,x+ww+2,y+wh+2),
                                          fill=(255,0,0),
                                          outline=(255,0,0))
                if  n >=  len(self.window_list):
                    break
                w = self.window_list[order[n]]
                self.canvas.blit(w.get_canvas(),target=(x,y),source=((0,0),(ww,wh)))
                x += ww + ws
                n += 1
            y += wh + ws

    #def draw_focus(self):
    #    pass
        """
        if self.window_list:
            w = self.window_list[self.active_focus]
            p = list(w.get_position()[0:2])
            p += [p[0]+5,p[1]+5]
            self.canvas.rectangle(p,fill=(255,0,0),outline=(255,0,0))
            w.got_focus()
        """
        
    def event(self,ev):
        pass

    def resize(self,rect):
        pass

    def focus_next(self):
        self.active_focus = (self.active_focus + 1) % len(self.window_list)
        self.redraw()
        
    def focus_prev(self):
        self.active_focus = (self.active_focus - 1) % len(self.window_list)
        self.redraw()

    def set_menu(self,menu):
        """ Merge window menu with PWidgetMngr menu
        """
        m = menu + self.menu
        app.menu = m

    def set_title(self,title):
        app.title = title
        
    def run(self):
        self.redraw()
        self.lock.wait()

PWM = PWidgetMngr()
PWM.run()