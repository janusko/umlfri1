import re
from Object import CDomainObject

class EDomainType(Exception):
    pass

class CDomainType(object):
    
    ATOMIC = 'int', 'float', 'str', 'bool', 'enum', 'list'
    
    def __init__(self, name, factory):
        '''
        @param name: Domain identifier
        @type name: str

        @param factory: domain factory that already loaded all the domains
        @type factory: L{CDomainFactory<Factory.CDomainFactory>}
        '''
        self.name = name
        self.imports = []
        self.attributes = {}
        self.factory = factory
        self.parsers = []
    
    def AppendAttribute(self, id, name, type):
        '''
        Add attribute the domain
        
        @param id: identifier of attribute.
        @type id: str
        
        @param name: Name of attribute. Displayed to user
        @type name: str
        
        @param type: id of domain. Must be atomic domain or one of imported
        @type type: str
        
        @raise EDomainType: if type is not atomic or one of imported domains
        '''
        
        if not type in self.ATOMIC and not type in self.imports:
            raise EDomainType('Used type %s is not imported'%(type, ))
        
        self.attributes[id] = {'name': name, 'type':type}

    def AppendImport(self, id):
        '''
        Add name of domain that current uses
        
        Only imported domains are allowed to be used
        
        @param id: identifier of imported domain
        @type id: str
        '''
        assert isinstance(id, (str, unicode))
        self.imports.append(id)
    
    def AppendEnumValue(self, id, value):
        '''
        Add next valid value for enum type.
        
        @param id: identifier of attribute
        @type id: str
        
        @param value: enum value
        @type value: str
        '''
        
        assert isinstance(value, (str, unicode))
        if not id in self.attributes:
            raise EDomainType('Unknown identifier %s'%(id, ))
            
        if value in self.attributes.get('enum',[]):
            raise EDomainType('the same enum value already defined')
        
        self.attributes[id].setdefault('enum',[]).append(value)
    
    def SetList(self, id, type, separator):
        '''
        Set information about items in list
        
        @param id: attribute identifier
        @type id: str
        
        @param type: domain of item in list, must be either atomic or imported
        @type type: str
        
        @param separator: character (substring) by which are items of list
        separated from each other when in list in string representation
        @type separator: str
        '''
        if not id in self.attributes:
            raise EDomainType('Unknown identifier %s'%(id, ))
        
        self.attributes[id]['list'] = {'type':type, 'separator':separator}
    
    def AppendParser(self, regexp=None):
        '''
        Add parameters for new parser.
        
        @param regexp: Regular expression, compiled in verbose mode
        @type regexp: str
        '''
        parser = {}
        if regexp is not None:
            parser['regexp'] = re.compile(regexp, re.X)
        self.parsers.append(parser)


    def __InnerImportLoop(self, name):
        '''
        Inner recursive loop of self.HasImportLoop
        
        @param name: id of domain that is searched in import tree
        @type name: str
        
        @return: string representing part of the loop or False
        @rtype: bool / str
        '''
        for imported in self.imports:
            if name == imported: 
                return self.name + ' - ' + name
            else:
                result = self.factory.GetDomain(imported).__InnerImportLoop(name)
                if result:
                    return self.name + ' - ' + result
        return False

    def HasImportLoop(self):
        '''
        @return: False if no loop detected, string with loop description otherwise
        @rtype: bool / str
        '''
        return self.__InnerImportLoop(self.name)
    
    def UndefinedImports(self):
        '''
        @return: list of the domain names that are imported but not recognized
        @rtype: list
        '''
        return ([name for name in self.imports if not self.factory.RecognizedDomain(name)])
    
    def CheckMissingInfo(self):
        '''
        Search trough self.attributes for missing information such as:
            - enum part of attributes with "enum" domain
            - list part of attributes with "list" domain and all its 
        '''
        for id, info in self.attributes.iteritems():
            if info['type'] == 'enum' and len(info.get('enum',[])) == 0:
                raise EDomainType('In domain "&s" is attribute "&s" of enum '
                    'domain, but has no "enum" values defined'&(self.name, id))
            elif info['type'] == 'list' and 'list' not in info:
                raise EDomainType('In domain "&s" is attribute "&s" of list '
                    'domain, but has no "list" definition'&(self.name, id))
    
    def GetAttribute(self, id):
        '''
        get item information as an dictionary
        
        keys of the dictionary: 'name', 'type', 'options', 'itemtype'
        
        @param id: identifier of item
        @type id: str
        
        @return: information about item
        @rtype dict
        '''
        
        return self.attributes[id]
    
    def IterAttributesID(self):
        '''
        Iterator over ID of items
        
        @rtype: str
        '''
        for id in self.attributes.iterkeys():
            yield id
    
    def IterParsers(self):
        '''
        Iterator over parsers
        
        @rtype: re._pattern_type
        '''
        for parser in self.parsers:
            yield parser
    
    def GetName(self):
        '''
        @return name of current domain
        @rtype: str
        '''
        return self.name
    
    def GetImports(self):
        '''
        @return: list of imported domains
        @rtype: list
        '''
        return self.imports
    
    def GetDefaultValue(self, id):
        '''
        @return: default value of item defined by id
        @rtype: various
        
        @raise EDomainType: when id is not valid item identifier
        
        @param id: item identifier
        @type id: str
        '''
        if not id in self.attributes:
            raise EDomainType('Unknown identifier %s'%(id, ))
        
        type = self.attributes[id]['type']

        if self.IsAtomic(id):
            if type == 'int': 
                return 0
            elif type == 'float':
                return 0.0
            elif type == 'bool':
                return False
            elif type == 'str':
                return ''
            elif type == 'list':
                return []
            elif type == 'enum':
                return self.attributes[id]['enum'][0]
        else:
            return CDomainObject(self.factory.GetDomain(type))
    
    def IsAtomic(self, id):
        '''
        @return: True if item defined by id is of an atomic domain
        @rtype: bool
        
        @param id: identifier of item
        @type id: str
        
        @raise EDomainType: if id is not valid item identifier
        '''
        if not id in self.attributes:
            raise EDomainType('Unknown identifier %s'%(id, ))
        
        return self.attributes[id]['type'] in self.ATOMIC
    
    def TransformValue(self, id, value):
        '''
        @return: value transformed to domain that is defined for defined attribute
        
        @param id: identifier of the attribute
        @type id: str
        
        @param value: value to be transformed
        
        @raise EDomainType: 
            - if id is not recoginzed
            - if value is incopatible with attribute domain
        '''
        
        if not id in self.attributes:
            raise EDomainType('Unknown identifier %s'%(id, ))
        
        type = self.attributes[id]['type']
        
        if type in self.ATOMIC:
            if type == 'int':
                return self.__GetInt(value)
            elif type == 'float':
                return self.__GetFloat(value)
            elif type == 'str':
                return self.__GetStr(value)
            elif type == 'bool':
                return self.__GetBool(value)
            elif type == 'enum':
                try:
                    return self.__GetEnum(value, self.attributes[id]['enum'])
                except KeyError:
                    raise EDomainType(
                        'In domain "%s" is attribute "%s" of type "enum", '
                        'but has no defined values'%(self.name, id))
            elif type == 'list':
                try:
                    return self.__GetList(value, **self.attributes[id]['list'])
                except KeyError:
                    raise EDomainType(
                        'In domain "%s" is attribute "%s" of type "list", '
                        'but has no list definition'%(self.name, id))
        else:
            return self.__GetNonAtomic(value, type)
    
    def __GetInt(self, value):
        if isinstance(value, (int, long)):
            return value
        elif isinstance(value, (str, unicode)):
            try:
                return int(value)
            except:
                raise EDomainType('Cannot convert value to int')
        else:
            raise EDomainType('Invalid value type')
    
    def __GetFloat(self, value):
        if isinstance(value, (float, int, long, str, unicode)):
            try:
                return float(value)
            except:
                raise EDomainType('Cannot convert value to float')
        else:
            raise EDomainType('Invalid value type')
    
    def __GetStr(self, value):
        if isinstance(value, (str, unicode)):
            return value
        else:
            return str(value)
    
    def __GetBool(self, value):
        if isinstance(value, bool):
            return value
        elif isinstance(value, (int, float, long)):
            return bool(value)
        elif isinstance(value, (str, unicode)):
            if value.lower() in ('true', '1', 'yes'):
                return True
            elif value.lower() in ('false', '0', 'no'):
                return False
            else:
                raise EDomainType('Invalid string to be converted to bool')
        else:
            raise EDomainType('Invalid value type')
    
    def __GetEnum(self, value, enum):
        if isinstance(value, (str, unicode)):
            if enum.count(value) > 0:
                return value
            else:
                raise EDomainType('value is not member of enumeration')
        elif isinstance(value, (int, long)):
            if 0 <= value < len(enum):
                return enum[value]
            else:
                raise EDomainType('value points to the index out of range')
        else:
            raise EDomainType('value cannot be converted to enumeration item')
    
    def __GetList(self, value, separator, type):
        if isinstance(value, (str, unicode)):
            result = []
            domain = self.factory.GetDomain(type)
            atempt = [False]
            for parser in self.factory.GetDomain(type).IterParsers():
                if 'regexp' in parser:
                    attempt = [parser['regexp'].match(part) for part in value.split(separator)]
                if all(attempt):
                    break
            if not all(attempt):
                raise EDomainType('No parser can parse all the items in the list')
            for item in attempt:
                obj = CDomainObject(self.factory.GetDomain(type))
                for id, val in item.groupdict().iteritems():
                    if val is not None:
                        obj.SetValue(id, val)
                result.append(obj)
            return result
        elif isinstance(value, (list, tuple)):
            return [self.__GetNonAtomic(item, type) for item in value]
        else:
            raise EDomainType('value cannot be converted to list')

    
    def __GetNonAtomic(self, value, type):
        if isinstance(value, CDomainObject):
            if value.GetType().GetName() == type:
                return value
            else:
                raise EDomainType('Type mismatch')
        elif isinstance(value, (str, unicode)):
            attempt = None
            for parser in self.factory.GetDomain(type).IterParsers():
                attempt = parser.match(value)
                if attemtp:
                    break
            if not attempt:
                raise EDomainType('No parser can parse value')
            obj = CDomainObject(self.factory.GetDomain(type))
            for id, val in item.groupdict().iteritems():
                if val is not None:
                    obj.SetValue(id, val)
            return obj
        else:
            raise EDomainType('Invalid value type')
