# -*- coding: cp1252 -*-
# (c) Marcelo Barros de Almeida
# marcelobarrosalmeida@gmail.com
# License: GPL3

from appuifw import *
import e32
import sysinfo
import os
import graphics
import key_codes

class ExplorerDemo(object):
    """ Demo explorer class
    """
    def __init__(self,init_dir = ""):       
        self.lock = e32.Ao_lock()
        app.title = u"Explorer demo"
        app.screen = "full"
        self.show_images = True        
        app.menu = [(u"Hide images", lambda: self.images_menu(False)),
                    (u"About", self.about),
                    (u"Quit", self.close_app)]
        self.cur_dir = unicode(init_dir)
        if not os.path.exists(self.cur_dir):
            self.cur_dir = u""
        self.fill_items()
        
        pos = (0,0) + sysinfo.display_pixels()
        self.listbox = CanvasListBox(items=self.items,
                                     cbk=self.item_selected,
                                     images=self.images,
                                     position=pos,
                                     margins=[6,2,2,2],
                                     selection_fill_color=(0,43,34),
                                     selection_border_color=(0,43,34),
                                     odd_fill_color=(0,0,0),
                                     even_fill_color=(0,0,0),
                                     image_size=(44,44),
                                     title_font_color=(255,255,102),
                                     title_fill_color=(0,43,34),
                                     title=self.cur_dir)
        
        app.body = self.listbox
        self.lock.wait()

                          
    def fill_items(self):
        if self.cur_dir == u"":
            self.items = [ unicode(d + "\\") for d in e32.drive_list() ]
            self.images = [None for d in self.items]
        else:
            entries = [ e.decode('utf-8')
                        for e in os.listdir( self.cur_dir.encode('utf-8') ) ]
            entries.sort()
            d = self.cur_dir
            dirs = []
            files = []
            dimages = []
            fimages = []
            for e in entries:
                f = os.path.join(d,e)
                if os.path.isdir(f.encode('utf-8')):
                    dirs.append(e.upper())
                    dimages.append(None)
                elif os.path.isfile(f.encode('utf-8')):
                    desc = e.lower() + "\n"
                    desc += "%d bytes" % os.path.getsize(f)
                    files.append(desc)
                    if f.endswith(".jpg") or f.endswith(".png") or f.endswith(".gif"):
                        fimages.append(f)
                    else:
                        fimages.append(None)
            dirs.insert(0, u".." )
            dimages.insert(0,None)
            self.items = dirs + files
            self.images = dimages + fimages       

    def images_menu(self,val):
        self.show_images = val
        menu = []
        if val:
            menu += [(u"Hide images", lambda: self.images_menu(False))]
        else:
            menu += [(u"Show images", lambda: self.images_menu(True))]
        menu += [(u"About", self.about),
                 (u"Quit", self.close_app)]
        app.menu = menu
        self.update_list()
                    
    def item_selected(self):
        item = self.listbox.current()
        f = self.items[item]
        self.update_list(f)

    def update_list(self,f=u""):
        if f:
            d = os.path.abspath( os.path.join(self.cur_dir,f) )
        else:
            d = self.cur_dir
        if os.path.isdir(d.encode('utf-8')):
            if f == u".." and len(self.cur_dir) == 3:
                self.cur_dir = u""
            else:
                self.cur_dir = d 
            self.fill_items()
            attrs = self.listbox.get_config()
            attrs['items'] = self.items
            attrs['title'] = u" " + self.cur_dir
            if self.show_images:
                attrs['images'] = self.images
                attrs['image_size'] = (44,44)
            else:
                attrs['images'] = []
                
            self.listbox.reconfigure(attrs)

    def about(self):
        note(u"Explorer demo by Marcelo Barros (marcelobarrosalmeida@gmail.com)","info")
        
    def close_app(self):
        self.lock.signal()
        app.set_exit()

#if __name__ == "__main__":
ExplorerDemo()


