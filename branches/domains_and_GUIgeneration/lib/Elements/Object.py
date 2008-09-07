from lib.Exceptions.UserException import *
import weakref

class CElementObject(object):
    """
    Object that represents logical element and its properties
    """
    def __init__(self, type):
        """
        Initialize element object and set it into default state
        
        @param type: Type of the new element
        @type  type: L{CElementType<Type.CElementType>}
        """
        self.revision = 0
        self.type = type
        self.path = None
        self.connections = []
        self.attribs = {}
        for i in self.type.GetAttributes():
            self.SetAttribute(i, self.type.GetDefValue(i))            
        if type.GetGenerateName():
            self.SetAttribute('Name', 'New ' + type.GetId())
        else:
            self.SetAttribute('Name', '')
        self.node = lambda: None
        self.appears = []
    
    def GetRevision(self):
        """
        Get revision of this object. Revision is incremented after each
        object state chage
        
        @return: Object revision
        @rtype:  integer
        """
        return self.revision
    
    def GetAppears(self):
        """
        Get list of object appearances on diagrams
        
        @return: list of diagrams
        @rtype:  iterator over L{CDiagram<lib.Drawing.Diagram.CDiagram>}
        """
        for i in self.appears:
            yield i

    def AddAppears(self, diagram):
        """
        Add element appearance
        
        @param diagram: Diagram on which element appears
        @type  diagram: L{CDiagram<lib.Drawing.Diagram.CDiagram>}
        """
        self.appears.append(diagram)

    def RemoveAppears(self, diagram):
        """
        Remove element appearance
        
        @param diagram: Diagram on which element was appearing
        @type  diagram: L{CDiagram<lib.Drawing.Diagram.CDiagram>}
        
        @raise ValueError: if given diagram is not found
        """
        self.appears.remove(diagram)
    
    def GetPath(self):
        """
        Get path of this element object in the project
        
        @return: Element object path
        @rtype:  string
        """
        return self.path
    
    def SetPath(self, path):
        """
        Set path of this element object in the project
        
        @param path: Element object path
        @type  path:  string
        """
        self.path = path 
    
    def GetNode(self):
        """
        Get the project node which is associated with this element object
        
        @return: project node of this element
        @rtype:  L{CProjectNode<lib.Project.Node.CProjectNode>}
        """
        return self.node
        
    def AddConnection(self, connection):
        """
        Add the connection object connected to this element object
        
        @param connection: connected connection
        @type  connection: L{CConnectionObject<lib.Connections.Object.CConnectionObject>}
        """
        self.revision += 1
        if connection not in self.connections:
            self.connections.append(connection)
        else:
            pass
            
    def GetConnections(self):
        """
        Get list of connections connected to this object
        
        @return: List of connected connections
        @rtype:  iterator over L{CConnectionObject<lib.Connections.Object.CConnectionObject>}(s)
        """
        for c in self.connections:
            yield c
        
    def GetType(self):
        return self.type
    
    def GetSize(self, context):
        return self.type.GetSize(context)
        
    def GetName(self):
        if 'Name' in self.attribs:
            return self.attribs['Name']
        else:
            raise ElementAttributeError("KeyError")

    def GetAttribute(self, key):
        if key in self.attribs:
            return self.attribs[key]
        else:
            return None
    
    def GetAttributes(self):
        for attr in self.attribs:
            yield attr
        
    def GetVisualProperty(self, key):
        if key == 'CHILDREN':
            node = self.node()
            if node is None:
                return []
            v = []
            for vi in node.GetChilds():
                o = {}
                o['icon'] = vi.GetObject().GetType().GetIcon()
                o['name'] = vi.GetObject().GetName()
                v.append(o)
            return v
        attr = self.type.GetVisAttr(key)
        type = self.type.GetAttribute(attr)
        val = self.attribs[attr]
        if type[0] == 'attrs':
            v = []
            for vi in val:
                s = ''
                o = {}
                if vi['scope'] == 'private':
                    o['scope'] = '-'
                elif vi['scope'] == 'public':
                    o['scope'] = '+'
                elif vi['scope'] == 'protected':
                    o['scope'] = '#'
                l = vi['name']
                if 'type' in vi and vi['type']:
                    l += ": "+vi['type']
                if 'initial' in vi and vi['initial']:
                    l += " = "+vi['initial']
                o['line'] = l
                v.append(o)
            val = v
        elif type[0] == 'opers':
            v = []
            for vi in val:
                s = ''
                o = {}
                if vi['scope'] == 'private':
                    o['scope'] = '-'
                elif vi['scope'] == 'public':
                    o['scope'] = '+'
                elif vi['scope'] == 'protected':
                    o['scope'] = '#'
                l = vi['name']
                l += "("
                if 'params' in vi and vi['params']:
                    l += vi['params']
                l += ")"
                if 'type' in vi and vi['type']:
                    l += ": "+vi['type']
                o['line'] = l
                v.append(o)
            val = v
        return val

    def Paint(self, context):
        self.type.Paint(context)

    def RemoveAttribute(self, key):
        self.revision += 1
        if self.attribs.has_key(key):
            del self.attribs[key]
        else:
            raise ElementAttributeError("KeyError")
    
    def HasAttribute(self, key):
        return key in self.attribs
            
    def SetAttribute(self, key, value):
        self.revision += 1
        self.attribs[key] = self.type.TypeCastAttribute(key, value)
        
    def Disconnect(self, connection):
        connection.Disconnect()
        
    def RemoveConnection(self, connection):
        self.revision += 1
        if connection in self.connections:
            self.connections.remove(connection)
        else:
            raise ConnectionError("ConnectionNotFound")
     
    # Automaticke generovanie mena elementu 
    # pomocou cprojNode zisti mena elementov na rovnakej urovni
    # ak meno uz existuje (a je rovnaky typ), objekt sa premenuje
    def Assign(self, cprojNode):
        if not self.type.GetGenerateName():
            return
        self.revision += 1
        self.node = weakref.ref(cprojNode)
        if cprojNode.parent is not None:
            id = 1
            # zisti nazvy / typy deti, porovnaj a pripadne sa premenuj
            checkNames = True
            while checkNames :
                checkNames = False
                for child in cprojNode.parent.childs:
                    if child.GetName() == self.GetName() and child.GetObject().GetType() is self.GetType():
                        nName = self.GetName()
                        while nName[-1].isdigit(): # useknem cisla
                            nName = nName[:-1]
                        if nName.endswith(' '):
                            nName = nName + str(id)
                        else:
                            nName = nName + ' ' + str(id)
                        self.SetAttribute('Name', nName)
                        id = id + 1
                        checkNames = True #znovu prekontroluj nazvy
            cprojNode.Change()
