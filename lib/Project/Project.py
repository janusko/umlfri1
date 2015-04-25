from lib.Depend.libxml import etree, builder
from lib.Domains import CDomainObject, CDomainType
from lib.Domains.AttributeConditions import BuildParam
from lib.Domains.Modifications.DeleteAttributeModification import CDeleteAttributeModification
from lib.Domains.Modifications.DomainAttributeModification import DomainAttributeModificationType
from lib.Domains.Modifications.ReplaceAttributeModification import CReplaceAttributeModification
from lib.Domains.ModifiedType import CModifiedDomainType
from lib.datatypes import CFont, CColor

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

xmlschema_doc = [
    ((1,0,1), etree.parse(os.path.join(SCHEMA_PATH, "umlproject_1.0.1.xsd"))),
    ((1,1,0), etree.parse(os.path.join(SCHEMA_PATH, "umlproject_1.1.0.xsd"))),
    ((1,2,0), etree.parse(os.path.join(SCHEMA_PATH, "umlproject_1.2.0.xsd"))),
    ((1,3,0), etree.parse(os.path.join(SCHEMA_PATH, "umlproject_1.3.0.xsd")))
]
xmlschemas = []
for version, doc in xmlschema_doc:
    xmlschemas.append((version, etree.XMLSchema(doc)))


