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
        'node-moved-in-tree': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, 
            [gobject.TYPE_PYOBJECT]),
        'diagram-moved-in-tree': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, 
            [gobject.TYPE_PYOBJECT]),
        'undo-redo-action': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, 
            [gobject.TYPE_STRING]),
        'add-element':(gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE,
            (gobject.TYPE_PYOBJECT,gobject.TYPE_PYOBJECT,gobject.TYPE_PYOBJECT,)),
        'delete-element-from-all':(gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE,
            (gobject.TYPE_PYOBJECT, )),
        'project-expand-node': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, 
            [gobject.TYPE_PYOBJECT]),
        'open-diagram': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, 
            [gobject.TYPE_PYOBJECT]),
        'open-specification': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE,
            [gobject.TYPE_PYOBJECT]),
        'get-selected-toolbox-item': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_PYOBJECT,
            []),
        'set-selected-toolbox-item': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE,
            [gobject.TYPE_PYOBJECT]),
        'selected-toolbox-item-changed': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE,
            [gobject.TYPE_PYOBJECT]),
        'selected-items': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE,
            [gobject.TYPE_PYOBJECT]),
        'show-element-in-treeView': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT, )),
    }
    
    __actionMap = {
        'expandNode': 'project-expand-node',
        'openDiagram': 'open-diagram',
    }
    
    __actionParamMangle = {
        
    }
    
    __doMap = {
        'createDiagram': 'diagram-created',
        'createElementObject': 'element-object-created',
        'createConnectionObject': 'connection-object-created',
        'connectionChanged': 'connection-changed',
        'elementChanged': 'element-changed',
        'diagramChanged': 'diagram-changed',
        'moveNodeInProject': 'node-moved-in-tree',
        'moveDiagramInProject': 'diagram-moved-in-tree',
    }
    
    __undoMap = {
        'createDiagram': 'diagram-removed',
        'createElementObject': 'element-object-removed',
        'createConnectionObject': 'connection-object-removed',
        'connectionChanged': 'connection-changed',
        'elementChanged': 'element-changed',
        'diagramChanged': 'diagram-changed',
        'moveNodeInProject': 'node-moved-in-tree',
        'moveDiagramInProject': 'diagram-moved-in-tree',
    }
    
    __doParamMangle = {
        'moveNodeInProject': lambda param: (param[0], param[1]),
        'moveDiagramInProject': lambda param: (param[0], param[1]),
    }
    
    __undoParamMangle = {
        'moveNodeInProject': lambda param: (param[0], param[2]),
        'moveDiagramInProject': lambda param: (param[0], param[2]),
    }
    
    def __ExecuteActions(self, actions):
        for action, params in actions:
            if action in self.__actionParamMangle:
                mangleFnc = self.__actionParamMangle[action]
                params = [mangleFnc(param) for param in params]
            self.emit(self.__actionMap[action], params)

    def ExecuteActions(self, actions, postpone = False):
        if postpone:
            gobject.idle_add(self.__ExecuteActions, actions)
        else:
            self.__ExecuteActions(actions)
    
    def __DoUpdates(self, updates):
        for upd, params in updates:
            if upd in self.__doParamMangle:
                mangleFnc = self.__doParamMangle[upd]
                params = [mangleFnc(param) for param in params]
            self.emit(self.__doMap[upd], params)
        self.emit('undo-redo-action', 'do')

    def DoUpdates(self, updates, postpone = False):
        if postpone:
            gobject.idle_add(self.__DoUpdates, updates)
        else:
            self.__DoUpdates(updates)
    
    def UndoUpdates(self, updates, postpone = False):
        for upd, params in updates:
            if upd in self.__undoParamMangle:
                mangleFnc = self.__undoParamMangle[upd]
                params = [mangleFnc(param) for param in params]
            self.emit(self.__undoMap[upd], params)
        self.emit('undo-redo-action', 'undo')
