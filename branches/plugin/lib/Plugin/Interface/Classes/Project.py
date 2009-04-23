from base import IBase
from lib.Plugin.Communication.ComSpec import *
from lib.Plugin.Interface.decorators import *
from lib.Project.Project import CProject
from lib.Exceptions import *
from lib.Elements.Object import CElementObject

class IProject(IBase):
    __cls__ = CProject
    
    def GetFileName(self):
        return self.GetFileName()
    
    @result(r_object)
    def GetRoot(self):
        return self.GetRoot().GetObject()
    
    @result(r_object)
    def GetNode(self, path):
        try:
            return self.GetNode(path).GetObject()
        except (ProjectError, ):
            raise ErrorDuringExecution()
    
    @result(r_objectlist)
    def GetDefaultDiagrams(self):
        return self.GetDefaultDiagrams()
    
    def GetFileName(self):
        return self.GetFileName()
    
    @parameter('node', t_classobject(CElementObject))
    def RemoveNode(self, node):
        node = node.GetNode()
        if node is not None:
            self.RemoveNode(node)
    
    @result(r_object)
    def GetCurrentDiagram(self):
        return self.app.GetWindow('frmMain').picDrawingArea.GetDiagram()
