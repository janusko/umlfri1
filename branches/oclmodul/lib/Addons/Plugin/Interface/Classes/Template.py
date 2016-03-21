from base import IBase
from lib.Project.Templates.Template import CTemplate

class ITemplate(IBase):
    __cls__ = CTemplate
    
    def GetName(him):
        return him.GetName()
    
    def GetMetamodelUri(him):
        return him.GetMetamodelUri()
    
    def CreateNewProject(him):
        return IBase.GetAdapter().CreateNewProject(him)
