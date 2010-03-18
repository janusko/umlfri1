from lib.Depend.gtk2 import gobject

class CGuiObject(gobject.GObject):
    
    def __init__(self, app):
        gobject.GObject.__init__(self)
        self.application = app
        self.__events = {}
        self.__connected = False
        for fnc in dir(self):
            fnc = getattr(self, fnc)
            if callable(fnc):
                if hasattr(fnc, 'events'):
                    for event in fnc.events:
                        obj, event, params = event
                        if event is None:
                            if obj == 'load':
                                gobject.idle_add(fnc)
                        else:
                            self.__events.setdefault(obj, []).append((event, fnc, params))
        for obj, oevents in self.__events.iteritems():
            objtxt = obj.split(".")
            obj = getattr(self, objtxt[0])
            for attr in objtxt[1:]:
                try:
                    obj = getattr(obj, attr)
                except AttributeError:
                    obj = obj.get_property(attr)
            for event, fnc, params in oevents:
                #print objtxt
                obj.connect(event, fnc, *params)
        
