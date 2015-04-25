from lib.Commands.Base import CCommand
from lib.Connections import CConnectionObject
from lib.Elements import CElementObject


class CAppendProjectPropertyItemCommand(CCommand):
    def __init__(self, project, path):
        CCommand.__init__(self)
        
        self.__object = project.GetDomainObject()
        self.__path = path
        self.__idx = None
    
    def _Do(self):
        if not self.__path.endswith(']'):
            self.__idx = len(self.__object.GetValue(self.__path))
        self.__object.AppendItem(self.__path)
    
    def _Redo(self):
        if self.__idx is None:
            self.__object.AppendItem(self.__path)
        else:
            self.__object.AppendItem("%s[%d]" % (self.__path, self.__idx))
    
    def _Undo(self):
        if self.__idx is None:
            self.__object.RemoveItem(self.__path)
        else:
            self.__object.RemoveItem("%s[%d]" % (self.__path, self.__idx))
    
    def __str__(self):
        return _("Added item to property %s of the project")%(self.__path)
