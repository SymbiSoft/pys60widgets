from pwlayout import PWLayout

__all__ = [ "PWLayout3x2" ]

class PWLayout3x2(PWLayout):
    def __init__(self,mngr,active=0):
        info = {'name':u"3x2",
                'description':u"Generic 3x2 layout",
                'author':u"Marcelo Barros",
                'version':u"0.1"}
        PWLayout.__init__(self,mngr,info,active)
       
    def redraw(self,thumb_mode):
        if self.num_widgets == 0:
            self.draw_background()
        elif thumb_mode:
            self.draw_background()
            self.draw_thumbnails()
        else:
            self.draw_fullscreen()
        self.canvas.blit(self.buffer)

    def draw_background(self):
        if self.background:
            self.buffer.blit(self.background)
        else:
            self.buffer.clear((255,255,255))            

    def draw_fullscreen(self):
        self.buffer.blit(self.get_canvas(self.active))

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
                    self.buffer.rectangle((x-2,y-2,x+ww+2,y+wh+2),
                                          fill=(255,0,0),
                                          outline=(255,0,0))
                # TODO: resize is generating exception ... async mode necessary
                try:
                    screen_aux = self.get_canvas(n).resize((ww,wh))
                    self.buffer.blit(screen_aux,target=(x,y),source=((0,0),(ww,wh)))
                except:
                    print "error: canvas resize"
                x += ww + ws
                n += 1
            y += wh + ws
    
    def next(self,thumb_mode):       
        # calculate next active widget
        curr = self.get_canvas(self.active)
        self.active = (self.active + 1) % self.num_widgets
        next = self.get_canvas(self.active)
                
        # transition effect
        if not thumb_mode:
            self.buffer.blit(curr)
            xstep = 8
            for x in range(xstep,self.size[0],xstep):
                self.buffer.blit(curr,
                                 target=(0,0),
                                 source=((x,0),self.size))
                self.buffer.blit(next,
                                 target=(self.size[0]-x,0),
                                 source=((0,0),self.size))
                self.canvas.blit(self.buffer)
   
    def prev(self,thumb_mode):
        # calculate next active widget        
        curr = self.get_canvas(self.active)
        self.active = (self.active - 1) % self.num_widgets
        next = self.get_canvas(self.active)

        # transition effect        
        if not thumb_mode:
            self.buffer.blit(curr)
            xstep = 8
            for x in range(self.size[0]-xstep,0,-xstep):
                self.buffer.blit(curr,
                                 target=(self.size[0]-x,0),
                                 source=((0,0),self.size))
                self.buffer.blit(next,
                                 target=(0,0),
                                 source=((x,0),self.size))
                self.canvas.blit(self.buffer)
      
    def up(self,thumb_mode): 
        pass
    
    def down(self,thumb_mode): 
        pass     
        