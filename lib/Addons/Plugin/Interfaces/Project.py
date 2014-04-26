from .Decorators import params, mainthread, polymorphic

from . import ElementObject
from . import Diagram
from . import Metamodel

class IProject(object):
    def __init__(self, plugin, project):
        self.__plugin = plugin
        self.__project = project
    
    @property
    def uid(self):
        return self.__project.GetUID()
    
    def GetFileName(self):
        return self.__project.GetFileName()
    
    def GetRoot(self):
        return ElementObject.IElementObject(self.__plugin, self.__project.GetRoot().GetObject())
    
    def GetDefaultDiagrams(self):
        return Diagram.IDiagram(self.__plugin, self.__project.GetDefaultDiagrams())
    
    def GetMetamodel(self):
        return Metamodel.IMetamodel(self.__project.GetMetamodel())
    
    def Save(self):
        self.__project.SaveProject()
    
    @params(str, bool)
    def SaveAs(self, fileName, isZippedFile):
        self.__project.SaveProject(fileName, isZippedFile)
