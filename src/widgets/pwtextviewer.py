import e32
import re
import key_codes
from pwidget import *
from pwcolor import *
from graphics import *
from appuifw import available_fonts, popup_menu

__all__ = ["PWTextViewer"]

LIPSUM = u"""Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin feugiat, mi id consectetur cursus, sem diam pretium nibh, et tristique libero erat luctus odio. Morbi dapibus mauris sit amet lectus.

Ut est eros, aliquam ut, dapibus sed, vehicula at, nisl. Ut turpis dui, consequat eget, congue et, consequat eu, massa. In hac habitasse platea dictumst. Pellentesque mi felis, hendrerit id, imperdiet ut, venenatis nec, velit. 

Suspendisse et tellus ut mauris bibendum tempus. Nullam molestie. Etiam lobortis. Maecenas sit amet nunc. Vivamus diam massa, tincidunt id, iaculis nec, dignissim quis, massa. Pellentesque tempor leo rutrum neque. Donec sit amet nisi a dui tristique eleifend. Nunc in mauris sed enim pulvinar iaculis. Vestibulum dui turpis, accumsan et, fermentum vitae, aliquam vitae, eros.

Sed mattis nisi at orci. Etiam ante orci, ornare sit amet, placerat feugiat, venenatis eu, dui. Sed pretium blandit ante. Curabitur feugiat orci condimentum enim. Quisque bibendum nulla eu massa. Maecenas tempor lobortis libero. Etiam lorem sapien, imperdiet at, vestibulum nec, molestie nec, dui. Etiam feugiat sem id augue ullamcorper luctus. Pellentesque gravida dictum dui. Pellentesque sit amet orci. Maecenas elit. Suspendisse cursus accumsan dui. Vestibulum mi magna, volutpat ut, ornare quis, vulputate sit amet, mi. Aenean a lectus sit amet ante malesuada egestas.

Donec interdum. Nam urna nibh, auctor non, dictum eget, convallis eget, erat. Duis lorem arcu, varius nec, auctor ut, lobortis sit amet, leo. Quisque sodales egestas metus. Pellentesque mattis risus vel velit. Praesent porta turpis in ipsum. In sed quam et libero suscipit vestibulum. Donec ut sem. Nullam at mauris vel eros porttitor condimentum. Vestibulum vitae nibh et neque placerat bibendum. Maecenas ultricies orci ut ipsum. In hendrerit massa at lorem. Nunc fermentum dapibus felis. Nunc mauris. Ut vitae sem quis ligula malesuada congue. Donec luctus mauris sit amet urna. Morbi odio dolor, tincidunt at, ultrices ac, tincidunt at, urna. Integer et justo. Nulla enim elit, ornare nec, lacinia id, auctor sed, tellus.

Mauris enim diam, lobortis at, eleifend malesuada, sodales sit amet, quam. Pellentesque porta leo nec arcu. Aliquam eget sapien quis urna fermentum ornare. Fusce posuere, est eu vehicula bibendum, odio tellus lobortis nunc, quis euismod justo ante a magna. Nulla nec odio. Morbi ac urna ut erat placerat mollis. Vestibulum sed sem et nisl dapibus fringilla. Nam mattis ante. In rutrum blandit eros. Pellentesque ut sem. Aliquam facilisis. Praesent leo erat, posuere eu, malesuada in, tincidunt sed, leo. Curabitur vitae nulla. Sed scelerisque vehicula est.

Quisque nec diam. Vestibulum hendrerit. Nunc lacus erat, convallis sed, malesuada vel, interdum porttitor, diam. Curabitur viverra, tortor elementum placerat porta, turpis dolor mattis magna, vel tempor arcu metus in tortor. Maecenas ut dolor. Aliquam erat volutpat. Nullam a risus sed diam pellentesque feugiat. Pellentesque non turpis id justo malesuada consectetur. Integer nulla. Donec semper odio euismod nulla tincidunt varius. Suspendisse non lacus sit amet orci rutrum vulputate. Fusce sit amet urna quis nibh elementum sagittis. Proin blandit venenatis urna. Donec iaculis odio eget est. Sed eleifend semper massa. Nulla fringilla ligula at eros. Mauris lobortis sollicitudin odio. Etiam nunc. 
"""

