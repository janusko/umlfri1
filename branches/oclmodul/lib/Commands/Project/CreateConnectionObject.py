from ..Base.Command import CCommand
from lib.Connections.Object import CConnectionObject

class CCreateConnectionObjectCommand(CCommand):
    def __init__(self, sourceObject, destinationObject, connectionType):
        CCommand.__init__(self)
        
        self.__sourceObject = sourceObject
        self.__destinationObject = destinationObject
        self.__connectionType = connectionType
        self.__connectionObject = None
    
    def _Do(self):
        self.__connectionObject = CConnectionObject(self.__connectionType, self.__sourceObject, self.__destinationObject)
    
    def _Redo(self):
        self.__sourceObject.AddConnection(self.__connectionObject)
        self.__destinationObject.AddConnection(self.__connectionObject)
    
    def _Undo(self):
        self.__connectionObject.RemoveConnection(self.__connectionObject)
        self.__destinationObject.RemoveConnection(self.__connectionObject)
    
    def GetGuiUpdates(self):
        return [
            ('createConnectionObject', self.__connectionObject)
        ]
    
    def __str__(self):
        return _("Connection created between objects %s and %s") % (self.__sourceObject.GetName(), self.__destinationObject.GetName())
    
    def GetConnectionObject(self):
        return self.__connectionObject
