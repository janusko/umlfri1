from base import IBase
from lib.Addons.Plugin.Communication.ComSpec import *
from DomainObject import IDomainObject
from lib.Addons.Plugin.Interface.decorators import *
from lib.Commands.Project.SetProjectPropertyValues import CSetProjectPropertyValuesCommand
from lib.Project.Project import CProject
from lib.Exceptions import *
from lib.Elements.Object import CElementObject

class IProject(IBase):
    __cls__ = CProject
    
    def GetFileName(him):
        return him.GetFileName()
    
    def GetRoot(him):
        return him.GetRoot().GetObject()
    
    def GetDefaultDiagrams(him):
        return him.GetDefaultDiagrams()
    
    def GetMetamodel(him):
        return him.GetMetamodel()


    def GetValue(him, path):
        return IDomainObject.GetValue(him.GetDomainObject(), path)

    def GetAllValues(him):
        return IDomainObject.GetAllValues(him.GetDomainObject())

    @destructive
    def SetValue(him, command, path, value):
        cmd = CSetProjectPropertyValuesCommand(him, {path: value})
        command.Execute(cmd)
    
    
    def Save(him):
        him.SaveProject()
    
    def SaveAs(him, fileName, isZippedFile):
        him.SaveProject(fileName, isZippedFile)
    

