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
        
        'project-selection-changed': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT, )),
        
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
        'diagram-created': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, 
            [gobject.TYPE_PYOBJECT]),
        'diagram-removed': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, 
            [gobject.TYPE_PYOBJECT]),
        'element-object-created': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, 
            [gobject.TYPE_PYOBJECT]),
        'element-object-removed': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, 
            [gobject.TYPE_PYOBJECT]),
        'connection-object-created': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, 
            [gobject.TYPE_PYOBJECT]),
        'connection-object-removed': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, 
            [gobject.TYPE_PYOBJECT]),
        'connection-changed': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, 
            [gobject.TYPE_PYOBJECT]),
        'element-changed': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, 
            [gobject.TYPE_PYOBJECT]),
        'diagram-changed': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, 
            [gobject.TYPE_PYOBJECT]),
        'undo-redo-action': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, 
            [gobject.TYPE_STRING]),
    }
    
    __doMap = {
        'createDiagram': 'diagram-created',
        'createElementObject': 'element-object-created',
        'createConnectionObject': 'connection-object-created',
        'connectionChanged': 'connection-changed',
        'elementChanged': 'element-changed',
        'diagramChanged': 'diagram-changed',
    }
    
    __undoMap = {
        'createDiagram': 'diagram-removed',
        'createElementObject': 'element-object-removed',
        'createConnectionObject': 'connection-object-removed',
        'connectionChanged': 'connection-changed',
        'elementChanged': 'element-changed',
        'diagramChanged': 'diagram-changed',
    }
    
    def DoUpdates(self, updates):
        for upd, params in updates:
            self.emit(self.__doMap[upd], params)
        self.emit('undo-redo-action', 'do')
    
    def UndoUpdates(self, updates):
        for upd, params in updates:
            self.emit(self.__undoMap[upd], params)
        self.emit('undo-redo-action', 'undo')
