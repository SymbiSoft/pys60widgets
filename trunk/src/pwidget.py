import graphics

__all__ = [ "PWidget" ]

class PWidget(object):

    def __init__(self,mngr,title=u"",menu=[],size=None):
        self.mngr = mngr
        self.menu = menu
        self.title = title
        self.name = u"Widget"
        self.size = (0,0)
        if not size:
            size = self.mngr.get_size()
        self.set_size(size)

    def set_size(self,size):
        if self.size != size:
            self.size = size
            # Is explicit del for previous canvas necessary ?
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
        """ Return the current canvas image to manager
        """
        return self.canvas

    def redraw(self):
        """ Request an redraw from pwidget manager. update_canvas is called before.
        """
        self.update_canvas()
        self.mngr.redraw_widget(self)

    def got_focus(self):
        self.mngr.set_menu(self.menu)
        self.mngr.set_title(self.title)

    def add_window(self,win):
        self.mngr.add_window(win)