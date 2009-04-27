from appuifw import *
import sysinfo
import e32
import key_codes
from pwcanvas import *
from pwidgetcfg import *
from pwidgetmngr import *
from pwlayoutmngr import *
from pwidgetconst import *

__all__ = [ "PWidgetApp" ]

class PWidgetApp(object):
    def __init__(self):
        self.lock = e32.Ao_lock()
        app.screen = "full"
        self.view_mode = VIEW_MODE_THUMBNAIL
        self.size = sysinfo.display_pixels()
        self.bind_list = {}
        self.canvas = Canvas(redraw_callback = self.redraw,
                             event_callback = self.event,
                             resize_callback = self.resize)
        self.buffer = PWCanvas.new(self.size)
        self.background = None
        self.menu = [(u"Open Widget",self.open_widget),
                     (u"Setup",self.show_setup),
                     (u"About",self.show_about),
                     (u"Exit",self.close_app) ]
        self.pwmngr = PWidgetMngr(self)
        self.pwlmngr = PWLayoutMngr(self,self.pwmngr)
        app.body = self.canvas
        app.menu = self.menu
        app.exit_handler = self.close_app
        self.bind(self,key_codes.EKeySelect, self.change_view_mode)
    
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
            self.canvas.bind(key,lambda: self.bind_dispatch(key))

    def bind_dispatch(self,key):
        """ Dispatch callbacks for key according to view mode.
        """    
        for updt in self.bind_list[key].values():
            if self.view_mode == VIEW_MODE_WIDGET:
                if updt['win'] != self:
                    updt['cbk']()
            else:
                if updt['win'] == self:
                    updt['cbk']()
                
    def open_widget(self):
        self.view_mode = VIEW_MODE_WIDGET
        #self.pwmngr.focus(True)
        self.redraw()
        
    def change_view_mode(self):
        if self.view_mode == VIEW_MODE_THUMBNAIL:
            self.view_mode = VIEW_MODE_FULL_SCREEN
        elif self.view_mode == VIEW_MODE_FULL_SCREEN:
            self.view_mode = VIEW_MODE_THUMBNAIL
        self.redraw()
            
    def show_setup(self):
        pass
    
    def show_about(self):
        pass

    def load(self,key): pass
    def save(self,key): pass

    def redraw(self,rect=None):
        self.pwlmngr.redraw(self.is_thumb_mode())

    def is_thumb_mode(self):
        return self.view_mode == VIEW_MODE_THUMBNAIL
    
    def run(self):
        self.pwmngr.load_widgets()
        self.pwlmngr.load_layouts()
        self.redraw()
        self.lock.wait()

    def event(self,ev):
        pass

    def resize(self,rect):
        pass

    def close_app(self):
        # TODO: call all widgets saying that the app is closing
        self.lock.signal()
        app.set_tabs( [], None )
        app.menu = []
        app.body = None
        app.set_exit()

#if __name__ == "__main__":
pwa = PWidgetApp()
pwa.run()
    