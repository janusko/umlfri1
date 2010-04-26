from lib.Depend.etree import etree, HAVE_LXML

from lib.lib import XMLEncode, Indent
from ProjectNode import CProjectNode
from cStringIO import StringIO
from zipfile import ZipFile, ZIP_STORED, ZIP_DEFLATED, is_zipfile
from lib.Exceptions.UserException import *
from lib.Exceptions.DevException import DomainObjectError
from lib.Drawing import CElement
from lib.Drawing import CConnection
from lib.Elements.Type import CElementType
from lib.Elements.Object import CElementObject
from lib.Connections.Object import CConnectionObject
from lib.Drawing import CDiagram
import os.path
from lib.consts import UMLPROJECT_NAMESPACE, PROJECT_EXTENSION, PROJECT_CLEARXML_EXTENSION
from lib.Distconfig import SCHEMA_PATH
from lib.Base import CBaseObject

#if lxml.etree is imported successfully, we use xml validation with xsd schema
if HAVE_LXML:
    xmlschema_doc = [
        ((1,0,1), etree.parse(os.path.join(SCHEMA_PATH, "umlproject_1.0.1.xsd"))),
        ((1,1,0), etree.parse(os.path.join(SCHEMA_PATH, "umlproject_1.1.0.xsd"))),
    ]
    xmlschemas = []
    for version, doc in xmlschema_doc:
        xmlschemas.append((version, etree.XMLSchema(doc)))