class PWTextViewer(PWidget):

    def __init__(self, mngr, **attrs):
        self.name = u"TextViewer"
        menu = [(u"Font", self.change_font), (u"Colors", self.change_color)]
        PWidget.__init__(self,mngr,self.name, menu)
        #test gradient colors
        c1 = PWColor([0,99,249,255])
        c2 = PWColor([0,49,124,255])
        self.gradient = Image.new((self.canvas.size[0],self.canvas.size[1]))
        c1.gradient(self.gradient, c2, (1,0))
        #end test gradient
        self.check_default_values(attrs)
        self.cursor = [0,0]
        self.set_binds(True)

    def check_default_values(self, attrs):
        """ Given some user attributes, define all attributes
        """
        self.attrs = {}
        
        self.def_attrs = { 'top':0,
                           'left':0,
                           'width':240,
                           'height':320,
                           'bg_color':PWColor([0,49,124,255]),
                           'fg_color':PWColor([255,255,255,255]),
                           'scrollbar_color':PWColor([128,128,128,255]),
                           'scrollbar_width':6,
                           'font':u"dense",
                           'font_size':10,
                           'margin_top':3,
                           'margin_left':3,
                           'margin_bottom':0,
                           'margin_right':3,
                           'text': LIPSUM }

        for k in self.def_attrs.keys():
            if attrs.has_key(k):
                self.attrs[k] = attrs[k]
            else:
                self.attrs[k] = self.def_attrs[k]
        
        self.set_text(self.attrs['text'])
        
        white = PWColor(WHITE)
        self.handle_width = self.attrs['scrollbar_width']
        self.glow_width   = int(self.handle_width / 2)
        self.shadow_width = self.handle_width - self.glow_width
        self.shadow_color = PWColor(self.attrs['scrollbar_color'].color)
        self.glow_color   = PWColor(self.shadow_color.color)
        self.glow_color.combine(white, 0.3)
        
        #Cursor uses the inverse colors fg => bg
        self.cursor_fg_color = PWColor(self.attrs['bg_color'].color)
        self.cursor_bg_color = PWColor(self.attrs['fg_color'].color)
        self.cursor_glow = PWColor(self.cursor_bg_color.color)
        self.cursor_glow.combine(white, 0.3)
    
    def set_binds(self,val):
        """ Enable or disable bindings
        """
        if val:
            self.bind(key_codes.EKeyUpArrow, self.up_key)
            self.bind(key_codes.EKeyDownArrow, self.down_key)
            self.bind(key_codes.EKeyLeftArrow, self.left_key)
            self.bind(key_codes.EKeyRightArrow, self.right_key)
        else:
            self.bind(key_codes.EKeyUpArrow, None)
            self.bind(key_codes.EKeyDownArrow, None)
            self.bind(key_codes.EKeyLeftArrow, None)
            self.bind(key_codes.EKeyRightArrow, None)

    def up_key(self):
        if self.cursor[0] > 0:
            self.cursor[0] -= 1
            if len(self.lines[self.cursor[0]]) == 0:
                self.cursor[1] = 0
            elif self.cursor[1] >= len(self.lines[self.cursor[0]]):
                self.cursor[1] = len(self.lines[self.cursor[0]]) - 1
        self.redraw_textview()

    def down_key(self):
        if self.cursor[0] < len(self.lines) - 1:
            self.cursor[0] += 1
            if len(self.lines[self.cursor[0]]) == 0:
                self.cursor[1] = 0
            elif self.cursor[1] >= len(self.lines[self.cursor[0]]):
                self.cursor[1] = len(self.lines[self.cursor[0]]) - 1
        self.redraw_textview()

    def left_key(self):
        if self.cursor[1] > 0:
            self.cursor[1] -= 1
        elif self.cursor[0] > 0:
            self.cursor[0] -= 1
            if len(self.lines[self.cursor[0]]) == 0:
                self.cursor[1] = 0
            else:
                self.cursor[1] = len(self.lines[self.cursor[0]]) - 1
        self.redraw_textview()

    def right_key(self):
        if self.cursor[1] < len(self.lines[self.cursor[0]]) - 1:
            self.cursor[1] += 1
        elif self.cursor[0] < len(self.lines) - 1:
            self.cursor[0] += 1
            self.cursor[1] = 0
        self.redraw_textview()

    def get_name(self):
        return self.name

    def run(self):
        self.add_window(self)
        
    def draw_cursor(self):
        if len(self.lines[self.cursor[0]]) > 0:
            sleft = self.lines[self.cursor[0]][:self.cursor[1]]
            c = self.lines[self.cursor[0]][self.cursor[1]]
            
            lrect = self.canvas.measure_text(sleft, font=(self.attrs['font'],
                                                        self.attrs['font_size'],
                                                        FONT_ANTIALIAS))[0]
            crect = self.canvas.measure_text(c, font=(self.attrs['font'],
                                                        self.attrs['font_size'],
                                                        FONT_ANTIALIAS))[0]
            
            w = crect[2]
            h = self.attrs['font_size']
            x = self.attrs['margin_left'] + lrect[2] + 1
            y = self.attrs['margin_top'] + (self.cursor[0] + 1) * self.attrs['font_size']
            
            self.canvas.rectangle((x-1,y-h-1,x+w-1,y+1),
                                    outline=None,
                                    fill=self.cursor_bg_color.get_color())
            self.canvas.text((x,y),
                                c, fill = self.cursor_fg_color.get_color(), 
                                   font = (self.attrs['font'],
                                   self.attrs['font_size'],FONT_ANTIALIAS))
        else:
            self.canvas.rectangle((self.attrs['margin_left'],
                                    self.attrs['margin_top'] + (self.cursor[0] + 1) * self.attrs['font_size'] - self.attrs['font_size'],
                                    self.attrs['margin_left']+ self.attrs['font_size'],
                                    self.attrs['margin_top'] + (self.cursor[0] + 1) * self.attrs['font_size']),
                                    outline=None,
                                    fill=self.cursor_bg_color.get_color())

    def draw_scrollbar(self):
        a = self.attrs
        hw = self.handle_width
        sc = self.shadow_color
        gc = self.glow_color
        sw = self.shadow_width
        gw = self.glow_width
        #Draw scrollbar BG
        self.canvas.rectangle((a['width']-hw,a['top'],a['width'],a['height']),
                                outline=sc.get_color(),
                                fill=None)
        #Draw scrollbar handle - first the shadow
        self.canvas.rectangle((a['width']-sw,a['top'],a['width'],a['top']+30),
                                outline=sc.get_color(),
                                fill=sc.get_color())
        #and now the glow
        self.canvas.rectangle((a['width']-hw,a['top'],a['width']-hw+gw,a['top']+30),
                                outline=gc.get_color(),
                                fill=gc.get_color())
    
    def draw_background(self):
        #self.canvas.clear(self.attrs['bg_color'].get_color())
        self.canvas.blit(self.gradient)

    def draw_text(self):
        i = 1;
        for line in self.lines:
            line = line.strip(u"\n")
            self.canvas.text((self.attrs['margin_left'], self.attrs['margin_top'] + i * self.attrs['font_size']),
                                line, 
                                fill = self.attrs['fg_color'].get_color(), 
                                font = (self.attrs['font'],self.attrs['font_size'],FONT_ANTIALIAS))
            i += 1

    # modified version of TextRenderer.chop 
    # http://discussion.forum.nokia.com/forum/showthread.php?t=124666
    def text_wrap(self):
        self.lines = []
        paragraphs = self.text.splitlines(True)
        width = self.attrs['width'] - self.attrs['scrollbar_width'] - self.attrs['margin_left'] - self.attrs['margin_right']
        for text_left in paragraphs:
            while len(text_left) > 0:
                bounding, to_right, fits = self.canvas.measure_text(text_left,
                                                             font=(self.attrs['font'],
                                                                    self.attrs['font_size'],
                                                                    FONT_ANTIALIAS),
                                                             maxwidth=width,
                                                             maxadvance=width)
                if fits <= 0:
                    self.lines.append(text_left)
                    break
                    
                slice = text_left[0:fits]
                adjust = 0 # (preserve or not whitespaces at the end of the row)
                if len(slice) < len(text_left):
                    # find the separator character closest to the right
                    rindex = -1
                    idx = slice.rfind(u' ')
                    if idx > rindex:
                        rindex = idx
                    if rindex > 0:
                        if slice[rindex] == u' ':
                            adjust = 1
                        slice = slice[0:rindex]
                
                self.lines.append(slice.strip(u"\n"))
                text_left = text_left[len(slice)+adjust:]

    def set_text(self, text):
        self.text = text
        self.text_wrap()
    
    def set_font(self, font, size):
        self.attr['font'] = font
        self.attr['font_size'] = size
    
    def change_font(self):
        fonts = [u"normal", u"dense", u"title", u"symbol", u"legend", u"annotation"] + available_fonts()
        f = popup_menu(fonts,u"Font:")
        if f is not None:
            self.attrs['font']= fonts[f]
            self.text_wrap()
            sizes = [u"8", u"10", u"12", u"14", u"16", u"18", u"20", u"22", u"24", u"30", u"32"]
            s = popup_menu(sizes, u"Size:")
            if s is not None:
                self.attrs['font_size'] = int(sizes[s])
                self.text_wrap()
            self.redraw_textview()

    def change_color(self):
        scolors = [u"White",u"Black",u"Red",u"Green",u"Blue",u"Yellow",u"Magenta",u"Cyan",u"Gray"]
        colors = [WHITE,BLACK,RED,GREEN,BLUE,YELLOW,MAGENTA,CYAN,GRAY]
        c = popup_menu(scolors,u"Background:")
        if c is not None:
            self.attrs['bg_color'] = PWColor(colors[c])
        c = popup_menu(scolors,u"Foreground:")
        if c is not None:
            self.attrs['fg_color'] = PWColor(colors[c])
        self.redraw_textview()
    
    def redraw_textview(self):
        self.draw_background()
        self.draw_text()
        self.draw_cursor()
        self.draw_scrollbar()
        self.redraw()

    
    def update_canvas(self):
        self.redraw_textview()