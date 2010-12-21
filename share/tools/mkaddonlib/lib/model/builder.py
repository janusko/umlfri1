from baseContainer import BaseContainer
from delegate import Delegate
from delegateParameter import DelegateParameter
from delegateReturn import DelegateReturn
from delegateThrows import DelegateThrows
from exception import Exception as ExceptionDefinition
from exceptionProperty import ExceptionProperty
from interface import Interface
from interfaceMethod import InterfaceMethod
from interfaceMethodParameter import InterfaceMethodParameter
from interfaceMethodReturn import InterfaceMethodReturn
from interfaceMethodThrows import InterfaceMethodThrows
from interfaceProperty import InterfaceProperty
from interfacePropertyGetter import InterfacePropertyGetter
from interfacePropertyIndex import InterfacePropertyIndex
from interfacePropertyIterator import InterfacePropertyIterator
from interfacePropertySetter import InterfacePropertySetter
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
            documentation = self.__parseDocumentation(root.find(self.__xmlns%'documentation'))
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
            mutator = root.attrib.get('mutator', "false").lower() in ("1", "true"),
            transactional = root.attrib.get('transactional', "true").lower() in ("1", "true"),
            documentation = self.__parseDocumentation(root.find(self.__xmlns%'documentation'))
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
                    documentation = self.__parseDocumentation(child.find(self.__xmlns%'documentation')),
                )
            elif child.tag == self.__xmlns%'parameterDictionary':
                parameter = InterfaceMethodParameter(
                    child.attrib['name'],
                    method,
                    '*',
                    apiName = child.attrib.get('apiname'),
                    required = True,
                    documentation = self.__parseDocumentation(child.find(self.__xmlns%'documentation')),
                )
            elif child.tag == self.__xmlns%'return':
                returnType = InterfaceMethodReturn(
                    method,
                    child.attrib['type'],
                    iterable = child.attrib.get('iterable', "true").lower() in ("1", "true"),
                    documentation = self.__parseDocumentation(child.find(self.__xmlns%'documentation')),
                )
            elif child.tag == self.__xmlns%'throws':
                returnType = InterfaceMethodThrows(
                    method,
                    child.attrib['exception'],
                    documentation = self.__parseDocumentation(child.find(self.__xmlns%'documentation')),
                )
    
    def __parseInterfaceProperty(self, root, interface):
        value = root.find(self.__xmlns%'value')
        index = root.find(self.__xmlns%'index')
        getter = root.find('getter')
        setter = root.find('setter')
        iterator = root.find('iterator')
        
        property = InterfaceProperty(
            root.attrib['name'],
            interface,
            singular = root.attrib.get('singular'),
            type = value.attrib['type'],
            documentation = self.__parseDocumentation(root.find(self.__xmlns%'documentation'))
        )
        
        if index is not None:
            InterfacePropertyIndex(
                index.attrib['name'],
                property,
                type = index.attrib['type'],
                apiName = index.attrib.get('apiname'),
                documentation = self.__parseDocumentation(root.find(self.__xmlns%'documentation'))
            )
        ableChildren = 0
        
        if value.attrib.get('readable', "false").lower() in ("1", "true"):
            apiName = None
            
            if getter is not None:
                apiName = getter.attrib.get('apiname')
            
            InterfacePropertyGetter(
                property,
                apiName = apiName
            )
            
            ableChildren += 1
        
        if value.attrib.get('writable', "false").lower() in ("1", "true"):
            apiName = None
            transactional = True
            
            if setter is not None:
                apiName = setter.attrib.get('apiname')
                transactional = setter.attrib.get('transactional', "true").lower() in ("1", "true")
            
            InterfacePropertySetter(
                property,
                apiName = apiName,
                transactional = transactional
            )
            
            ableChildren += 1
        
        if value.attrib.get('iterable', "false").lower() in ("1", "true"):
            apiName = None
            
            if iterator is not None:
                apiName = iterator.attrib.get('apiname')
            
            InterfacePropertyIterator(
                property,
                apiName = apiName
            )
            
            ableChildren += 1
        
        if ableChildren == 0:
            raise Exception()
    
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
            namespace,
            documentation = self.__parseDocumentation(root.find(self.__xmlns%'documentation'))
        )
        
        for child in root:
            if child.tag == self.__xmlns%'property':
                value = child.find(self.__xmlns%'value')
                
                iterable = value.attrib.get('iterable', 'false').lower() in ('1', 'true')
                readable = value.attrib.get('readable', 'false').lower() in ('1', 'true')
                
                if not (iterable or readable) or (iterable and readable):
                    raise Exception()
                
                property = ExceptionProperty(
                    child.attrib['name'],
                    exception,
                    type = value.attrib['type'],
                    iterable = iterable,
                    documentation = self.__parseDocumentation(child.find(self.__xmlns%'documentation'))
                )
    
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
        
        delegate = Delegate(
            name,
            namespace,
            documentation = self.__parseDocumentation(root.find(self.__xmlns%'documentation'))
        )
        
        for child in root:
            if child.tag == self.__xmlns%'parameter':
                if child.attrib['type'] == 'namedparams':
                    raise Exception
                
                parameter = DelegateParameter(
                    child.attrib['name'],
                    delegate,
                    child.attrib['type'],
                    apiName = child.attrib.get('apiname'),
                    required = child.attrib.get('required', "true").lower() in ("1", "true"),
                    default = child.attrib.get('default'),
                    documentation = self.__parseDocumentation(child.find(self.__xmlns%'documentation')),
                )
            elif child.tag == self.__xmlns%'parameterDictionary':
                parameter = DelegateParameter(
                    child.attrib['name'],
                    delegate,
                    '*',
                    apiName = child.attrib.get('apiname'),
                    required = True,
                    documentation = self.__parseDocumentation(child.find(self.__xmlns%'documentation')),
                )
            elif child.tag == self.__xmlns%'return':
                returnType = DelegateReturn(
                    delegate,
                    child.attrib['type'],
                    iterable = child.attrib.get('iterable', "true").lower() in ("1", "true"),
                    documentation = self.__parseDocumentation(child.find(self.__xmlns%'documentation')),
                )
            elif child.tag == self.__xmlns%'throws':
                returnType = DelegateThrows(
                    delegate,
                    child.attrib['exception'],
                    documentation = self.__parseDocumentation(child.find(self.__xmlns%'documentation')),
                )
    
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
        print ('    ' * level) + repr(object), ('with api name ' + repr(object.apiName)) if hasattr(object, 'apiName') else ''
        
        if isinstance(object, BaseContainer):
            for child in object.children:
                self.__printStructureHelper(child, level + 1)
