from pwcanvas import *
from pwfill import *

__all__ = [ "PWidget" ]

class PWidget(object):
    """ Base class for widgets creation.
    """
    # Required information about the widget
    info_keys = ('name','description','author','version')
    
    def __init__(self,mngr,info,menu=[]):
        # All values in info must be filled        
        for k in self.info_keys:
            if not info.has_key(k):
                raise ValueError
        self.mngr = mngr
        self.info = info
        self.menu = menu
        self.size = self.mngr.get_size()
        self.canvas = PWCanvas.new(self.size)
            
    def bind(self,key,funct):
        """ Bind widget keys to callback functions.
        """
        self.mngr.bind(self,key,funct)
               
    def start(self):
        """ Widget startup code.
            This routine is called when the widget is created and added to
            widget manager list.
        """
        self.load()

    def stop(self):
        """ Widget shutdown code.
            This routine is called when the widget is removed from
            widget manager list.
        """
        self.save()

    def focus(self,received):
        """ Indicated when the widget receives (received = True) or
            loses (received = False) focus
        """
        return

    def resize(self,size):
        """ When size of manager canvas is changed, this routine is called.
            Widget must use this event to change its own size.
        """
        #raise NotImplementedError
        pass
    
    def redraw(self):
        """ Request an redraw from pwidget manager.
            Before calling this function, it is necessary to update
            the widget canvas.
        """
        self.mngr.redraw(self)

    def load(self):
        """ Load widget data from manager persitence.
        """
        self.mngr.load(self.info['name'])

    def save(self):
        """ Save widget data in manager persitence.
        """
        self.mngr.save(self.info['name'])

    def show_config(self,callback):
        """ Display the widget configuration dialog.
            When configuration is finished, call callback.
        """
        callback()
