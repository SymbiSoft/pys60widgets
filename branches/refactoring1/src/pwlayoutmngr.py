import os
from appuifw import note
import key_codes
from pwidgetcfg import *
from pwlayout import PWLayout

__all__ = [ "PWLayoutMngr" ]

class PWLayoutMngr(object):

    highlander = None
    base_name = "LAYOUT:"
    
    def __init__(self,pwapp,pwmngr):
        
        #Only one application is allowed.
        if self.highlander:
            raise RuntimeError
        
        self.pwapp = pwapp
        self.pwmngr = pwmngr
        self.size = self.pwapp.size       
        self.layouts = []
        self.active = 0
        self.buffer = self.pwapp.buffer
        self.canvas = self.pwapp.canvas
        self.background = self.pwapp.background        
        self.widgets = self.pwmngr.widgets
        self.pwapp.bind(self,key_codes.EKeyLeftArrow, lambda: self.dispatch_move(0))
        self.pwapp.bind(self,key_codes.EKeyRightArrow, lambda: self.dispatch_move(1))
        self.pwapp.bind(self,key_codes.EKeyUpArrow, lambda: self.dispatch_move(2))
        self.pwapp.bind(self,key_codes.EKeyDownArrow, lambda: self.dispatch_move(3))

    def get_size(self):
        return self.size

    def load(self,pwname):
        self.pwapp.load(self.base_name+pwname)

    def save(self,pwname):        
        self.pwapp.save(self.base_name+pwname)
        
    def load_layouts(self):
        try:
            files = os.listdir(PW_LAYOUTS_DIR)
        except:
            note(u"Impossible to open %s" % PW_LAYOUTS_DIR,"error")
            return
        
        [ self.try_import(f[:f.rfind(".py")]) for f in files if f.endswith(".py") ]

        self.layouts = []
        for layout in PWLayout.__subclasses__():
            self.layouts.append(layout(self)) # instanciate the layout

        for layout in self.layouts:
            print "Starting", layout.info
            layout.start()
               
    def try_import(self,module):
        try:
            __import__(module)
        except ImportError:
            note(u"Impossible to import layout %s" % module,"error")
            return False
        else:
            return True

    def dispatch_move(self,dir):
        if self.layouts:
            (self.layouts[self.active].left,
             self.layouts[self.active].right,
             self.layouts[self.active].up,
             self.layouts[self.active].down)(dir)

    def redraw(self,mode):
        if self.layouts:
            self.layouts[self.active].redraw(mode)