from lib.Depend.gtk2 import gobject

class CBus(gobject.GObject):
    
    __gsignals__ = {
        'content-update':  (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, 
            (gobject.TYPE_PYOBJECT, gobject.TYPE_STRING)),
        'all-content-update':  (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, 
            [gobject.TYPE_PYOBJECT]),
        'content-update-from-plugin':  (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, 
            (gobject.TYPE_PYOBJECT, gobject.TYPE_STRING)),
        'run-dialog':  (gobject.SIGNAL_RUN_LAST, gobject.TYPE_PYOBJECT,
            (gobject.TYPE_PYOBJECT, gobject.TYPE_PYOBJECT, )), #type, message
        'project-opened': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ()),
        'project-opened-from-plugin-adapter': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ()),
        
        'position-change':  (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, 
            (gobject.TYPE_PYOBJECT, )),
        'many-position-change':  (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, 
            (gobject.TYPE_PYOBJECT, )),
        'position-change-from-plugin':  (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, 
            (gobject.TYPE_PYOBJECT, )),
        'properties-editing-started': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ()),
        'properties-editing-stoped': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ()),
        'all-content-update-from-plugin': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, 
            [gobject.TYPE_PYOBJECT]),
        'diagram-created-from-plugin': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, 
            [gobject.TYPE_PYOBJECT]),
    }
