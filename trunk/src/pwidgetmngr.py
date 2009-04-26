import os
import sys
import sysinfo
import e32
import key_codes
from pwcanvas import *
from pwidgetcfg import *
from appuifw import *
import graphics
from pwidget import PWidget
import time
from pwlayout import PWLayout3x2

__all__ = [ "PWM" ]

class PWidgetMngr(object):

    """
    Different view modes for PyWidgets:

    * Thumbnail: all widgets in a thumbnail view
    * Full screen: just one widget in full screen but with key bindings for thumbnail
    * Widget: just one widget in full screen but with key bindings for widget
    """
    VIEW_MODE_THUMBNAIL = 0
    VIEW_MODE_FULL_SCREEN = 1
    VIEW_MODE_WIDGET = 2

    DOUBLE_CLICK_TIME = 0.5    
    
    def __init__(self):
        app.screen = "full"
        self.view_mode = self.VIEW_MODE_THUMBNAIL
        self.layouts = None
        self.size = sysinfo.display_pixels()
        self.window_list = []
        self.bind_list = {}
        self.background = None
        #self.active_focus = 0
        self.drawing_in_progress = False
        self.effect_in_progress = False
        self.widgets = {}         
        self.canvas = Canvas(redraw_callback = self.redraw,
                             event_callback = self.event,
                             resize_callback = self.resize)
        self.size = sysinfo.display_pixels()
        self.double_buffer = PWCanvas.new(self.size)
        app.body = self.canvas
        self.menu = [(u"Exit",self.close_app) ]
        app.menu = self.menu
        self.lock = e32.Ao_lock()
        self.bind(self,key_codes.EKeyLeftArrow, self.show_prev_widget)
        self.bind(self,key_codes.EKeyRightArrow, self.show_next_widget)
        self.bind(self,key_codes.EKeySelect, self.change_view_mode)
        app.exit_handler = self.close_app
        self.tmp_debug = 0
        self.select_double_click = time.time()
        self.load_widgets()
        wlst=[w.get_canvas() for w in self.window_list]
        self.layouts = [PWLayout3x2(self.double_buffer,self.canvas,self.background,wlst)]
        self.active_layout = 0
        self.bind_enabled = True
    
    def get_size(self):
        return self.size
    
    def close_app(self):
        # TODO: call all widgets saying that the app is closing
        self.lock.signal()
        app.set_tabs( [], None )
        app.menu = []
        app.body = None
        app.set_exit()

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
        if not self.bind_enabled:
            return        
        for updt in self.bind_list[key].values():
            if self.view_mode == self.VIEW_MODE_WIDGET:
                if updt['win'] != self:
                    updt['cbk']()
            else:
                if updt['win'] == self:
                    updt['cbk']()
            
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

    def redraw_widget(self,win):
        """ Redraw widget if possible. Playground/effect has priority over this call.
            However, when in widget mode, playground and effects are disabled and all
            redraws from widget are performed.
            
            TODO: some cache here ?
        """
        self.redraw()

    def manager_is_busy(self):
        return (self.drawing_in_progress or self.effect_in_progress)

    def redraw(self,rect=None):
        if self.layouts:
            self.bind_enabled = False
            self.drawing_in_progress = True
            thumb_mode = self.view_mode == self.VIEW_MODE_THUMBNAIL
            self.layouts[self.active_layout].redraw(thumb_mode)
            self.drawing_in_progress = False
            self.bind_enabled = True
       
    def show_next_widget(self):
        self.effect_in_progress = True
        thumb_mode = self.view_mode == self.VIEW_MODE_THUMBNAIL
        self.layouts[self.active_layout].next(thumb_mode)
        self.effect_in_progress = False
        self.redraw()

    def show_prev_widget(self):
        self.effect_in_progress = True
        thumb_mode = self.view_mode == self.VIEW_MODE_THUMBNAIL
        self.layouts[self.active_layout].prev(thumb_mode)
        self.effect_in_progress = False
        self.redraw()     

    def set_menu(self,menu):
        """ Merge window menu with PWidgetMngr menu
        """
        m = menu + [(u"PyWidgets",((u"Playground",self.show_thumbnail_mode),
                                   (u"Next",self.show_next_widget),
                                   (u"Prev",self.show_prev_widget)                                   
                                   ))] + self.menu
        app.menu = m
    
    def change_view_mode(self):
        """ If in thumbnail mode, show widget in full screen (one click).
            If already in full screen mode, go to widget view with double click
            or to back to thumbnail with single click.
        """
        if not self.window_list:
            return
        
        double_click = False
        tm = time.time()
        if (tm - self.select_double_click) < self.DOUBLE_CLICK_TIME:
            double_click = True
        self.select_double_click = tm
            
        if self.view_mode == self.VIEW_MODE_THUMBNAIL:
            self.view_mode = self.VIEW_MODE_FULL_SCREEN
        elif self.view_mode == self.VIEW_MODE_FULL_SCREEN:
            if double_click:
                self.view_mode = self.VIEW_MODE_WIDGET
            else:
                self.view_mode = self.VIEW_MODE_THUMBNAIL
        else:
            print "Not expected case for change_view_mode"
                
        if self.view_mode == self.VIEW_MODE_WIDGET:
            a = self.layouts[self.active_layout].get_active()
            self.window_list[a].got_focus()

        self.redraw()
            
    def show_thumbnail_mode(self):
        app.menu = self.menu
        self.view_mode = self.VIEW_MODE_THUMBNAIL
        self.redraw()
        
    def set_title(self,title):
        app.title = title
        
    def run(self):
        self.redraw()
        self.lock.wait()

    def event(self,ev):
        pass

    def resize(self,rect):
        pass
    
PWM = PWidgetMngr()
PWM.run()

"""
    def layout_4x3(self,order):
        ws = 10
        ww = (self.size[0]-ws)/4 - ws
        wh = (self.size[1]-ws)/3 - ws
        y = ws
        n = 0
        for lin in range(3):
            x = ws
            for col in range(4):
                # focus
                if n == self.active_focus:
                    self.double_buffer.rectangle((x-2,y-2,x+ww+2,y+wh+2),
                                          fill=(255,0,0),
                                          outline=(255,0,0))
                if  n >=  len(self.window_list) or n >= 12:
                    break
                w = self.window_list[order[n]]
                # TODO: resize is generating exception ... async mode necessary
                try:
                    screen_aux = w.get_canvas().resize((ww,wh))
                    self.double_buffer.blit(screen_aux,target=(x,y),source=((0,0),(ww,wh)))
                except:
                    print "error: canvas resize"
                x += ww + ws
                n += 1
            y += wh + ws
"""