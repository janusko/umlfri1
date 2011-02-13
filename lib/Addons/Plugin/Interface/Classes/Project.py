from base import IBase
from lib.Addons.Plugin.Communication.ComSpec import *
from lib.Addons.Plugin.Interface.decorators import *
from lib.Project.Project import CProject
from lib.Exceptions import *
from lib.Elements.Object import CElementObject

class IProject(IBase):
    __cls__ = CProject
    
    def GetFileName(him):
        return him.GetFileName()
    
    def GetRoot(him):
        return him.GetRoot().GetObject()
    
    def GetNode(him, path):
        try:
            return him.GetNode(path).GetObject()
        except (ProjectError, ):
            raise ErrorDuringExecution()
    
    def GetDefaultDiagrams(him):
        return him.GetDefaultDiagrams()
    
    def GetMetamodel(him):
        return him.GetMetamodel()
    
    
    def Save(him, fileName = None, isZippedFile = None):
        him.SaveProject(fileName, isZippedFile)
    
    

