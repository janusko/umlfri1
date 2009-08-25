from base import IBase
from lib.Addons.Plugin.Communication.ComSpec import *
from lib.Addons.Plugin.Interface.decorators import *
from lib.Project.Project import CProject
from lib.Exceptions import *
from lib.Elements.Object import CElementObject

class IProject(IBase):
    __cls__ = CProject
    
    @result(r_str)
    def GetFileName(him):
        return him.GetFileName()
    
    @result(r_object)
    def GetRoot(him):
        return him.GetRoot().GetObject()
    
    @result(r_object)
    @parameter('path', t_str)
    def GetNode(him, path):
        try:
            return him.GetNode(path).GetObject()
        except (ProjectError, ):
            raise ErrorDuringExecution()
    
    @result(r_objectlist)
    def GetDefaultDiagrams(him):
        return him.GetDefaultDiagrams()
    
    @result(r_object)
    def GetCurrentDiagram(him):
        return him.app.GetWindow('frmMain').picDrawingArea.GetDiagram()
        
    #~ @parameter('node', t_classobject(CElementObject))
    #~ def RemoveNode(him, node):
        #~ node = node.GetNode()
        #~ if node is not None:
            #~ him.RemoveNode(node)
    

