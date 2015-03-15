import re
from Object import CDomainObject
from lib.Exceptions import DomainTypeError
import weakref
from lib.Base import CBaseObject
from lib.datatypes import CColor, CFont

class CDomainType(CBaseObject):
    '''
    @cvar ATOMIC: list of names of atomic attribute types
    @ivar name: name/id of domain
    @ivar imports: list of names of domains imported by this one
    @ivar attributes: description of attributes
    @ivar factory: reference to factory that created current instance
    @ivar parsers: list of parsers of this domain
    @ivar attributeorder: order of attributes defined by metamodel
    '''
    
    ATOMIC = 'int', 'float', 'str', 'text', 'bool', 'enum', 'list', 'color', 'font'
    
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
        if factory is None:
            self.factory = lambda:None
        else:
            self.factory = weakref.ref(factory)
        self.parsers = []
        self.joiners = []
        self.attributeorder = []
    
    def GetFactory(self):
        '''
        @retrun: Current domain factory
        @rtype: L{CDomainFactory<Factory.CDomainFactory>}
        '''
        return self.factory()
    
    def AppendAttribute(self, id, name, type = None, default = None, hidden=False):
        '''
        Add attribute the domain
        
        @param id: identifier of attribute.
        @type id: str
        
        @param name: Name of attribute. Displayed to user
        @type name: str
        
        @param type: id of domain. Must be atomic domain or one of imported
        @type type: str
        
        @param type: default value for attribute
        @type type: str
        
        @param hidden: wheter attribute should not be shown in GUI
        @type hidden: bool
        
        @raise DomainTypeError: if type is not atomic or one of imported domains
        '''
        
        if type is not None and type not in self.ATOMIC and type not in self.imports:
            raise DomainTypeError('Used type "%s" is not imported '
                'in definition of "%s.%s"'%(type, self.name, id))
        
        self.attributes[id] = {'name': name, 'type':type, 'default': default,'hidden': (hidden in ('true', '1'))}
        self.attributeorder.append(id)
    
    def HasAttribute(self, id):
        '''
        @return: True if id is defined attribute
        @rtype: bool
        '''
        return id in self.attributes

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
        
        if not id in self.attributes:
            raise DomainTypeError('Unknown identifier %s'%(id, ))
            
        if value in self.attributes.get('enum',[]):
            raise DomainTypeError('the same enum value already defined')
        
        self.attributes[id].setdefault('enum',[]).append(value)
    
    def AppendRestriction(self,id,res,value):
        '''
        Add restriction to type.
        
        @param id: identifier of attribute
        @type id: str
        
        @param res: restriction identifiier
        @type value: str
        
        @param value: restriction value
        @type value: str
        '''
        
        if not id in self.attributes:
            raise DomainTypeError('Unknown identifier %s'%(id, ))
        self.attributes[id].setdefault(res,value)
    
    def SetList(self, id, type=None, parser=None):
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
            raise DomainTypeError('Unknown identifier %s'%(id, ))
        list = self.attributes[id].setdefault('list',{'type':None})
        if type is not None:
            if type not in self.ATOMIC and type not in self.imports:
                raise DomainTypeError('Used type "%s" is not imported '
                    'in list definition of "%s.%s"'%(type, self.name, id))
            list['type'] = type
        if parser is not None:
            list['parser'] = parser
        
    
    def AppendParser(self, parser):
        '''
        Add parameters for new parser.
        
        @param regexp: Regular expression, compiled in verbose mode
        @type regexp: str
        '''
        self.parsers.append(parser)


    def AppendJoiner(self, joiner):
        self.joiners.append(joiner)
        
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
                result = self.GetFactory().GetDomain(imported).__InnerImportLoop(name)
                if result:
                    return self.name + ' - ' + result
        return False

    def HasImportLoop(self):
        '''
        @return: False if no loop detected, string with loop description otherwise
        @rtype: bool / str
        '''
        return self.__InnerImportLoop(self.name)
    
    def EmptyTypes(self):
        '''
        @return: list of attributes with type set to None
        @rtype: list
        '''
        return [name for name in self.attributes.iterkeys() 
                if self.attributes[name]['type'] is None
                    or (self.attributes[name]['type'] == 'list' 
                        and ('list' not in self.attributes[name]
                            or self.attributes[name]['list']['type'] is None))]
    
    def UndefinedImports(self):
        '''
        @return: list of the domain names that are imported but not recognized
        @rtype: list
        '''
        return ([name for name in self.imports if not self.GetFactory().HasDomain(name)])
    
    def CheckMissingInfo(self):
        '''
        Search trough self.attributes for missing information such as:
            - enum part of attributes with "enum" domain
            - list part of attributes with "list" domain and all its 
        '''
        for id, info in self.attributes.iteritems():
            if info['type'] == 'enum' and len(info.get('enum',[])) == 0:
                raise DomainTypeError('In domain "&s" is attribute "&s" of enum '
                    'domain, but has no "enum" values defined'&(self.name, id))
            elif info['type'] == 'list':
                if 'list' not in info:
                    raise DomainTypeError('In domain "&s" is attribute "&s" of list '
                        'domain, but has no "list" definition'&(self.name, id))
                elif ('parser' in info['list'] and 
                    not self.IsAtomic(domain = info['list']['type']) and 
                    len(list(self.GetFactory().GetDomain(info['list']['type']).IterParsers())) == 0):
                    raise DomainTypeError('"%s.%s" is list with parser, but used domain "%s" '
                        'has no parser.' % (self.name, id, info['list']['type']))
    
    def CheckDefault(self):
        '''
        Search through self.attributes for validity of default values
        ''' 
        for name in self.attributes.iterkeys():
            if self.attributes[name]['default'] is not None:
                self.TransformValue(self.attributes[name]['default'], name)
        
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
    
    def IterAttributeIDs(self):
        '''
        Iterator over ID of items
        It will skip hidden attributes

        @rtype: str
        '''
        for id in self.attributeorder:
            yield id
    
    def IterParsers(self):
        '''
        Iterator over parsers
        
        @rtype: re._pattern_type
        '''
        for parser in self.parsers:
            yield parser
    
    def IterJoiners(self):
        for joiner in self.joiners:
            yield joiner
            
    def GetName(self):
        '''
        @return: name of current domain
        @rtype: str
        '''
        return self.name
    
    def GetImports(self):
        '''
        @return: list of imported domains
        @rtype: list
        '''
        return self.imports
    
    def GetDefaultValue(self, id=None, domain=None):
        '''
        @return: default value of item defined by id
        @rtype: various
        
        @raise DomainTypeError: when id is not valid item or domain is unknown
        or none of parameters are set
        
        @param id: item identifier
        @type id: str
        '''
        
        if id is not None:
            if self.HasAttribute(id):
                raise DomainTypeError('Unknown identifier %s'%(id, ))
            attribute = self.GetAttribute(id)
            type = attribute['type']
        
        elif domain is not None and (self.IsAtomic(domain=domain) or self.GetFactory().HasDomain(domain)):
            type = domain
        
        else:
            raise DomainTypeError('None of the parameters are valid\n'
                'id = "%s" domain = "%s"'%(id, domain))
        
        if self.IsAtomic(domain=type):
            if id is None:
                raise DomainTypeError('Domain is atomic, but identifier of attribute was not provided\n'
                    'domain = "%s"'%(domain))

            if type == 'int': 
                return attribute['default'] or 0
            elif type == 'float':
                return attribute['default'] or 0.0
            elif type == 'bool':
                return attribute['default'] or False
            elif type in ('str', 'text'):
                return attribute['default'] or ''
            elif type == 'list':
                return []
            elif type == 'color':
                return attribute['default'] or CColor("#000000")
            elif type == 'font':
                return attribute['default'] or CFont("Arial 10")
            elif type == 'enum':
                return attribute['default'] or attribute['enum'][0]
        else:
            return CDomainObject(self.GetFactory().GetDomain(type))
    
    def IsAtomic(self, id=None, domain=None):
        '''
        Test on atomicity of domain
        
        Domain can be specified by parameter domain or by attribute of current
        domain, then its domain is tested.
        
        @return: True if domain is atomic
        @rtype: bool
        
        @param id: identifier of attribute which domain is asked
        @type id: str
        
        @param domain: name of domain
        @type domain: str
        
        @raise DomainTypeError: if id is not valid item identifier
        '''
        if id is not None:
            if not id in self.attributes:
                raise DomainTypeError('Unknown identifier "%s"'%(id, ))
            return self.IsAtomic(domain = self.attributes[id]['type'])
        elif domain is not None:
            return domain in self.ATOMIC
        else:
            raise DomainTypeError("Invalid input parameters")
    
    def IsHidden(self, id):
        '''
        Test on hidden attribute of domain
        
        Hidden attributes are not shown in GUI, thus not editable by user
        
        @return: True if attribute is hidden
        @rtype: bool
        
        @param id: name of attribute
        @type id: str
        '''
        
        if id not in self.attributes:
            raise DomainTypeError('Unknown identifier "%s"'%(id, ))
        return self.attributes[id]['hidden']
    
    def CheckValue(self, value, id = None, domain = None):
        '''
        @return: checked value
        
        @param id: identifier of the attribute
        @type id: str
        
        @param value: value to be checked
        
        @raise DomainTypeError: 
            - if id is not recoginzed
            - if value is incopatible with attribute domain
            - if value is incopatible with attribute constraint
        '''
        
        if domain is None:
            if not id in self.attributes:
                raise DomainTypeError('Unknown identifier %s'%(id, ))
            type = self.attributes[id]['type']
        else:
            type = domain
        
        if type in self.ATOMIC:
            if type == 'int':
                min = self.attributes[id]['min'] if self.attributes[id].has_key('min') else None
                max = self.attributes[id]['max'] if self.attributes[id].has_key('max') else None
                val = self.__GetInt(value)
                if (min!=None and min>val) or (max!=None and max<val):
                    raise DomainTypeError('Value of attribute %s is out of bounds.'%(id))
                else:
                    return val
            elif type == 'float':
                min = self.attributes[id]['min'] if self.attributes[id].has_key('min') else None
                max = self.attributes[id]['max'] if self.attributes[id].has_key('max') else None
                val = self.__GetFloat(value)
                if (min!=None and min>val) or (max!=None and max<val):
                    raise DomainTypeError('Value of attribute %s is out of bounds.'%(id))
                else:
                    return val
            elif type in ('str', 'text'):
                restriction=self.attributes[id]['restricted'] if self.attributes[id].has_key('restricted') else None
                val = self.__GetStr(value)
                if restriction!=None:
                    strings=restriction.split('|')
                    for string in strings:
                        if val.find(string)!=-1:
                            raise DomainTypeError('Value of attribute %s is out of bounds.'%(id))
                return val
            elif type in ('color', 'font'):
                return self.__GetStr(value)
            else:
                return value
        else:
            return self.__GetNonAtomic(value, type)
    
    def TransformValue(self, value, id = None, domain = None):
        '''
        @return: value transformed to domain that is defined for defined attribute
        
        @param id: identifier of the attribute
        @type id: str
        
        @param value: value to be transformed
        
        @raise DomainTypeError: 
            - if id is not recoginzed
            - if value is incopatible with attribute domain
        '''
        
        if domain is None:
            if not id in self.attributes:
                raise DomainTypeError('Unknown identifier %s'%(id, ))
            type = self.attributes[id]['type']
        else:
            type = domain
        
        if type in self.ATOMIC:
            if type == 'int':
                return self.__GetInt(value)
            elif type == 'float':
                return self.__GetFloat(value)
            elif type in ('str', 'text', 'color', 'font'):
                return self.__GetStr(value)
            elif type == 'bool':
                return self.__GetBool(value)
            elif type == 'enum':
                try:
                    return self.__GetEnum(value, self.attributes[id]['enum'])
                except KeyError:
                    raise DomainTypeError(
                        'In domain "%s" is attribute "%s" of type "enum", '
                        'but has no defined values'%(self.name, id))
            elif type == 'list':
                try:
                    return self.__GetList(value, **self.attributes[id]['list'])
                except KeyError:
                    raise DomainTypeError(
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
                raise DomainTypeError('Cannot convert value to int')
        else:
            raise DomainTypeError('Invalid value type')
    
    def __GetFloat(self, value):
        if isinstance(value, (float, int, long, str, unicode)):
            try:
                return float(value)
            except:
                raise DomainTypeError('Cannot convert value to float')
        else:
            raise DomainTypeError('Invalid value type')
    
    def __GetStr(self, value):
        if isinstance(value, (str, unicode)):
            return value
        elif value is None:
            return ''
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
                raise DomainTypeError('Invalid string to be converted to bool')
        else:
            raise DomainTypeError('Invalid value type')
    
    def __GetEnum(self, value, enum):
        if isinstance(value, (str, unicode)):
            if enum.count(value) > 0:
                return value
            else:
                raise DomainTypeError('value is not member of enumeration')
        elif isinstance(value, (int, long)):
            if 0 <= value < len(enum):
                return enum[value]
            else:
                raise DomainTypeError('value points to the index out of range')
        else:
            raise DomainTypeError('value cannot be converted to enumeration item')
    
    def __GetList(self, value, type, parser=None):
        if isinstance(value, (str, unicode)) and parser is not None : 
            domain = self.GetFactory().GetDomain(type)
            atempt = [False]
            
            for itemparser in domain.IterParsers():
                attempt = [itemparser.CreateObject(part, domain) for part in parser.Split(value)]
                if all(attempt):
                    break
            
            if not all(attempt):
                raise DomainTypeError('No parser can parse all the items in the list')
            return attempt
            
        elif isinstance(value, (list, tuple)):
            return [self.__GetNonAtomic(item, type) for item in value]
            
        else:
            raise DomainTypeError('value cannot be converted to list')

    
    def __GetNonAtomic(self, value, type):
        domain = self.GetFactory().GetDomain(type)
        if isinstance(value, CDomainObject):
            if value.GetType().GetName() == type:
                return value
            else:
                raise DomainTypeError('Type mismatch')
        elif isinstance(value, (str, unicode)):
            attempt = None
            for parser in domain.IterParsers():
                attempt = parser.CreateObject(value, domain)
                if attempt:
                    break
            if not attempt:
                raise DomainTypeError('No parser can parse value')
            return attempt
        elif isinstance(value, dict):
            result = CDomainObject(domain)
            result.SetSaveInfo(value)
            return result
        else:
            raise DomainTypeError('Invalid value type')
    
    def PackValue(self, id, value):
        '''
        '''
        
        if not id in self.attributes:
            raise DomainTypeError('Unknown identifier %s'%(id, ))
        
        if self.IsAtomic(id = id):
            if self.attributes[id]['type'] == 'list':
                return [(unicode(item)
                    if self.IsAtomic(domain = self.attributes[id]['list']['type'])
                    else item.GetSaveInfo()) for item in value]
            else:
                return unicode(value)
        else:
            return value.GetSaveInfo()
    
    def GetAttributesCount(self):
        return len(self.attributeorder)

    def _GetAttributes(self):
        return self.attributes