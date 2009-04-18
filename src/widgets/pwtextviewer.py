import e32
from pwidget import *
from pwcolor import *
from graphics import *

__all__ = ["PWTextViewer"]

class PWTextViewer(PWidget):

    def __init__(self, mngr, **attrs):
        self.name = u"TextViewer"
        self.check_default_values(attrs)
        PWidget.__init__(self,mngr,self.name)
    
    def check_default_values(self, attrs):
        """ Given some user attributes, define all attributes
        """
        self.attrs = {}

        self.def_attrs = { 'top':0,
                           'left':0,
                           'width':240,
                           'height':320,
                           'bg_color':PWColor(YELLOW),
                           'fg_color':PWColor(BLUE),
                           'scrollbar_color':PWColor(BLACK),
                           'scrollbar_width':5,
                           'font':u"dense",
                           'font_size':14,
                           'text':u"Lorem ipsum dolor sit."}

        for k in self.def_attrs.keys():
            if attrs.has_key(k):
                self.attrs[k] = attrs[k]
            else:
                self.attrs[k] = self.def_attrs[k]
        
        self.set_text(self.attrs['text'])

    def get_name(self):
        return self.name

    def run(self):
        self.add_window(self)
    
    def draw_background(self):
        self.canvas.clear(self.attrs['bg_color'].get_color())
    
    def draw_scrollbar(self):
        pass
    
    def draw_text(self):
        #wrap lines
        self.canvas.text((0,self.attrs['font_size']),
                  self.text, 
                  fill = self.attrs['fg_color'].get_color(), 
                  font = (self.attrs['font'],self.attrs['font_size'],FONT_ANTIALIAS))
    
    def text_wrap(self):
        pass
    
    def set_text(self, text):
        self.text = text
        #todo wrap text
        """if self.canvas:
            self.update_canvas()"""

    def update_canvas(self):
        self.draw_background()
        self.draw_text()
