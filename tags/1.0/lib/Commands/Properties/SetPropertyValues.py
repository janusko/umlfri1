from ..Base.Command import CCommand, CommandNotDone
from lib.Connections.Object import CConnectionObject
from lib.Elements.Object import CElementObject

class CSetPropertyValuesCommand(CCommand):
    def __init__(self, object, newValues):
        CCommand.__init__(self)
        
        self.__object = object
        if not isinstance(self.__object, CConnectionObject):
            self.__objectName = object.GetName()
        else:
            self.__objectName = None
        self.__newValues = newValues
        self.__oldValues = None
    
    def _Do(self):
        if not self.__newValues:
            raise CommandNotDone
        self.__oldValues = dict((name, self.__object.GetValue(name)) for name in self.__newValues)
        
        self._Redo()
    
    def _Redo(self):
        for name, value in self.__newValues.iteritems():
            self.__object.SetValue(name, value)
    
    def _Undo(self):
        for name, value in self.__oldValues.iteritems():
            self.__object.SetValue(name, value)
    
    def Fold(self, other):
        if isinstance(other, CSetPropertyValuesCommand) and other.__newValues.keys() == self.__newValues.keys():
            ret = CSetPropertyValuesCommand(self.__object, self.__newValues)
            ret.__oldValues = other.__oldValues
            self._CopyStatusTo(ret)
            return ret
        return None
    
    def GetGuiUpdates(self):
        if isinstance(self.__object, CElementObject):
            return [
                ('elementChanged', (self.__object, self.__newValues.keys()))
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
        
        if len(self.__newValues) == 1:
            return _("Changed property %s of the %s")%(self.__oldValues.keys()[0], name)
        else:
            return _("Changed properties of the %s" % name)
