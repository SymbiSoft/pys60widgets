import os
from appuifw import note
from pwidgetcfg import *
from pwidget import PWidget

__all__ = [ "PWidgetMngr" ]

class PWidgetMngr(object):

    highlander = None
    base_name = "WIDGET:"
    
    def __init__(self,pwapp):

        #Only one application is allowed.
        if self.highlander:
            raise RuntimeError

        self.pwapp = pwapp
        self.size = self.pwapp.size
        self.widgets = []

    def get_size(self):
        return self.size

    def load(self,pwname):
        self.pwapp.load(self.base_name+pwname)

    def save(self,pwname):        
        self.pwapp.save(self.base_name+pwname)
        
    def load_widgets(self):
        try:
            files = os.listdir(PW_WIDGETS_DIR)
        except:
            note(u"Impossible to open %s" % PW_WIDGETS_DIR,"error")
            return
        
        [ self.try_import(f[:f.rfind(".py")]) for f in files if f.endswith(".py") ]

        self.widgets = []               
        for widget in PWidget.__subclasses__():
            self.widgets.append(widget(self)) # instanciate the widget
                
        for widget in self.widgets:
            print "Starting", widget.info            
            widget.start()
               
    def try_import(self,module):            
        try:
            __import__(module)
        except ImportError:
            note(u"Impossible to import widget %s" % module,"error")
            return False
        else:
            return True

    def bind(self,win,key,funct):
        self.pwapp.bind(win,key,funct)
        
    def redraw(self,win):
        if not self.pwapp.is_thumb_mode():
            self.pwapp.buffer.blit(win.canvas)
            self.pwapp.redraw()
