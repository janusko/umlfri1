from base import IBase
from lib.Addons.Plugin.Communication.ComSpec import *
from lib.Addons.Plugin.Interface.decorators import *
from lib.Drawing.Connection import CConnection
from lib.Drawing.Diagram import CDiagram
from lib.Drawing.Element import CElement
from lib.Elements.Object import CElementObject
from lib.Connections.Object import CConnectionObject
from lib.Addons.Plugin.Interface.Classes.DomainObject import IDomainObject
from lib.Drawing import CConLabelInfo

class IDiagram(IDomainObject):
    __cls__ = CDiagram
    
    def GetElement(him, obj):
        return him.HasElementObject(obj)
    
    def GetConnection(him, obj):
        return him.GetConnection(obj)
    
    def GetSelected(him):
        return list(him.GetSelected())
    
    def GetSelectedElements(him):
        return list(him.GetSelectedElements(True))
        
    def GetSelectedLabels(him):
        return [item for item in him.GetSelectedElements(False) if isinstance(item, CConLabelInfo)]
    
    def GetSelectedConnections(him): 
        return list(him.GetSelectedConnections())
        
    def GetSelectSquare(him):
        return him.GetSelectSquare(IBase.adapter.GetCanvas())
    
    def GetElementAtPosition(him, pos): 
        return him.GetElementAtPosition(IBase.adapter.GetCanvas(), pos)
    
    def GetElementsInRange(him, topleft, bottomright, includeall = True):
        return list(him.GetElementsInRange(IBase.adapter.GetCanvas(), topleft, bottomright, includeall))
    
    def GetSizeSquare(him):
        return him.GetSizeSquare(IBase.adapter.GetCanvas())
    
    def GetElements(him):
        return list(him.GetElements())
        
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
    

