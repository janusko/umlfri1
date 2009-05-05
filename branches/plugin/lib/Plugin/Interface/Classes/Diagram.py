from base import IBase
from lib.Plugin.Communication.ComSpec import *
from lib.Plugin.Interface.decorators import *
from lib.Drawing.Connection import CConnection
from lib.Drawing.Diagram import CDiagram
from lib.Drawing.Element import CElement
from lib.Elements.Object import CElementObject
from lib.Connections.Object import CConnectionObject

class IDiagram(IBase):
    __cls__ = CDiagram
    
    @result(r_str)
    def GetName(him):
        return him.GetName()
    
    @parameter('obj', t_classobject(CElementObject))
    @result(r_object)
    def GetElement(him, obj):
        return him.HasElementObject(obj)
    
    @parameter('obj', t_classobject(CConnectionObject))
    @result(r_object)
    def GetConnection(him, obj):
        return him.GetConnection(obj)
    
    @result(r_str)
    def GetPath(him):
        return him.GetPath()
    
    @result(r_str)
    def GetType(him):
        return him.GetType().GetId()
    
    @result(r_objectlist)
    def GetSelected(him):
        return list(him.GetSelected())
    
    @parameter('nolabels', t_bool)
    @result(r_objectlist)
    def GetSelectedElements(him, nolabels = False):
        return list(him.GetSelectedElements(nolabels))
    
    @result(r_objectlist)
    def GetSelectedConnections(him): 
        return list(him.GetSelectedConnections)
        
    @result(r_2x2intTuple)
    def GetSelectSquare(him):
        return him.GetSelectSquare(IBase.adapter.GetCanvas())
    
    @parameter('pos', t_2intTuple)
    @result(r_object)
    def GetElementAtPosition(him, pos): 
        return him.GetElementAtPosition(IBase.adapter.GetCanvas(), pos)
    
    @parameter('topleft', t_2intTuple)
    @parameter('bottomright', t_2intTuple)
    @parameter('includeall', t_bool)
    @result(r_objectlist)
    def GetElementsInRange(him, topleft, bottomright, includeall = True):
        return list(him.GetElementsInRange(IBase.adapter.GetCanvas(), topleft, bottomright, includeall))
    
    @result(r_2x2intTuple)
    def GetSizeSquare(him):
        return him.GetSizeSquare(IBase.adapter.GetCanvas())
    
    @result(r_objectlist)
    def GetElements(him):
        return list(him.GetElements())
        
    @result(r_objectlist)
    def GetConnections(him):
        return list(him.GetConnections)
    
    # WRITE METHODS
    
    @result(r_none)
    @parameter('name', t_str)
    def SetName(him, name):
        him.SetName(name)
        IBase.adapter.plugin_change_domain_value(him, CDiagram.NAME_PROPERY)
    
    #~ @parameter('connection', t_classobject(CConnection))
    #~ def AddConnection(him, connection): 
        #~ him.AddConnection(connection)
    
    #~ @parameter('item', t_classobject(CElement))
    #~ def DeleteElement(him, item):
        #~ him.DeleteItem(item)
    

