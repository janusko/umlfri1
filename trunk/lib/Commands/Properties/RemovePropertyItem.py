from lib.Commands.Base import CCommand
from lib.Connections import CConnectionObject
from lib.Elements import CElementObject


class CRemovePropertyItemCommand(CCommand):
    def __init__(self, object, path):
        CCommand.__init__(self)
        
        self.__object = object
        if not isinstance(self.__object, CConnectionObject):
            self.__objectName = object.GetName()
        else:
            self.__objectName = None
        self.__path = path
    
    def _Do(self):
        self.__object.RemoveItem(self.__path)
    
    def _Redo(self):
        self.__object.RemoveItem(self.__path)
    
    def _Undo(self):
        self.__object.AppendItem(self.__path)
    
    def GetGuiUpdates(self):
        if isinstance(self.__object, CElementObject):
            return [
                ('elementChanged', (self.__object, []))
            ]
        elif isinstance(self.__object, CConnectionObject):
            return [
                ('connectionChanged', (self.__object, self.__newValues.keys()))
            ]
        else:
            return [
                ('diagramChanged', (self.__object, self.__newValues.keys()))
            ]
    
    def __str__(self):
        if isinstance(self.__object, CElementObject):
            name = "element %s" % self.__objectName
        elif isinstance(self.__object, CConnectionObject):
            name = "connection"
        else:
            name = "diagram %s"
        
        return _("Removed item from property %s of the %s")%(self.__path, name)
