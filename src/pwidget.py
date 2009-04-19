import graphics

__all__ = [ "PWidget" ]

class PWidget(object):

    def __init__(self,mngr,title=u"",menu=[]):
        self.mngr = mngr
        self.menu = menu
        self.title = title
        self.name = u"Widget"
        self.size = self.mngr.get_size()
        self.canvas = graphics.Image.new(self.size)

    def get_name(self):
        """ Returns the plugin name. Must be a unicode string
        """
        raise NotImplementedError

    def run(self):
        """ Widget startup code. Call add_window to create the widget views
        """
        raise NotImplementedError
    
    def bind(self,key,funct):
        self.mngr.bind(self,key,funct)

    def update_canvas(self):
        """ Update canvas.
        """
        raise NotImplementedError

    def get_canvas(self):
        self.update_canvas()
        return self.canvas

    def redraw(self):
        self.mngr.redraw(self)

    def got_focus(self):
        self.mngr.set_menu(self.menu)
        self.mngr.set_title(self.title)

    def add_window(self,win):
        self.mngr.add_window(win)