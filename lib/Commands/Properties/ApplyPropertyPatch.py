from ..Base.Command import CCommand, CommandNotDone
from lib.Connections.Object import CConnectionObject
from lib.Elements.Object import CElementObject

class CApplyPropertyPatchCommand(CCommand):
    def __init__(self, object, patch):
        CCommand.__init__(self)
        
        self.__object = object
        self.__patch = patch
        
        if not isinstance(self.__object, CConnectionObject):
            self.__objectName = object.GetName()
        else:
            self.__objectName = None
    
    def _Do(self):
        if not self.__patch:
            raise CommandNotDone
        
        self._Redo()
    
    def _Redo(self):
        for patchCommand in self.__patch:
            cmd = patchCommand.GetCommand()
            if cmd == 'modify':
                self.__object.SetValue(patchCommand.GetPath(), patchCommand.GetNewValue(), useRuntimeType=False)
            elif cmd == 'append':
                self.__object.AppendItem(patchCommand.GetPath(), patchCommand.GetNewValue(), useRuntimeType=False)
            elif cmd == 'remove':
                self.__object.RemoveItem("%s[%d]" % (patchCommand.GetPath(), patchCommand.GetIndex()), useRuntimeType=False)
    
    def _Undo(self):
        for patchCommand in self.__patch:
            cmd = patchCommand.GetCommand()
            if cmd == 'modify':
                self.__object.SetValue(patchCommand.GetPath(), patchCommand.GetOldValue(), useRuntimeType=False)
            elif cmd == 'append':
                self.__object.RemoveItem("%s[%d]" % (patchCommand.GetPath(), patchCommand.GetIndex()), useRuntimeType=False)
            elif cmd == 'remove':
                self.__object.AppendItem(patchCommand.GetPath(), patchCommand.GetOldValue(), useRuntimeType=False)
    
    def GetGuiUpdates(self):
        if isinstance(self.__object, CElementObject):
            return [
                ('elementChanged', (self.__object, set(cmd.GetPath() for cmd in self.__patch)))
            ]
        elif isinstance(self.__object, CConnectionObject):
            return [
                ('connectionChanged', (self.__object, set(cmd.GetPath() for cmd in self.__patch)))
            ]
        else:
            return [
                ('diagramChanged', (self.__object, set(cmd.GetPath() for cmd in self.__patch)))
            ]
    
    def __str__(self):
        if isinstance(self.__object, CElementObject):
            name = "element %s" % self.__objectName
        elif isinstance(self.__object, CConnectionObject):
            name = "connection"
        else:
            name = "diagram %s"
        
        if len(self.__patch) == 1 and self.__patch[0].GetCommand() == 'modify':
            return _("Changed property %s of the %s")%(self.__patch[0].GetPath(), name)
        else:
            return _("Changed properties of the %s" % name)
