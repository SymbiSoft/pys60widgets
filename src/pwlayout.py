__all__ = [ "PWLayout" ]

class PWLayout(object):
    """ Base class for layouts creation.
    """
    # Required information about the widget
    info_keys = ('name','description','author','version')
    
    def __init__(self,mngr,info,active=0):
        # All values in info must be filled        
        for k in self.info_keys:
            if not info.has_key(k):
                raise ValueError
            
        self.mngr = mngr
        self.info = info        
        self.buffer = self.mngr.buffer
        self.canvas = self.mngr.canvas
        self.widgets = self.mngr.widgets
        self.background = self.mngr.background
        self.size = self.canvas.size
        self.num_widgets = len(self.widgets)
        self.active = active

    def get_canvas(self,index):
        self.widgets[index].canvas
    
    def set_active(active=0):
        self.active = active

    def get_active(self):
        return self.active
       
    def redraw(self,thumb_mode): 
        """ 
        """
        raise NotImplementedError
    
    def next(self,thumb_mode): 
        """ 
        """
        raise NotImplementedError
    
    def prev(self,thumb_mode): 
        """ 
        """
        raise NotImplementedError
    
    def up(self,thumb_mode): 
        """ 
        """
        raise NotImplementedError
    
    def down(self,thumb_mode): 
        """ 
        """
        raise NotImplementedError
    
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

    def resize(self,size):
        """ When size of manager canvas is changed, this routine is called.
            Widget must use this event to change its own size.
        """
        #raise NotImplementedError
        pass
    
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

        
