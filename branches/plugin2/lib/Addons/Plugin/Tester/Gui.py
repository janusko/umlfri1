import os
import platform
import threading
import gobject
import gtk
import gtk.keysyms
import pango


class PluginTesterGui(object):
    def __init__(self):
        self.w = gtk.Window()
        self.w.set_title("Plugin tester")
        box = gtk.VBox()
        boxInput = gtk.HBox()
        self.input = gtk.TextView()
        boxInput.pack_start(gtk.Label('>>>'), expand = False)
        boxInput.pack_end(self.input, expand = True)
        self.output = gtk.TextView()
        box.pack_start(self.output, expand = True)
        box.pack_end(boxInput, expand = False)
        self.w.add(box)
        
        if platform.system()=="Windows":
            font = "Lucida Console 9"
        else:
            font = "Luxi Mono 10"
        
        self.output.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse('black'))
        self.output.modify_text(gtk.STATE_NORMAL, gtk.gdk.color_parse('white'))
        self.output.modify_font(pango.FontDescription(font))
        self.output.set_wrap_mode(gtk.WRAP_CHAR)
        
        self.output.set_editable(False)
        
        self.output.get_buffer().create_tag("client", foreground = "yellow", pixels_below_lines = 10)
        self.output.get_buffer().create_tag("server", foreground = "white", pixels_below_lines = 10)
        
        self.input.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse('black'))
        self.input.modify_text(gtk.STATE_NORMAL, gtk.gdk.color_parse('white'))
        self.input.modify_font(pango.FontDescription(font))
        self.input.set_wrap_mode(gtk.WRAP_CHAR)
        
        self.w.set_size_request(900, 500)
    
    def __keypress(self, widget, event):
        if event.keyval == gtk.keysyms.Return:
            buffer = self.input.get_buffer()
            text = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter())
            buffer.set_text('')
            
            buffer = self.output.get_buffer()
            buffer.insert_with_tags_by_name(buffer.get_end_iter(), text + "\n", "client")
            
            self.pipeout.write(text + '\r\n')
            self.pipeout.flush()
            return True
        else:
            return False
    
    def __pipeReader(self):
        while True:
            line = self.pipein.readline()
            if not line:
                return
            gobject.idle_add(self.__addline, line)
    
    def __addline(self, line):
        buffer = self.output.get_buffer()
        buffer.insert_with_tags_by_name(buffer.get_end_iter(), line + "\n", "server")

    def show(self, channel):
        self.pipein = os.fdopen(channel.GetReaderFD(), 'rb')
        self.pipeout = os.fdopen(channel.GetWriterFD(), 'wb')
        
        self.input.connect('key-press-event', self.__keypress)
        
        threading.Thread(target = self.__pipeReader).start()
        
        self.w.show_all()
        self.input.grab_focus()

#PluginTesterGui().show(None)
#gobject.threads_init()
#gtk.main()
