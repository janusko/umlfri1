from .baseContainer import BaseContainer
from .delegate import Delegate
from .delegateParameter import DelegateParameter
from .delegateReturn import DelegateReturn
from .delegateThrows import DelegateThrows
from .documentation import Documentation
from .exception import Exception as ExceptionDefinition
from .exceptionProperty import ExceptionProperty
from .interface import Interface
from .interfaceMethod import InterfaceMethod
from .interfaceMethodParameter import InterfaceMethodParameter
from .interfaceMethodReturn import InterfaceMethodReturn
from .interfaceMethodThrows import InterfaceMethodThrows
from .interfaceProperty import InterfaceProperty
from .interfacePropertyGetter import InterfacePropertyGetter
from .interfacePropertyIndex import InterfacePropertyIndex
from .interfacePropertyIterator import InterfacePropertyIterator
from .interfacePropertySetter import InterfacePropertySetter
from .interfacePropertyThrows import InterfacePropertyThrows
from .namespace import Namespace

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
        self.__cache = {}
    
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
        self.__addAutoThrows()
        self.__addToCache(self.__rootNamespace)
    
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
    
    def getTypeByFQN(self, fqn):
        return self.__cache[fqn]
    
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
            apiName = root.attrib.get('apiName'),
            base = root.attrib.get('base'),
            abstract = root.attrib.get('abstract', "false").lower() in ("1", "true"),
            generate = root.attrib.get('generate', "true").lower() in ("1", "true"),
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
            async = root.attrib.get('async', "false").lower() in ("1", "true"),
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
                throws = InterfaceMethodThrows(
                    method,
                    child.attrib['exception'],
                    documentation = self.__parseDocumentation(child.find(self.__xmlns%'documentation')),
                )
    
    def __parseInterfaceProperty(self, root, interface):
        value = root.find(self.__xmlns%'value')
        index = root.find(self.__xmlns%'index')
        getter = root.find(self.__xmlns%'getter')
        setter = root.find(self.__xmlns%'setter')
        iterator = root.find(self.__xmlns%'iterator')
        
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
            
            method = InterfacePropertyGetter(
                property,
                apiName = apiName
            )
            
            if getter is not None:
                self.__parseInterfacePropertyThrows(method, getter)
            
            ableChildren += 1
        
        if value.attrib.get('writable', "false").lower() in ("1", "true"):
            apiName = None
            transactional = True
            
            if setter is not None:
                apiName = setter.attrib.get('apiname')
                transactional = setter.attrib.get('transactional', "true").lower() in ("1", "true")
            
            method = InterfacePropertySetter(
                property,
                apiName = apiName,
                transactional = transactional
            )
            
            if setter is not None:
                self.__parseInterfacePropertyThrows(method, setter)
            
            ableChildren += 1
        
        if value.attrib.get('iterable', "false").lower() in ("1", "true"):
            apiName = None
            
            if iterator is not None:
                apiName = iterator.attrib.get('apiname')
            
            method = InterfacePropertyIterator(
                property,
                apiName = apiName
            )
            
            if iterator is not None:
                self.__parseInterfacePropertyThrows(method, iterator)
            
            ableChildren += 1
        
        if ableChildren == 0:
            raise Exception()
    
    def __parseInterfacePropertyThrows(self, method, root):
        for child in root:
            if child.tag == self.__xmlns%'throws':
                throws = InterfacePropertyThrows(
                    method,
                    child.attrib['exception'],
                    documentation = self.__parseDocumentation(child.find(self.__xmlns%'documentation')),
                )
    
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
            number = int(root.attrib['number']),
            base = root.attrib.get('base'),
            throwsFrom = root.attrib.get('throwsFrom'),
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
                    index = int(child.attrib['index']),
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
        
        return Documentation('\n'.join(line.strip() for line in text.strip().split('\n')))
    
    def __printStructureHelper(self, object, level):
        print ('    ' * level) + repr(object), ('with api name ' + repr(object.apiName)) if hasattr(object, 'apiName') else ''
        
        if isinstance(object, BaseContainer):
            for child in object.children:
                self.__printStructureHelper(child, level + 1)
    
    def __addToCache(self, object):
        if object.fqn in self.__cache:
            raise Exception("%s is already in cache"%object.fqn)
        
        self.__cache[object.fqn] = object
        
        if isinstance(object, BaseContainer):
            for child in object.children:
                self.__addToCache(child)

    ########################
    # Auto throws processing
    
    def __addAutoThrows(self):
        exceptions = {'all': [], 'mutator': [], 'transactional': [], 'getter': [], 'setter': [], 'iterator': []}
        self.__findAutoThrows(self.__rootNamespace, exceptions)
        self.__setAutoThrows(self.__rootNamespace, exceptions)
    
    def __findAutoThrows(self, ns, exceptions):
        for child in ns.children:
            if isinstance(child, Namespace):
                self.__findAutoThrows(child, exceptions)
            elif isinstance(child, ExceptionDefinition):
                for type in child.throwsFrom:
                    exceptions[type].append(child)
    
    def __setAutoThrows(self, ns, exceptions):
        for child in ns.children:
            if isinstance(child, Namespace):
                self.__setAutoThrows(child, exceptions)
            elif isinstance(child, Interface):
                for member in child.children:
                    if isinstance(member, InterfaceMethod):
                        self.__setAutoThrowsToMethod(member, exceptions['all'])
                        if member.mutator:
                            self.__setAutoThrowsToMethod(member, exceptions['mutator'])
                        if member.transactional:
                            self.__setAutoThrowsToMethod(member, exceptions['transactional'])
                    elif isinstance(member, InterfaceProperty):
                        if member.getter is not None:
                            self.__setAutoThrowsToProperty(member.getter, exceptions['all'])
                            self.__setAutoThrowsToProperty(member.getter, exceptions['getter'])
                        if member.setter is not None:
                            self.__setAutoThrowsToProperty(member.setter, exceptions['all'])
                            self.__setAutoThrowsToProperty(member.setter, exceptions['setter'])
                            self.__setAutoThrowsToProperty(member.setter, exceptions['mutator'])
                            if member.setter.transactional:
                                self.__setAutoThrowsToProperty(member.setter, exceptions['transactional'])
                        if member.iterator is not None:
                            self.__setAutoThrowsToProperty(member.iterator, exceptions['all'])
                            self.__setAutoThrowsToProperty(member.iterator, exceptions['iterator'])
    
    def __setAutoThrowsToMethod(self, member, exceptions):
        for exc in exceptions:
            InterfaceMethodThrows(member, exc)
    
    def __setAutoThrowsToProperty(self, member, exceptions):
        for exc in exceptions:
            InterfacePropertyThrows(member, exc)
