from lib.Commands.Base import CCommand
from lib.Connections import CConnectionObject
from lib.Elements import CElementObject


class CRemoveProjectPropertyItemCommand(CCommand):
    def __init__(self, project, path):
        CCommand.__init__(self)
        
        self.__object = project.GetDomainObject()
        self.__path = path
    
    def _Do(self):
        self.__object.RemoveItem(self.__path)
    
    def _Redo(self):
        self.__object.RemoveItem(self.__path)
    
    def _Undo(self):
        self.__object.AppendItem(self.__path)

    def __str__(self):
        return _("Removed item from property %s of the project")%(self.__path)
