import gtk, gobject

class CGtk(object):
    
    def Mainloop(self):
        gobject.threads_init()
        gtk.main()
    
    def Call(self, callable, *args, **kwds):
        gobject.idle_add(callable, *args, **kwds)
    
    def Stop(self):
        gtk.main_quit()
