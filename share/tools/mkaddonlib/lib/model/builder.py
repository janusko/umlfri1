from baseContainer import BaseContainer
from delegate import Delegate
#from delegateParameter import DelegateParameter
#from delegateReturn import DelegateReturn
from exception import Exception as ExceptionDefinition
#from exceptionProperty import ExceptionProperty
from interface import Interface
from interfaceMethod import InterfaceMethod
from interfaceMethodParameter import InterfaceMethodParameter
from interfaceMethodReturn import InterfaceMethodReturn
#from interfaceProperty import InterfaceProperty
#from interfacePropertyGetter import InterfacePropertyGetter
#from interfacePropertyIndex import InterfacePropertyIndex
#from interfacePropertyIterator import InterfacePropertyIterator
#from interfacePropertySetter import InterfacePropertySetter
from namespace import Namespace

import os
import os.path

import lxml.etree

class Builder(object):
    __xmlschema = lxml.etree.XMLSchema(
        lxml.etree.parse(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "schema", "publicApi.xsd"))
    )

    __xmldefs = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "publicApi")
    
    __xmlns = "{http://umlfri.org/xmlschema/publicApi.xsd}%s"
    
    def __init__(self):
        self.__rootNamespace = Namespace(None, None)
    
    def parse(self, dir = None):
        if dir is None:
            dir = self.__xmldefs
        
        for f in os.listdir(dir):
            if not f.endswith('.xml'):
                continue
            
            root = lxml.etree.parse(os.path.join(dir, f)).getroot()
            if not self.__xmlschema.validate(root):
                raise SyntaxError(self.__xmlschema.error_log.last_error)
            
            if root.tag == self.__xmlns%'interface':
                self.__parseInterface(root)
            elif root.tag == self.__xmlns%'exception':
                self.__parseException(root)
            elif root.tag == self.__xmlns%'delegate':
                self.__parseDelegate(root)
    
    def finish(self):
        self.__rootNamespace._link(self)
    
    def getRootNamespace(self):
        return self.__rootNamespace
    
    def printStructure(self):
        for child in self.__rootNamespace.children:
            self.__printStructureHelper(child, 0)
    
    def getTypeByName(self, name):
        namespace, name = self.__parseNamespaceAndName(name)
        type = namespace.getChild(name)
        
        if not isinstance(type, (Interface, Delegate, ExceptionDefinition)):
            raise Exception
        
        return type
    
    ################
    ### Interface
    
    def __parseInterface(self, root):
        namespace, name = self.__parseNamespaceAndName(root.attrib['name'])
        try:
            namespace.getChild(name)
        except KeyError:
            pass
        else:
            raise Exception
        
        interface = Interface(
            name,
            namespace,
            base = root.attrib.get('base'),
            abstract = root.attrib.get('abstract', "false").lower() in ("1", "true"),
            documentation = self.__parseDocumentation(root.find('documentation'))
        )
        
        for child in root:
            if child.tag == self.__xmlns%'property':
                self.__parseInterfaceProperty(child, interface)
            elif child.tag == self.__xmlns%'method':
                self.__parseInterfaceMethod(child, interface)
    
    def __parseInterfaceMethod(self, root, interface):
        method = InterfaceMethod(
            root.attrib['name'],
            interface,
            apiName = root.attrib.get('apiname'),
            documentation = self.__parseDocumentation(root.find('documentation'))
        )
        
        for child in root:
            if child.tag == self.__xmlns%'parameter':
                if child.attrib['type'] == 'namedparams':
                    raise Exception
                
                parameter = InterfaceMethodParameter(
                    child.attrib['name'],
                    method,
                    child.attrib['type'],
                    apiName = child.attrib.get('apiname'),
                    required = child.attrib.get('required', "true").lower() in ("1", "true"),
                    default = child.attrib.get('default'),
                    documentation = self.__parseDocumentation(child.find('documentation')),
                )
            elif child.tag == self.__xmlns%'parameterDictionary':
                parameter = InterfaceMethodParameter(
                    child.attrib['name'],
                    method,
                    '*',
                    apiName = child.attrib.get('apiname'),
                    required = True,
                    documentation = self.__parseDocumentation(child.find('documentation')),
                )
            elif child.tag == self.__xmlns%'return':
                returnType = InterfaceMethodReturn(
                    method,
                    child.attrib['type'],
                    iterable = child.attrib.get('iterable', "true").lower() in ("1", "true"),
                    documentation = self.__parseDocumentation(child.find('documentation')),
                )
    
    def __parseInterfaceProperty(self, root, interface):
        pass
    
    ################
    ### Exception
    
    def __parseException(self, root):
        namespace, name = self.__parseNamespaceAndName(root.attrib['name'])
        try:
            namespace.getChild(name)
        except KeyError:
            pass
        else:
            raise Exception
        
        exception = ExceptionDefinition(
            name,
            namespace
        )
        
        # # # TODO
    
    ################
    ### Delegate
    
    def __parseDelegate(self, root):
        namespace, name = self.__parseNamespaceAndName(root.attrib['name'])
        try:
            namespace.getChild(name)
        except KeyError:
            pass
        else:
            raise Exception
        
        exception = Delegate(
            name,
            namespace
        )
        
        # # # TODO
    
    ################
    ### Helpers
    
    def __parseNamespaceAndName(self, fqn):
        symbols = fqn.split('.')
        
        name = symbols.pop()
        
        namespace = self.__rootNamespace
        
        for symbol in symbols:
            try:
                namespace = namespace.getChild(symbol)
                if not isinstance(namespace, Namespace):
                    raise Exception()
            except KeyError:
                namespace = Namespace(symbol, namespace)
        
        return namespace, name
    
    def __parseDocumentation(self, documentation):
        if documentation is None:
            return None
        
        text = documentation.text
        
        return '\n'.join(line.strip() for line in text.strip().split('\n'))
    
    def __printStructureHelper(self, object, level):
        print ('    ' * level) + repr(object), 'with apiName', repr(getattr(object, 'apiName', None))
        
        if isinstance(object, BaseContainer):
            for child in object.children:
                self.__printStructureHelper(child, level + 1)
