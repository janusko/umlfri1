from base import IBase
from lib.Addons.Plugin.Communication.ComSpec import *
from lib.Addons.Plugin.Interface.decorators import *
from lib.Drawing.Connection import CConnection
from lib.Drawing.Diagram import CDiagram
from lib.Drawing.Element import CElement
from lib.Elements.Object import CElementObject
from lib.Connections.Object import CConnectionObject
from lib.Addons.Plugin.Interface.Classes.DomainObject import IDomainObject

class IDiagram(IDomainObject):
    __cls__ = CDiagram
    
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
        return list(him.GetConnections())
    
    # WRITE METHODS
    
    @destructive
    def AddElement(him, elementObject, pos = (0,0)):
        element = CElement(him, elementObject)
        element.SetPosition(pos)
        IBase.adapter.plugin_add_element(element)
        
    @destructive
    def AddNewElement(him, elementType, pos = (0,0)):
        elementObject = CElementObject(elementType)
        element = CElement(him, elementObject)
        element.SetPosition(pos)
        IBase.adapter.plugin_add_new_element(element)
        
    
    
    #~ @parameter('connection', t_classobject(CConnection))
    #~ def AddConnection(him, connection): 
        #~ him.AddConnection(connection)
    
    #~ @parameter('item', t_classobject(CElement))
    #~ def DeleteElement(him, item):
        #~ him.DeleteItem(item)
    