class CProject(CBaseObject):
    SaveVersion = (1, 1, 0) # save file format version
    def __init__(self, addonManager):
        self.root = None
        
        self.__addonManager = addonManager
        self.__metamodel = None
        self.__addon = None
        self.defaultDiagram = None
        
        self.filename = None
        self.isZippedFile = None
    
    def GetAddon(self):
        return self.__addon
    
    def GetDefaultDiagrams(self):
        if self.defaultDiagram is not None:
            yield self.defaultDiagram
    
    def AddDefaultDiagram(self, diagram):
        self.defaultDiagram = diagram
    
    def DeleteDefaultDiagram(self, diagram):
        if self.defaultDiagram is diagram:
            self.defaultDiagram = None
    
    def GetDiagrams(self):
        stack = [self.root]
        diagrams = []
        while len(stack) > 0:
            node = stack.pop(0)
            for d in node.GetDiagrams():
                diagrams.append(d)
            stack += node.GetChilds()
        return diagrams
        
    
    def GetMetamodel(self):
        return self.__metamodel
    
    def SetRoot(self, value):
        self.root = value
    
    def GetRoot(self):
        return self.root
    
    def GetFileName(self):
        return self.filename
    
    def GetNode(self, path):
        node = self.root
        
        #e.g. path = Project:Package/New Class diagram:=Diagram=
        k = path.split('/')[0]
        i,j = k.split(':')
        
        if i == self.root.GetName() and j == self.root.GetType() and len(path.split('/')) == 1:
            return self.root
        
        if i == self.root.GetName() and j == self.root.GetType():
            for i in path.split('/')[1:]:
                j, k  = i.rsplit(':', 1)
                if k == "=Diagram=":
                    return node
                else:
                    node = node.GetChild(j, k)
                if node is None:
                    raise ProjectError("BadPath")
            return node
        raise ProjectError("BadPath3")
    
    
    def Find(self, name):
        stack = [self.root]
        while len(stack) > 0:
            node = stack.pop(0)
            if node.GetName() == name:
                return node
            stack += node.GetChilds()
        return None

    def AddNode(self, node, parent):
        if parent is None:
            self.root = node
        else:
            parent.AddChild(node)
            

    def MoveNode(self, node, newParent):
        node.GetParent(node).RemoveChild(node)
        node.SetParent(newParent)
        newParent.AddChild(node)
              

    def RemoveNode(self, node):
        node.GetParent().RemoveChild(node)
   
    # search for all connections and elements under given node
    def searchCE(self, node): 
        elements = set()
        connections = set()
        diagrams = set()
        def _search(node):
            obj = node.GetObject()
            elements.add(obj)
            for con in obj.GetConnections():
                connections.add(con)
            for diagram in node.GetDiagrams():
                diagrams.add(diagram)
            for chld in node.GetChilds():
                _search(chld)
        
        _search(node)
        return elements, connections, diagrams
    
    def SaveProject(self, filename = None, isZippedFile = None):
        if filename is None:
            filename = self.filename
        else:
            self.filename = filename
        
        
        if isZippedFile is None:
            isZippedFile = self.isZippedFile
        else:
            self.isZippedFile = isZippedFile
        
        rootNode = self.GetSaveXml()
        
        if isZippedFile :
            fZip = ZipFile(filename, 'w', ZIP_DEFLATED)
            fZip.writestr('content.xml', CProject.XmlToStr(rootNode))
            fZip.close()
        else:
            f = open(filename, 'w')
            f.write(CProject.XmlToStr(rootNode))
            f.close()
        
    @staticmethod
    def XmlToStr(rootNode):
        return '<?xml version="1.0" encoding="utf-8"?>\n'+etree.tostring(rootNode, encoding='utf-8')
        
    def GetSaveXml(self):
        assert self.__metamodel is not None
        
        def SaveDomainObjectInfo(data, name=None):
            if isinstance(data, dict):
                element = etree.Element(UMLPROJECT_NAMESPACE+'dict')
                d = list(data.iteritems())
                d.sort()
                for key, value in d:
                    element.append(SaveDomainObjectInfo(value, key))
            elif isinstance(data, list):
                element = etree.Element(UMLPROJECT_NAMESPACE+'list')
                for value in data:
                    element.append(SaveDomainObjectInfo(value))
            elif isinstance(data, (str, unicode)):
                element = etree.Element(UMLPROJECT_NAMESPACE+'text')
                element.text = data
            else:
                raise ProjectError("unknown data format")
            if name:
                element.set('name', name)
            return element
        
        def savetree(node, element):
            nodeNode = etree.Element(UMLPROJECT_NAMESPACE+'node', id=unicode(node.GetObject().GetUID()))
            if node.HasChild():
                childsNode = etree.Element(UMLPROJECT_NAMESPACE+'childs')
                for chld in node.GetChilds():
                    savetree(chld, childsNode)
                nodeNode.append(childsNode)
                
            diagramsNode = etree.Element(UMLPROJECT_NAMESPACE+'diagrams')
            if node.HasDiagram():
                for area in node.GetDiagrams():
                    diagramNode = etree.Element(UMLPROJECT_NAMESPACE+'diagram', id=unicode(area.GetUID()))
                    if area is self.defaultDiagram:
                        diagramNode.attrib['default'] = 'true'
                    for e in area.GetElements():
                        pos = e.GetPosition()
                        dw, dh = e.GetSizeRelative()
                        elementNode = etree.Element(UMLPROJECT_NAMESPACE+'element', id=unicode(e.GetObject().GetUID()), x=unicode(pos[0]), y=unicode(pos[1]), dw=unicode(dw), dh=unicode(dh))
                        diagramNode.append(elementNode)
                        
                    for c in area.GetConnections():
                        if c is None or c.GetObject() is None or c.GetObject().GetSource() is None or c.GetObject().GetDestination() is None:
                            print "WARNING: false ConnectionVisual"
                            continue
                        connectionNode = etree.Element(UMLPROJECT_NAMESPACE+'connection', id=unicode(c.GetObject().GetUID()))
                        for pos in c.GetMiddlePoints():
                            pointNode = etree.Element(UMLPROJECT_NAMESPACE+'point', x=unicode(pos[0]), y=unicode(pos[1]))
                            connectionNode.append(pointNode)
                            
                        for num, info in enumerate(c.GetAllLabelPositions()):
                            connectionNode.append(etree.Element(UMLPROJECT_NAMESPACE+'label', 
                                dict(map(lambda x: (x[0], unicode(x[1])), info.iteritems())), #transform {key:value, ...} -> {key:unicode(value), ...}
                                num=unicode(num)))
                                
                        diagramNode.append(connectionNode)
                    diagramsNode.append(diagramNode)
            nodeNode.append(diagramsNode)
            element.append(nodeNode)
        
        elements, connections, diagrams = self.searchCE(self.root)
        
        rootNode = etree.XML('<umlproject saveversion="%s" xmlns="http://umlfri.kst.fri.uniza.sk/xmlschema/umlproject.xsd"></umlproject>'%('.'.join(str(i) for i in self.SaveVersion)))
        
        metamodelNode = etree.Element(UMLPROJECT_NAMESPACE+'metamodel')
        objectsNode = etree.Element(UMLPROJECT_NAMESPACE+'objects')
        connectionsNode = etree.Element(UMLPROJECT_NAMESPACE+'connections')
        diagramsNode = etree.Element(UMLPROJECT_NAMESPACE+'diagrams')
        projtreeNode = etree.Element(UMLPROJECT_NAMESPACE+'projecttree')
        counterNode = etree.Element(UMLPROJECT_NAMESPACE+'counters')
        
        # metamodel informations
        metamodelUriNode = etree.Element(UMLPROJECT_NAMESPACE+'uri')
        metamodelUriNode.text = self.GetMetamodel().GetUri()
        metamodelVersionNode = etree.Element(UMLPROJECT_NAMESPACE+'version')
        metamodelVersionNode.text = self.GetMetamodel().GetVersion()
        
        metamodelNode.append(metamodelUriNode)
        metamodelNode.append(metamodelVersionNode)
        rootNode.append(metamodelNode)
        
        elements = list(elements)
        elements.sort(key = CBaseObject.GetUID)
        for object in elements:
            objectNode = etree.Element(UMLPROJECT_NAMESPACE+'object', type=unicode(object.GetType().GetId()), id=unicode(object.GetUID()))
            objectNode.append(SaveDomainObjectInfo(object.GetSaveInfo()))
            objectsNode.append(objectNode)
            
        rootNode.append(objectsNode)
        
        connections = list(connections)
        connections.sort(key = CBaseObject.GetUID)
        for connection in connections:
            if connection is None or connection.GetSource() is None or connection.GetDestination() is None:
                print "WARNING: False connection object"
                continue
            connectionNode = etree.Element(UMLPROJECT_NAMESPACE+'connection', type=unicode(connection.GetType().GetId()), id=unicode(connection.GetUID()), source=unicode(connection.GetSource().GetUID()), destination=unicode(connection.GetDestination().GetUID()))
            connectionNode.append(SaveDomainObjectInfo(connection.GetSaveInfo()))
            connectionsNode.append(connectionNode)
        
        rootNode.append(connectionsNode)
        
        diagrams = list(diagrams)
        diagrams.sort(key = CBaseObject.GetUID)
        for diagram in diagrams:
            diagramNode = etree.Element(UMLPROJECT_NAMESPACE + 'diagram', id=unicode(diagram.GetUID()), type=unicode(diagram.GetType().GetId()))
            diagramNode.append(SaveDomainObjectInfo(diagram.GetSaveInfo()))
            diagramsNode.append(diagramNode)
            
        rootNode.append(diagramsNode)
        
        savetree(self.root, projtreeNode)
        rootNode.append(projtreeNode)
        
        for type in self.GetMetamodel().GetElementFactory().IterTypes():
            counterNode.append(etree.Element(UMLPROJECT_NAMESPACE+'count', id = type.GetId(), value = unicode(type.GetCounter())))
        for type in self.GetMetamodel().GetDiagramFactory():
            counterNode.append(etree.Element(UMLPROJECT_NAMESPACE+'count', id = type.GetId(), value = unicode(type.GetCounter())))
        
        rootNode.append(counterNode)
        
        #xml tree is validate with xsd schema (recentfile.xsd)
        if HAVE_LXML:
            xmlschema = xmlschemas[-1][1]
            if not xmlschema.validate(rootNode):
                if __debug__:
                    raise XMLError("Schema validation failed\n" + str(xmlschema.error_log.last_error))
                else:
                    raise XMLError("Schema validation failed")
        
        #make human-friendly tree
        Indent(rootNode)
        
        return rootNode
    
    
    def __CreateTree(self, ListObj, ListCon, ListDiag, root, parentNode, savever):
        for elem in root:
            if elem.tag == UMLPROJECT_NAMESPACE+'childs':
                for node in elem:
                    elemid = node.get("id")
                    if elemid in ListObj:
                        proNode = CProjectNode(parentNode,ListObj[elemid],parentNode.GetPath() + "/" + ListObj[elemid].GetName() + ":" + ListObj[elemid].GetType().GetId())
                        self.AddNode(proNode,parentNode)
                        self.__CreateTree(ListObj, ListCon, ListDiag, node, proNode, savever)
                    else:
                        # show warning
                        pass
                    
            elif elem.tag == UMLPROJECT_NAMESPACE+'diagrams':
                for area in elem:
                    
                    if area.tag == UMLPROJECT_NAMESPACE+'diagram':
                        if savever < (1, 1, 0):
                            diagram = CDiagram(self.GetMetamodel().GetDiagramFactory().GetDiagram(area.get("type")),area.get("name"))
                        else:
                            diagid = area.get("id")
                            if diagid in ListDiag:
                                diagram = ListDiag[diagid]
                            else:
                                diagram = None
                        
                        if diagram is not None:
                            diagram.SetPath(parentNode.GetPath() + "/" + diagram.GetName() + ":=Diagram=")
                            if 'default' in area.attrib and area.attrib['default'].lower() in ('1', 'true'):
                                self.defaultDiagram = diagram
                            parentNode.AddDiagram(diagram)
                            for pic in area:
                                if pic.tag == UMLPROJECT_NAMESPACE+"element":
                                    elemid = pic.get("id")
                                    if elemid in ListObj:
                                        element = CElement(diagram,ListObj[elemid],True)
                                        element.SetPosition((int(pic.get("x")),int(pic.get("y"))))
                                        dw = int(pic.get("dw"))
                                        dh = int(pic.get("dh"))
                                        element.SetSizeRelative((dw, dh))
                                    else:
                                        # show warning
                                        pass
                                elif pic.tag == UMLPROJECT_NAMESPACE+"connection":
                                    conid = pic.get("id")
                                    if conid in ListCon:
                                        for e in diagram.GetElements():
                                            if e.GetObject() is ListCon[conid].GetSource():
                                                source = e
                                            if e.GetObject() is ListCon[conid].GetDestination():
                                                destination = e
                                        conect = CConnection(diagram,ListCon[conid],source,destination,[])
                                        for propCon in pic:
                                            if propCon.tag == UMLPROJECT_NAMESPACE+"point":
                                                conect.AddPoint((int(propCon.get("x")),int(propCon.get("y"))))
                                            elif propCon.tag == UMLPROJECT_NAMESPACE+"label":
                                                data = dict(propCon.items())
                                                del data["num"]
                                                conect.RestoreLabelPosition(int(propCon.get("num")), data)
                                    else:
                                        # show warning
                                        pass
                        else:
                            # show warning
                            pass
        
    @staticmethod
    def __LoadDomainObjectInfo(element):
        '''
        Transform element back to the dictionary readable by 
        L{CDomainObject.SetSaveInfo<lib.Domains.Object.CDomainObject.SetSaveInfo>}
        
        @return: structured dictionary
        @rtype: dict
        '''
        if element.tag == UMLPROJECT_NAMESPACE + 'dict':
            return dict([(item.get('name'), CProject.__LoadDomainObjectInfo(item)) for item in element])
        elif element.tag == UMLPROJECT_NAMESPACE + 'list':
            return [CProject.__LoadDomainObjectInfo(item) for item in element]
        elif element.tag == UMLPROJECT_NAMESPACE + 'text':
            return element.text
        else:
            raise ProjectError("malformed project file")
    
    def CreateProject(self, template):
        template.LoadInto(self)
    
    def LoadProject(self, filename, copy = False, storage = None):
        ListObj = {}
        ListCon = {}
        ListDiag = {}
        
        if storage is not None:
            self.isZippedFile = True
            data = storage.read_file(filename)
        elif is_zipfile(filename):
            self.isZippedFile = True
            file = ZipFile(filename,'r')
            data = file.read('content.xml')
        else:
            self.isZippedFile = False
            file = open(filename, 'r')
            data = file.read()
        
        if copy:
            self.filename = None
        else:
            self.filename = filename
        
        self.defaultDiagram = None
        
        root = etree.XML(data)
        
        savever = tuple(int(i) for i in root.get('saveversion').split('.'))
        if savever > self.SaveVersion:
            raise ProjectError("this version of UML .FRI cannot open this file")
        
        
        #xml (version) file is validate with xsd schema (metamodel.xsd)
        if HAVE_LXML:
            xmlschema = xmlschemas[0][1]
            for ver, sch in xmlschemas:
                if ver > savever:
                    break
                xmlschema = sch
            if not xmlschema.validate(root):
                if __debug__:
                    raise XMLError("Schema validation failed\n" + str(xmlschema.error_log.last_error))
                else:
                    raise XMLError("Schema validation failed")
        
        for element in root:
            if element.tag == UMLPROJECT_NAMESPACE+'metamodel':
                uri = None
                version = None
                
                for item in element:
                    if item.tag == UMLPROJECT_NAMESPACE+'uri':
                        uri = item.text
                    elif item.tag == UMLPROJECT_NAMESPACE+'version':
                        version = item.text
                
                if not uri or not version:
                    raise XMLError("Bad metamodel definition")
                
                self.__addon = None
                
                addon = self.__addonManager.GetAddon(uri)
                
                if addon is None and self.isZippedFile and ('metamodel/addon.xml' in file.namelist()):
                    if storage is None:
                        addon = self.__addonManager.LoadAddon(os.path.join(filename, 'metamodel'))
                    else:
                        addon = self.__addonManager.LoadAddon(storage.subopen('metamodel'))
                    if uri not in addon.GetUris():
                        addon = None
                    self.__addon = addon
                
                if addon is None:
                    raise ProjectError("Project using unknown metamodel")
                if addon.GetType() not in ('metamodel', 'composite'):
                    raise ProjectError("Given URI identifier is not metamodel")
                self.__metamodel = addon.GetComponent().LoadMetamodel()
                if self.__metamodel is None:
                    raise ProjectError("This metamodel is disabled")
                
            elif element.tag == UMLPROJECT_NAMESPACE+'objects':
                for subelem in element:
                    if subelem.tag == UMLPROJECT_NAMESPACE+'object':
                        id = subelem.get("id")
                        object = CElementObject(self.GetMetamodel().GetElementFactory().GetElement(subelem.get("type")))
                        object.SetUID(id)
                        object.SetSaveInfo(CProject.__LoadDomainObjectInfo(subelem[0]))
                        ListObj[id] = object
            
            elif element.tag == UMLPROJECT_NAMESPACE+'connections':
                for connection in element:
                    if connection.tag == UMLPROJECT_NAMESPACE+'connection':
                        conFrom = connection.get("source")
                        conTo = connection.get("destination")
                        if conFrom in ListObj and conTo in ListObj:
                            id = connection.get("id")
                            con = CConnectionObject(self.GetMetamodel().GetConnectionFactory().GetConnection(connection.get("type")),ListObj[conFrom],ListObj[conTo])
                            con.SetUID(id)
                            con.SetSaveInfo(CProject.__LoadDomainObjectInfo(connection[0]))
                            ListCon[id] = con
                        else:
                            # show warning
                            pass
            
            elif savever >= (1, 1, 0) and element.tag == UMLPROJECT_NAMESPACE+'diagrams':
                for diagram in element:
                    if diagram.tag == UMLPROJECT_NAMESPACE + 'diagram':
                        id = diagram.get('id')
                        diag = CDiagram(self.GetMetamodel().GetDiagramFactory().GetDiagram(diagram.get('type')))
                        diag.SetSaveInfo(CProject.__LoadDomainObjectInfo(diagram[0]))
                        diag.SetUID(id)
                        ListDiag[id] = diag
            
            elif element.tag == UMLPROJECT_NAMESPACE+'projecttree':
                for subelem in element:
                    if subelem.tag == UMLPROJECT_NAMESPACE+'node':
                        elemid = subelem.get("id")
                        proNode = CProjectNode(None,ListObj[elemid],ListObj[elemid].GetName() + ":" + ListObj[elemid].GetType().GetId())
                        self.SetRoot(proNode)
                        self.__CreateTree(ListObj, ListCon, ListDiag, subelem, proNode, savever)
            
            elif element.tag == UMLPROJECT_NAMESPACE + 'counters':
                for item in element:
                    if self.GetMetamodel().GetElementFactory().HasType(item.get('id')):
                        self.GetMetamodel().GetElementFactory().GetElement(item.get('id')).SetCounter(int(item.get('value')))
                    elif self.GetMetamodel().GetDiagramFactory().HasType(item.get('id')):
                        self.GetMetamodel().GetDiagramFactory().GetDiagram(item.get('id')).SetCounter(int(item.get('value')))
        
        self.__addonManager.GetPluginManager().GetPluginAdapter().gui_project_opened(self)