class CProject(CBaseObject):
    SaveVersion = (1, 3, 0) # save file format version
    def __init__(self, addonManager):
        self.root = None
        
        self.__addonManager = addonManager
        self.__metamodel = None
        self.__addon = None
        self.__domainObject = None
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

    def GetDomainObject(self):
        return self.__domainObject

    def SetRoot(self, value):
        self.root = value
    
    def GetRoot(self):
        return self.root
    
    def GetFileName(self):
        return self.filename
    
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
        metamodelRoots = []
        def _search(node):
            obj = node.GetObject()
            elements.add(obj)
            for con in obj.GetConnections():
                connections.add(con)
            for diagram in node.GetDiagrams():
                diagrams.add(diagram)
            for chld in node.GetChilds():
                _search(chld)
            if node.IsModifiedMetamodelRoot():
                metamodelRoots.append(node)
        
        _search(node)
        return elements, connections, diagrams, metamodelRoots
    
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
        
        try:
            if isZippedFile :
                fZip = ZipFile(filename, 'w', ZIP_DEFLATED)
                fZip.writestr('content.xml', CProject.XmlToStr(rootNode))
                fZip.close()
            else:
                f = open(filename, 'w')
                f.write(CProject.XmlToStr(rootNode))
                f.close()
        except IOError as err:
            if err.errno == 2: # IOError: [Errno 2] No such file or directory
                raise ProjectError("Specified folder/file does not exist:\n" + err.filename)
            elif err.errno ==  13: # IOError: [Errno 13] Permission denied
                raise ProjectError("You don't have permission to write:\n" + err.filename)
        
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
                        dw, dh = e.GetSize()
                        elementNode = etree.Element(UMLPROJECT_NAMESPACE+'element', id=unicode(e.GetObject().GetUID()), x=unicode(int(pos[0])), y=unicode(int(pos[1])), dw=unicode(int(dw)), dh=unicode(int(dh)))

                        for num, info in enumerate(e.GetAllLabelPositions()):
                            elementNode.append(etree.Element(UMLPROJECT_NAMESPACE+'label',
                                dict(map(lambda x: (x[0], unicode(x[1])), info.iteritems())), #transform {key:value, ...} -> {key:unicode(value), ...}
                                num=unicode(num)))

                        diagramNode.append(elementNode)
                        
                    for c in area.GetConnections():
                        if c is None or c.GetObject() is None or c.GetObject().GetSource() is None or c.GetObject().GetDestination() is None:
                            print "WARNING: false ConnectionVisual"
                            continue
                        connectionNode = etree.Element(UMLPROJECT_NAMESPACE+'connection', id=unicode(c.GetObject().GetUID()))
                        for pos in c.GetMiddlePoints():
                            pointNode = etree.Element(UMLPROJECT_NAMESPACE+'point', x=unicode(int(pos[0])), y=unicode(int(pos[1])))
                            connectionNode.append(pointNode)
                            
                        for num, info in enumerate(c.GetAllLabelPositions()):
                            connectionNode.append(etree.Element(UMLPROJECT_NAMESPACE+'label', 
                                dict(map(lambda x: (x[0], unicode(x[1])), info.iteritems())), #transform {key:value, ...} -> {key:unicode(value), ...}
                                num=unicode(num)))
                                
                        diagramNode.append(connectionNode)
                    diagramsNode.append(diagramNode)
            nodeNode.append(diagramsNode)
            element.append(nodeNode)
        
        elements, connections, diagrams, metamodelRoots = self.searchCE(self.root)
        
        rootNode = etree.XML('<umlproject saveversion="%s" xmlns="http://umlfri.kst.fri.uniza.sk/xmlschema/umlproject.xsd"></umlproject>'%('.'.join(str(i) for i in self.SaveVersion)))
        
        metamodelNode = etree.Element(UMLPROJECT_NAMESPACE+'metamodel')
        domainModificationNode = etree.Element(UMLPROJECT_NAMESPACE+'domainmodifications')
        domainNode = etree.Element(UMLPROJECT_NAMESPACE+'domain')
        modificationBundlesNode = etree.Element(UMLPROJECT_NAMESPACE+'modificationbundles')
        objectsNode = etree.Element(UMLPROJECT_NAMESPACE+'objects')
        connectionsNode = etree.Element(UMLPROJECT_NAMESPACE+'connections')
        diagramsNode = etree.Element(UMLPROJECT_NAMESPACE+'diagrams')
        projtreeNode = etree.Element(UMLPROJECT_NAMESPACE+'projecttree')
        counterNode = etree.Element(UMLPROJECT_NAMESPACE+'counters')
        
        # metamodel informations
        metamodelUriNode = etree.Element(UMLPROJECT_NAMESPACE+'uri')
        metamodelUriNode.text = self.GetMetamodel().GetUri()
        metamodelVersionNode = etree.Element(UMLPROJECT_NAMESPACE+'version')
        metamodelVersionNode.text = self.GetMetamodel().GetVersionString()
        
        metamodelNode.append(metamodelUriNode)
        metamodelNode.append(metamodelVersionNode)
        rootNode.append(metamodelNode)

        domainType = self.__domainObject.GetType()
        if isinstance(domainType, CModifiedDomainType):
            modifications = domainType.GetModifications()
            self.__CreateAttributeModificationsXml(domainModificationNode, modifications)

        rootNode.append(domainModificationNode)

        domainNode.append(SaveDomainObjectInfo(self.__domainObject.GetSaveInfo()))
        rootNode.append(domainNode)

        rootNode.append(modificationBundlesNode)

        for node in metamodelRoots:
            bundles = node.GetMetamodel().GetModificationBundles()
            elementNode = etree.SubElement(modificationBundlesNode, UMLPROJECT_NAMESPACE+'element', id=unicode(node.GetObject().GetUID()))
            for bundle in bundles:
                bundleNode = etree.SubElement(elementNode, UMLPROJECT_NAMESPACE+'bundle', name=bundle.GetName())
                for domain, modifications in bundle.GetDomainModifications().iteritems():
                    domainModificationNode = etree.SubElement(bundleNode, UMLPROJECT_NAMESPACE+'domain', id=domain)
                    self.__CreateAttributeModificationsXml(domainModificationNode, modifications)

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
        xmlschema = xmlschemas[-1][1]
        if not xmlschema.validate(rootNode):
            if __debug__:
                raise XMLError("Schema validation failed\n" + str(xmlschema.error_log.last_error))
            else:
                raise XMLError("Schema validation failed")
        
        #make human-friendly tree
        Indent(rootNode)
        
        return rootNode


    def __CreateAttributeModificationsXml(self, parentNode, modifications):
        nodes = self.__CreateAttributeModificationsNodes(modifications)
        for node in nodes:
            parentNode.append(node)

    def __CreateAttributeModificationsNodes(self, modifications):
        for attributeModification in modifications:
            if attributeModification.GetType() == DomainAttributeModificationType.DELETE:
                attributeNode = etree.Element(UMLPROJECT_NAMESPACE+'deleteattribute')

            elif attributeModification.GetType() == DomainAttributeModificationType.REPLACE:
                attributeNode = etree.Element(UMLPROJECT_NAMESPACE+'replaceattribute')
                props = attributeModification.GetAttributeProperties()
                attributeNode.set('name', unicode(props['name']))

                if 'condition' in props:
                    condition = str(props['condition'])
                    attributeNode.append(builder.E(UMLPROJECT_NAMESPACE+'condition', unicode(condition)))


                type = props['type']
                if props.get('hidden', False):
                    attributeNode.set('hidden', 'true')

                if not CDomainType.IsDomainAtomic(type):
                    attributeNode.set('type', type)
                else:
                    typeNode = etree.SubElement(attributeNode, UMLPROJECT_NAMESPACE+type.title())

                    if type in ('int', 'float'):
                        if 'min' in props:
                            typeNode.append(builder.E(UMLPROJECT_NAMESPACE+'Min', unicode(str(props['min']))))
                        if 'max' in props:
                            typeNode.append(builder.E(UMLPROJECT_NAMESPACE+'Max', unicode(str(props['max']))))

                    if 'enum' in props:
                        if type == 'enum':
                            enumNode = typeNode
                        else:
                            enumNode = etree.SubElement(typeNode, UMLPROJECT_NAMESPACE+'Enum')
                        for value in props['enum']:
                            enumNode.append(builder.E(UMLPROJECT_NAMESPACE+'Value', unicode(value)))

                    if type in ('str', 'text') and 'restricted' in props:
                        typeNode.append(builder.E(UMLPROJECT_NAMESPACE+'Restriction', unicode(props['restricted'])))

                    if type == 'list':
                        typeNode.set('type', unicode(props['list']['type']))

                    defaultValue = props.get('default', None)
                    if type != 'list' and defaultValue:
                        typeNode.set('default', unicode(str(defaultValue)))
            else:
                raise ProjectError('Unknown domain attribute modification type "%s"' % attributeModification.GetType())

            attributeNode.set('id', unicode(attributeModification.GetAttributeID()))
            yield attributeNode
    
    def __CreateTree(self, ListObj, ListCon, ListDiag, root, parentNode, savever):
        for elem in root:
            if elem.tag == UMLPROJECT_NAMESPACE+'childs':
                for node in elem:
                    elemid = node.get("id")
                    if elemid in ListObj:
                        proNode = CProjectNode(parentNode,ListObj[elemid])
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
                            if 'default' in area.attrib and area.attrib['default'].lower() in ('1', 'true'):
                                self.defaultDiagram = diagram
                            parentNode.AddDiagram(diagram)
                            for pic in area:
                                if pic.tag == UMLPROJECT_NAMESPACE+"element":
                                    elemid = pic.get("id")
                                    if elemid in ListObj:
                                        # backward compatibility with old project files
                                        hasDeltaSize = False
                                        if savever < (1, 2, 0):
                                            hasDeltaSize = True
                                        element = CElement(diagram,ListObj[elemid],True,hasDeltaSize)
                                        element.SetPosition((int(pic.get("x")),int(pic.get("y"))))
                                        dw = int(pic.get("dw"))
                                        dh = int(pic.get("dh"))
                                        element.SetSize((dw, dh))
                                        for label in pic:
                                            data = dict(label.items())
                                            del data["num"]
                                            element.RestoreLabelPosition(int(label.get("num")), data)
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
        ListBundles = {}

        DomainObjectSaveInfo = None
        DomainModifications = None
        
        if storage is not None:
            self.isZippedFile = True
            data = storage.read_file(filename)
        elif is_zipfile(filename):
            self.isZippedFile = True
            file = ZipFile(filename,'r')
            data = file.read('content.xml')
        else:
            self.isZippedFile = False
            try:
                file = open(filename, 'r')
                data = file.read()
            except IOError as err:
                if err.errno == 2:
                    raise ProjectError("Specified folder / file does not exist:\n" + err.filename)
        
        if copy:
            self.filename = None
        else:
            self.filename = filename
        
        self.defaultDiagram = None
        
        root = etree.XML(data)
        
        savever = tuple(int(i) for i in root.get('saveversion').split('.'))
        if savever > self.SaveVersion:
            raise ProjectError("This version of UML .FRI cannot open this file")
        
        
        #xml (version) file is validate with xsd schema (metamodel.xsd)
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

        from lib.Addons.Metamodel.Modifications.ModificationBundle import CMetamodelModificationBundle

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

                self.__domainObject = CDomainObject(self.__metamodel.GetDomain())

            elif element.tag == UMLPROJECT_NAMESPACE+'domainmodifications':
                DomainModifications = self.__LoadAttributeModifications(element)

            elif element.tag == UMLPROJECT_NAMESPACE+'domain':
                DomainObjectSaveInfo = CProject.__LoadDomainObjectInfo(element[0])

            elif element.tag == UMLPROJECT_NAMESPACE+'modificationbundles':
                for elementNode in element:
                    id = elementNode.get('id')
                    bundles = []
                    ListBundles[id] = bundles
                    for bundleNode in elementNode:
                        name = bundleNode.get('name')
                        domains = {}
                        for domainNode in bundleNode:
                            domainId = domainNode.get('id')
                            domains[domainId] = self.__LoadAttributeModifications(domainNode)

                        bundles.append(CMetamodelModificationBundle(name, None, domains))

            elif element.tag == UMLPROJECT_NAMESPACE+'objects':
                for subelem in element:
                    if subelem.tag == UMLPROJECT_NAMESPACE+'object':
                        id = subelem.get("id")
                        object = CElementObject(self.GetMetamodel().GetElementFactory().GetElement(subelem.get("type")))
                        object.SetUID(id)
                        ListObj[id] = (object, CProject.__LoadDomainObjectInfo(subelem[0]))
            
            elif element.tag == UMLPROJECT_NAMESPACE+'connections':
                for connection in element:
                    if connection.tag == UMLPROJECT_NAMESPACE+'connection':
                        conFrom = connection.get("source")
                        conTo = connection.get("destination")
                        if conFrom in ListObj and conTo in ListObj:
                            id = connection.get("id")
                            source = ListObj[conFrom][0]
                            destination = ListObj[conTo][0]
                            con = CConnectionObject(self.GetMetamodel().GetConnectionFactory().GetConnection(connection.get("type")),source,destination)
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
                        listObj = {id: obj for id, (obj, x) in ListObj.iteritems()}
                        proNode = CProjectNode(None,listObj[elemid],self)
                        self.SetRoot(proNode)
                        self.__CreateTree(listObj, ListCon, ListDiag, subelem, proNode, savever)
            
            elif element.tag == UMLPROJECT_NAMESPACE + 'counters':
                for item in element:
                    if self.GetMetamodel().GetElementFactory().HasType(item.get('id')):
                        self.GetMetamodel().GetElementFactory().GetElement(item.get('id')).SetCounter(int(item.get('value')))
                    elif self.GetMetamodel().GetDiagramFactory().HasType(item.get('id')):
                        self.GetMetamodel().GetDiagramFactory().GetDiagram(item.get('id')).SetCounter(int(item.get('value')))

        from lib.Commands.Project.ApplyModificationBundles import CApplyModificationBundlesCommand
        from lib.Commands.Project.ModifyProjectDomain import CModifyProjectDomainCommand

        if DomainModifications:
            CModifyProjectDomainCommand(self, DomainModifications).Do()

        if DomainObjectSaveInfo is not None:
            self.__domainObject.SetSaveInfo(DomainObjectSaveInfo)

        for nodeId, bundles in reversed(ListBundles.items()):
            node = ListObj[nodeId][0].GetNode()
            CApplyModificationBundlesCommand(node, bundles).Do()

        for obj, saveinfo in ListObj.itervalues():
            obj.SetSaveInfo(saveinfo)

        self.__addonManager.GetPluginManager().GetPluginAdapter().gui_project_opened(self)

    def __LoadAttributeModifications(self, parentNode):
        modifications = []

        for attributeModificationNode in parentNode:
            attributeID = attributeModificationNode.get('id')
            tag = attributeModificationNode.tag
            if tag == UMLPROJECT_NAMESPACE + 'deleteattribute':
                modifications.append(CDeleteAttributeModification(attributeID))
            elif tag == UMLPROJECT_NAMESPACE + 'replaceattribute':
                props = {'name': attributeModificationNode.get('name')}
                type = attributeModificationNode.get('type')
                props['hidden'] = attributeModificationNode.get('hidden') in ('true', '1')
                conditionNode = attributeModificationNode.find(UMLPROJECT_NAMESPACE+'condition')
                if conditionNode is not None:
                    props['condition'] = BuildParam(conditionNode.text)

                if type is not None:
                    props['type'] = type
                    props['default'] = None
                else:
                    count = len(attributeModificationNode.getchildren())
                    child = attributeModificationNode[count - 1]
                    type = child.tag[child.tag.rfind('}') + 1:]
                    props['type'] = type.lower()

                    restrictions = {}

                    trycast = lambda type, value: None if value is None else type(value)

                    def load_restriction(elementName, res, type):
                        node = attributeModificationNode.find(UMLPROJECT_NAMESPACE + elementName)
                        if node is not None:
                            restrictions[res] = trycast(type, node.text)

                    def load_default_value(type):
                        props['default'] = trycast(type, child.get('default'))

                    numberTypes = {'Int': int, 'Float': float}
                    otherTypes = {'Font': CFont, 'Color': CColor}

                    if type in numberTypes:
                        numberType = numberTypes[type]
                        load_restriction('Min', 'min', numberType)
                        load_restriction('Max', 'max', numberType)
                        load_default_value(numberType)
                    elif type in otherTypes:
                        otherType = otherTypes[type]
                        load_default_value(otherType)
                    elif type == 'Bool':
                        props['default'] = trycast(lambda x: x == 'True', child.get('default'))
                    elif type in ('Text', 'Str'):
                        load_restriction('Restriction', 'restricted', str)
                        load_default_value(str)

                    if type == 'Enum':
                        enumChild = child
                        load_default_value(str)
                    else:
                        enumChild = child.find(UMLPROJECT_NAMESPACE + 'Enum')

                    if enumChild:
                        for option in enumChild:
                            if option.tag == UMLPROJECT_NAMESPACE + 'Value':
                                value = option.text
                                if value is None:
                                    value = ''
                                props.setdefault('enum', []).append(value)

                    if type == 'List':
                        props['list'] = {'type': child.get('type')}

                modifications.append(CReplaceAttributeModification(attributeID, props))

        return modifications
