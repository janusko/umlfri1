from lib.Commands.ProjectViewCommands import CDeleteElementCmd
from lib.Drawing import  CElement


class CPurgeElementCmd(CDeleteElementCmd):
   
    def __init__(self, element, project):
        node = element.GetObject().GetNode()
        element.Deselect()
        CDeleteElementCmd.__init__(self, project,  node)
