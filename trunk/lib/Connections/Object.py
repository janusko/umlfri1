from lib.Exceptions.UserException import *
from lib.Domains import CDomainObject
from Alias import CConnectionAlias
from lib.Base import CBaseObject
import weakref

class CConnectionObject(CBaseObject):
    """
    Object that represents logical connection and its properties
    """
    def __init__(self, type, source, dest):
        """
        Initialize connection object
        
        @param type: Type of connection
        @type  type: L{CConnectionType<Type.CConnectionType>} or L{CConnectionType<Type.CConnectionAlias>}
        
        @param source: Source element of connection
        @type  source: L{CElementObject<lib.Elements.Object.CElementObject>}
        
        @param dest: Destination element of connection
        @type  dest: L{CElementObject<lib.Elements.Object.CElementObject>}
        """
        self.__SetWeakSource(None)
        self.__SetWeakDestination(None)
        self.revision = 0
        self.appears = []
        if isinstance(type, CConnectionAlias):
            self.type = type.GetAliasType()
        else:
            self.type = type
        self.SetSource(source)
        try:
            self.SetDestination(dest)
        except:
            if self.GetSource() is not None:
                self.GetSource().RemoveConnection(self)
            self.__SetWeakSource(None)
            raise
        self.domainobject = CDomainObject(self.type.GetDomain())
        if isinstance(type, CConnectionAlias):
            for path, value in type.GetDefaultValues():
                self.domainobject.SetValue(path, value)
    
    def __CheckRecursiveConnection(self):
        """
        Validate connection for recursion
        """
        source = self.GetSource()
        dest = self.GetDestination()
        type = self.type
        
        if source is None or dest is None:
            return True
        
        if source is not dest:
            return True
        typeid = type.GetId()
        destid = dest.GetType().GetId()
        allow = dict(source.GetType().GetConnections())
        withelem, allowrecursive = allow.get(typeid, (None, False))
        if allowrecursive and (withelem is None or '*' in withelem  or destid in withelem):
            return True
        return False
        
    def __CheckConnection(self, reversed):
        """
        Validate connection
        """
        if reversed:
            source = self.GetSource()
            dest = self.GetDestination()
        else:
            source = self.GetDestination()
            dest = self.GetSource()
        type = self.type
        
        if source is None or dest is None:
            return True
        
        typeid = type.GetId()
        destid = dest.GetType().GetId()
        allow = dict(source.GetType().GetConnections())
        if typeid in allow:
            withelem, allowrecursive = allow[typeid]
            if withelem is None:
                return None
            elif '*' in withelem or destid in withelem:
                return True
        return False
    
    def __DoCheck(self):
        """
        Do all validations
        
        @raise ConnectionRestrictionError: if there is something wrong
        """
        if not self.__CheckRecursiveConnection():
            raise ConnectionRestrictionError
        checksrc = self.__CheckConnection(False)
        checkdest = self.__CheckConnection(True)
        if not (checksrc or checkdest or (checksrc is checkdest is None)):
            raise ConnectionRestrictionError
    
    def GetRevision(self):
        """
        Get the revision number for this connection.
        Revision number increses after each change in connection
        object.
        
        @return: Revision number
        @rtype:  integer
        """
        return self.revision
        
    def AddRevision(self):
        """
        Increase revision on external change (Like movement in project tree)
        """
        
        self.revision += 1
    
    def GetAppears(self):
        """
        Gets all diagrams, this connection appers on
        
        @rtype:  iterator over L{CDiagram<lib.Drawing.Diagram.CDiagram>}
        """
        for i in self.appears:
            yield i()

    def AddAppears(self, diagram):
        """
        Add diagram, connection is appeared on
        
        @param diagram: Diagram
        @type  diagram: L{CDiagram<lib.Drawing.Diagram.CDiagram>}
        """
        self.appears.append(weakref.ref(diagram))

    def RemoveAppears(self, diagram):
        """
        Remove diagram, connection was appeared on, from the list
        
        @param diagram: Diagram
        @type  diagram: L{CDiagram<lib.Drawing.Diagram.CDiagram>}
        
        @raise ValueError: if given diagram is not found
        """
        for id, value in enumerate(self.appears):
            if value() is diagram:
                del self.appears[id]
    
    def AppearsAt(self, diagram):
        return diagram in self.appears

    def GetType(self):
        """
        Return type of connection
        
        @return: Type of this connection
        @rtype:  L{CConnectionType<Type.CConnectionType>}
        """
        return self.type
    
    def SetType(self, value):
        """
        Set type for this connection
        
        @param value: New type for this connection
        @type  value: L{CConnectionType<Type.CConnectionType>}
        """
        self.type = value
    
    def GetConnectedObject(self, object):
        """
        Get object that is connected through this connection to another object
        
        @param object: known object
        @type  object: L{CElementObject<lib.Elements.Object.CElementObject>}
        
        @return: other object
        @rtype:  L{CElementObject<lib.Elements.Object.CElementObject>}
        """
        if self.GetSource() is object:
            return self.GetDestination()
        elif self.GetDestination() is object:
            return self.GetSource()
        else:
            return None
        
    def GetDestination(self):
        """
        Get destination of this connection
        
        @return: connection destination
        @rtype:  L{CElementObject<lib.Elements.Object.CElementObject>}
        """
        return self.destination()

    def GetSource(self):
        """
        Get source of this connection
        
        @return: connection source
        @rtype:  L{CElementObject<lib.Elements.Object.CElementObject>}
        """
        return self.source()

    def SetDestination(self, dest):
        """
        Set destination object of this connection
        
        @param dest: object which has to be set as destination
        @type  dest: L{CElementObject<lib.Elements.Object.CElementObject>}
        """
        if self.GetDestination() and self.GetDestination() is not self.GetSource():
            self.GetDestination().RemoveConnection(self)
        old = self.GetDestination()
        self.__SetWeakDestination(dest)
        try:
            self.__DoCheck()
        except:
            self.__SetWeakDestination(old)
            raise
        if dest is not None:
            dest.AddConnection(self)
        self.revision += 1
        
    def ChangeConnection(self):
        dest = self.GetDestination()
        sour = self.GetSource()
        self.__SetWeakSource(dest)
        self.__SetWeakDestination(sour)

    def __SetWeakSource(self, source):
        if source is None:
            self.source = lambda: None
        else:
            self.source = weakref.ref(source)
            
    
        
    def __SetWeakDestination(self, destination):
        if destination is None:
            self.destination = lambda: None
        else:
            self.destination = weakref.ref(destination)
   
        
    def SetSource(self, source):
        """
        Set source object of this connection
        
        @param source: object which has to be set as source
        @type  source: L{CElementObject<lib.Elements.Object.CElementObject>}
        """
        if self.GetSource() and self.GetDestination() is not self.GetSource():
            self.GetSource().RemoveConnection(self)
        old = self.GetSource()
        self.__SetWeakSource(source)
        try:
            self.__DoCheck()
        except:
            self.__SetWeakSource(old)
            raise
        if source is not None:
            source.AddConnection(self)
        self.revision += 1
    
    def Disconnect(self):
        """
        Disconnect self from other objects
        """
        if self.GetSource() is self.GetDestination():
            self.GetSource().RemoveConnection(self)
        else:
            self.GetSource().RemoveConnection(self)
            self.GetDestination().RemoveConnection(self)            
    
    def Paint(self, context):
        """
        Paint self on canvas
        
        @param context: context in which is connection being drawn
        @type  context: L{CDrawingContext<lib.Drawing.Context.DrawingContext.CDrawingContext>}
        """
        self.type.Paint(context)
    
    def GetDomainName(self, key=''):
        return self.domainobject.GetDomainName(key)
    
    def GetDomainType(self, key=''):
        return self.domainobject.GetType(key)
    
    def GetDomainObject(self):
        return self.domainobject
    
    def GetValue(self, key):
        return self.domainobject.GetValue(key)
    
    def SetValue(self, key, value):
        self.domainobject.SetValue(key, value)
        self.revision += 1
        
    def GetSaveInfo(self):
        return self.domainobject.GetSaveInfo()
    
    def SetSaveInfo(self, value):
        return self.domainobject.SetSaveInfo(value)
    
    def HasVisualAttribute(self, key):
        return self.domainobject.HasVisualAttribute(key)
    
    def AppendItem(self, key):
        self.domainobject.AppendItem(key)
        self.revision += 1
    
    def RemoveItem(self, key):
        self.domainobject.RemoveItem(key)
        self.revision += 1
