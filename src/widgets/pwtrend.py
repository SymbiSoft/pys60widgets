import e32
from pwidget import *
from random import randint

__all__ = [ "PWTrend" ]

class PWTrend(PWidget):
    
    BLACK = (0,0,0)
    DARK_GREEN = (0,102,0)
    BLUE = (51,204,255)
    YELLOW = (255,255,102)

    def __init__(self,mngr,**attrs):
        info = {'name':u"Trend",
                'description':u"Trend demo Python for S60 widgets",
                'author':u"Marcelo Barros",
                'version':u"0.1"}
        self.check_default_values(attrs)
        menu = [(u"Start",self.start_trend),
                (u"Stop",self.stop_trend)]
        PWidget.__init__(self,mngr,info,menu)
        self.samples = []
        self.sampling = False
        self.timer = e32.Ao_timer()
        self.canvas.clear( self.BLACK )
        self.draw_grid()
      
    def start_trend(self):
        if not self.sampling:
            self.timer.after(self.attrs['sampling_time'],self.sampler)
            self.sampling = True

    def stop_trend(self):
        if self.sampling:
            self.sampling = False
            
    def sampler(self):
        if self.sampling:
            b = self.attrs['sampler']()
            self.samples.insert( 0, b )
            self.redraw()
            self.timer.after(self.attrs['sampling_time'],self.sampler)
        
    def default_sampler(self):
        return randint(0,100)
        
    def check_default_values(self,attrs):
        """ Given some user attributes, define all ptrend attributes
        """
        self.attrs = {}

        self.def_attrs = { 'min':0,
                           'max':100,
                           'sampling_time':2,
                           'sampler':self.default_sampler }
            
        for k in self.def_attrs.keys():
            if attrs.has_key(k):
                self.attrs[k] = attrs[k]
            else:
                self.attrs[k] = self.def_attrs[k]
        
    def draw_grid(self):
        w,h = self.size
        step = 10
        for x in range(0,w,step):
            self.canvas.line( (x,0,x,h), outline = self.DARK_GREEN )
        for y in range(0,h,step):
            self.canvas.line( (0,y,w,y), outline = self.DARK_GREEN )
        self.canvas.line( (w-1,0,w-1,h), outline = self.DARK_GREEN )
        self.canvas.line( (0,h-1,w,h-1), outline = self.DARK_GREEN )

    def draw_points(self):
        ns = len(self.samples)
        h = self.size[1] - 1
        minv = self.attrs['min']
        maxv = self.attrs['max']
        step = 2
        if ns >= 2:
            line_bar = []
            n = int( self.size[0] / step )
            for i in range(ns):
                ybar = h  - int(h*(self.samples[i]-minv)/(maxv-minv))
                xbar = (n-i)*step
                if xbar < 0: # only points that fit into screen
                    break
                line_bar.append( (xbar, ybar) )
                
            self.draw_lines(line_bar,self.BLUE)

    def draw_lines(self,lines,color_name):
        for p in range(len(lines) - 1):
            coord = ( lines[p][0], lines[p][1], lines[p+1][0], lines[p+1][1] )
            self.canvas.line( coord, outline = color_name )
        
    def redraw(self):
        self.canvas.clear( self.BLACK )
        self.draw_grid()
        self.draw_points()
        PWidget.redraw(self)

