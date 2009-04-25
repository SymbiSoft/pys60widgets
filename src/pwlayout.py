import graphics

__all__ = [ "PWLayout", "PWLayout3x2" ]

class PWLayout(object):

    def __init__(self,double_buffer,canvas,background=None,widgets=[],active=0):
        self.name = u""
        self.double_buffer = double_buffer
        self.canvas = canvas
        self.size = self.canvas.size
        self.background = background
        self.reconfigure(background,widgets,active)

    def reconfigure(self,background=None,widgets=[],active=0):
        self.active = active
        self.widgets = widgets
        self.background = background
        self.num_widgets = len(self.widgets)

    def get_active(self):
        return self.active
    
    def get_name(self):
        """ Returns the plugin name. Must be a unicode string
        """
        raise NotImplementedError
    
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

    def show_config(self):
        pass

class PWLayout3x2(PWLayout):
    def __init__(self,double_buffer,canvas,background=None,widgets=[],active=0):
        PWLayout.__init__(self,double_buffer,canvas,background,widgets,active)
        self.name = u"Table 3x2"
        
        def get_name(self):
            pass
       
    def redraw(self,thumb_mode):
        if self.num_widgets == 0:
            self.draw_background()
        elif thumb_mode:
            self.draw_background()
            self.draw_thumbnails()
        else:
            self.draw_fullscreen()
        self.canvas.blit(self.double_buffer)

    def draw_background(self):
        if self.background:
            self.double_buffer.blit(self.background)
        else:
            self.double_buffer.clear((255,255,255))            

    def draw_fullscreen(self):
        self.double_buffer.blit(self.widgets[self.active])      

    def draw_thumbnails(self):
        n = 6*(self.active/6)
        ws = 10
        ww = (self.size[0]-ws)/3 - ws
        wh = (self.size[1]-ws)/2 - ws
        y = ws
        for lin in range(2):
            x = ws
            for col in range(3):
                if  n >=  self.num_widgets:
                    break
                # focus
                if n == self.active:
                    self.double_buffer.rectangle((x-2,y-2,x+ww+2,y+wh+2),
                                                 fill=(255,0,0),
                                                 outline=(255,0,0))
                # TODO: resize is generating exception ... async mode necessary
                try:
                    screen_aux = self.widgets[n].resize((ww,wh))
                    self.double_buffer.blit(screen_aux,target=(x,y),source=((0,0),(ww,wh)))
                except:
                    print "error: canvas resize"
                x += ww + ws
                n += 1
            y += wh + ws
    
    def next(self,thumb_mode):
        if self.num_widgets == 0:
            return
        
        # calculate next active widget
        curr = self.widgets[self.active]
        self.active = (self.active + 1) % self.num_widgets
        next = self.widgets[self.active]
                
        # transition effect
        if not thumb_mode:
            self.double_buffer.blit(curr)
            xstep = 8
            for x in range(xstep,self.size[0],xstep):
                self.double_buffer.blit(curr,
                                        target=(0,0),
                                        source=((x,0),self.size))
                self.double_buffer.blit(next,
                                        target=(self.size[0]-x,0),
                                        source=((0,0),self.size))
                self.canvas.blit(self.double_buffer)
   
    def prev(self,thumb_mode):
        if self.num_widgets == 0:
            return

        # calculate next active widget        
        curr = self.widgets[self.active]
        self.active = (self.active - 1) % self.num_widgets
        next = self.widgets[self.active]

        # transition effect        
        if not thumb_mode:
            self.double_buffer.blit(curr)
            xstep = 8
            for x in range(self.size[0]-xstep,0,-xstep):
                self.double_buffer.blit(curr,
                                        target=(self.size[0]-x,0),
                                        source=((0,0),self.size))
                self.double_buffer.blit(next,
                                        target=(0,0),
                                        source=((x,0),self.size))
                self.canvas.blit(self.double_buffer)
      
    def up(self,thumb_mode): 
        pass
    
    def down(self,thumb_mode): 
        pass     
        