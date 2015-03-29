import weakref
from lib.Exceptions import DomainObjectError
import re
from lib.consts import DEFAULT_IDENTITY, LENGTH_PROPERTY
from types import NoneType
from lib.Base import CBaseObject

class CDomainObject(CBaseObject):
    '''
    representation of logical element attribute - its value
    
    @ivar values: stores values of domain attributes
    @ivar type: reference to domain type
    '''
    
    def __init__(self, type):
        '''
        create new instance
        
        all the inner values are set to default values defined by type.
        Non-atomic inner values are set to another CDomainObject objects
        creating tree-like structure.
        
        @param type: domain type of current object - definition
        @type type: L{CDomainType<Type.CDomainType>}
        '''
        
        if isinstance(type, (str, unicode)):
            raise DomainObjectError('string cannot be used as domain reference')
        self.type = type
        self.values = {}
        self.parent = lambda: None

    def GetParent(self):
        """
        Return parent of this domain object.

        @return: Parent L{CDomainObject<lib.Domains.Object.CDomainObject>}
        @rtype : CDomainObject or None
        """
        return self.parent()

    def SetParent(self, parent):
        """
        Sets new parent of this domain object. Parent can only be an instance of
        L{CDomainObject<lib.Domains.Object.CDomainObject>}.

        @param parent: New parent domain object of this object.
        @type parent : L{CDomainObject<lib.Domains.Object.CDomainObject>}
        """
        self.parent = weakref.ref(parent)

    def SetType(self, type):
        """
        Changes domain type of this domain object.

        @param type: Domain type to set.
        @type type: L{CDomainType<lib.Domains.Type.CDomainType>}
        """
        self.type = type

    def GetType(self, id=''):
        '''
        @return: DomainType of attribute
        @rtype: L{CDomainType<lib.Domains.Type.CDomainType>}
        
        @param id: path to the attribute
        @type id: str
        '''
        return self._TracePath(id, 'gettype')
    
    def GetDomainName(self, id):
        '''
        @return: name of DomainType of attribute
        @rtype: str
        
        @param id: path to the attribute
        @type id: str
        '''
        return self._TracePath(id, 'getdomainname')
    
    def __CopyFromObjectToObject(self,old,copy):
        for id in old.GetType().IterAttributeIDs():
            if old.GetType().GetAttribute(id)['type']!='list':
                copy.SetValue(id,old.GetValue(id))
            else:
                ind=0
                for att in old.GetValue(id):
                    copy.AppendItem(id)
                    self.__CopyFromObjectToObject(att,copy.GetValue(id)[ind])
                    ind=ind+1
        return copy

    def CopyFrom(self, domainobject):
        self.__CopyFromObjectToObject(domainobject, self)

    def GetCopy(self):
        '''
        Copy of this domain object
        
        @return: copy of domain object
        @rtype: L{CDomainObject<lib.Domains.Object.CDomainObject>}
        '''
        return self.__CopyFromObjectToObject(self,CDomainObject(self.GetType()))
    
    def SetValues(self,domainobject):
        '''
        Set values from given domain object
        
        @param domainobject: domain object with values to be copied
        @type domainobject: L{CDomainObject<lib.Domains.Object.CDomainObject>}
        '''
        if self.GetType().GetName()==domainobject.GetType().GetName():
            for id in self.type.IterAttributeIDs():
                self.__SetAttributeValue(id, self.type.GetDefaultValue(id))
            for id in self.GetType().IterAttributeIDs():
                if self.GetType().GetAttribute(id)['type']!='list':
                    self.SetValue(id,domainobject.GetValue(id))
                else:
                    ind=0
                    for att in domainobject.GetValue(id):
                        self.AppendItem(id)
                        self.__CopyFromObjectToObject(att,self.GetValue(id)[ind])
                        ind=ind+1
        else:
            raise DomainObjectError('Domain type mismatch.')

    def GetValue(self, id):
        '''
        @return: value of attribute
        @rtype: various
        
        @param id: path to the attribute
        @type id: str
        
        @return: value with entered id
        @rtype: object
        '''
        return self._TracePath(id, 'getvalue')
    
    def SetValue(self, id, value):
        '''
        Set new value to the attribute
        
        @param id: path to the attribute
        @type id: str
        
        @param value: new value to be set
        @type value: various
        '''
        self._TracePath(id, 'setvalue', value)
    
    def AppendItem(self, id,item=None):
        '''
        Append next object to the attribute with type list
        
        @param id: path to the attribute
        @type id: str
        
        @param item: new item
        @type item: variously varies
        
        @return: appended value
        @rtype: object
        '''
        return self._TracePath(id, 'append',item)
    
    def RemoveItem(self, id):
        '''
        Remove object from attribute with type list
        
        @param id: path to the attribute
        @type id: str
        '''
        self._TracePath(id, 'remove')

    def SwapItems(self, id, indexes):
        '''
        Swap two values of attribute with type list

        @param id: path to the attribute
        @type id: str

        @param indexes: two indexes to be swaped
        @type indexes: tuple
        '''
        self._TracePath(id, 'swap', indexes)
    
    def HasVisualAttribute(self, id):
        '''
        @return: True if attribute is being displayed
        '''
        return self.GetDomainName(id) != 'text'
        #return self._TracePath(id, 'visual')
    
    def _TracePath(self, id, action, value = None):
        '''
        Find attribute defined by id and perform action
        
        @param id: path to the attribute
        '''
        
        path = re.split(r'(\[|\.)', id, 1)
        
        if len(path) == 1: #work with current attribute
            if action == 'setvalue':
                if path[0] == DEFAULT_IDENTITY:
                    self.__SetAttributeValue(path[0], str(value))
                else:
                    if not self.type.HasAttribute(path[0]):
                        raise DomainObjectError('Invalid attribute %s in domain %s' % (path[0], self.type.GetName()))
                    self.__SetAttributeValue(path[0], self.type.TransformValue(value, id = path[0]))
                return
            elif action == 'getvalue':
                if not self.type.HasAttribute(path[0]):
                    raise DomainObjectError('Invalid attribute %s in domain %s' % (path[0], self.type.GetName()))
                return self.__GetAttributeValue(path[0])
            elif action == 'gettype':
                if path[0] == '':
                    return self.type
                else:
                    if not self.type.HasAttribute(path[0]):
                        raise DomainObjectError('Invalid attribute %s in domain %s' % (path[0], self.type.GetName()))
                    return self.type.GetFactory().GetDomain(self.type.GetAttribute(path[0])['type'])
            elif action == 'getdomainname':
                if path[0] == '':
                    return self.type.GetName()
                else:
                    if not self.type.HasAttribute(path[0]):
                        raise DomainObjectError('Invalid attribute %s in domain %s' % (path[0], self.type.GetName()))
                    return self.type.GetAttribute(path[0])['type']
            elif action == 'append':
                if not self.type.HasAttribute(path[0]):
                    raise DomainObjectError('Invalid attribute %s in domain %s' % (path[0], self.type.GetName()))
                if self.type.GetAttribute(path[0])['type'] == 'list':
                    if value is None:
                        value = self.type.GetDefaultValue(domain = self.type.GetAttribute(path[0])['list']['type'])
                    self.__GetAttributeValue(path[0]).append(value)
                    return value
                else:
                    raise DomainObjectError('Attribute %s of domain %s is not of type "list"'%\
                    (path[0], self.type.GetName()))
            elif action == 'swap':
                if not self.type.HasAttribute(path[0]):
                    raise DomainObjectError('Invalid attribute %s in domain %s' % (path[0], self.type.GetName()))
                if self.type.GetAttribute(path[0])['type'] == 'list':
                    leftIndex = value[0]
                    rightIndex = value[1]

                    if (min(value) >= 0 and max(value)<len):
                        list = self.__GetAttributeValue(id)
                        left = list[leftIndex]
                        right = list[rightIndex]
                        self.__SetAttributeValue(id, right, leftIndex)
                        self.__SetAttributeValue(id, left, rightIndex)
                    else:
                        raise DomainObjectError('Trying to swap values out of index: %s' % value)
                else:
                    raise DomainObjectError('Attribute %s of domain %s is not of type "list"'%\
                    (path[0], self.type.GetName()))
            elif action == 'remove':
                raise DomainObjectError('RemoveItem is allowed on item of a list only')
            elif action == 'visual':
                return self.type.HasVisualAttribute(path[0])
        
        elif path[1] == '.': #nested call
            if action == 'getvalue':
                # special treatment for getting the @length property of the list
                if self.type.GetAttribute(path[0])['type'] == 'list' and path[2] == LENGTH_PROPERTY:
                    return len(self.__GetAttributeValue(path[0]))
            if self.type.IsAtomic(id = path[0]): #atomic element doesn't have items
                raise DomainObjectError('Attribute %s of domain %s is atomic'%\
                    (path[0], self.type.GetName()))
            return self.__GetAttributeValue(path[0])._TracePath(path[2], action, value)
        
        elif path[1] == '[': #index of list

            if not self.type.HasAttribute(path[0]):
                raise DomainObjectError('Invalid attribute %s in domain %s' % (path[0], self.type.GetName()))
            
            if self.type.GetAttribute(path[0])['type'] <> 'list':
                raise DomainObjectError('Attribute %s of domain %s cannot be indexed'%\
                    (path[0], self.type.GetName()))

            list = self.__GetAttributeValue(path[0])
            
            idx, rest = path[2].split(']', 1)
            idx = int(idx)
            if self.type.IsAtomic(domain = self.type.GetAttribute(path[0])['list']['type']) or rest == '':
                if rest:
                    raise DomainObjectError('Nothing was expected after "]"')

                if action == 'setvalue':
                    if idx < 0 or idx >= len(list):
                        raise DomainObjectError('Index out of bounds in attribute %s of domain %s'%\
                            (path[0], self.type.GetName()))
                    value = self.type.TransformValue(value, domain = self.type.GetAttribute(path[0])['list']['type'])
                    self.__SetAttributeValue(path[0], value, index=idx)
                    return
                elif action == 'getvalue':
                    if idx < 0 or idx >= len(list):
                        raise DomainObjectError('Index out of bounds in attribute %s of domain %s'%\
                            (path[0], self.type.GetName()))
                    return list[idx]
                elif action == 'gettype':
                    return self.type.GetFactory().GetDomain(self.type.GetAttribute(path[0])['list']['type'])
                elif action == 'getdomainname':
                    return self.type.GetAttribute(path[0])['list']['type']
                elif action == 'append':
                    if idx < 0 or idx > len(list):
                        raise DomainObjectError('Index out of bounds in attribute %s of domain %s'%\
                            (path[0], self.type.GetName()))
                    if value is None:
                        value = self.type.GetDefaultValue(domain = self.type.GetAttribute(path[0])['list']['type'])
                    list.insert(idx, value)
                    return value
                elif action == 'remove':
                    if idx < 0 or idx >= len(list):
                        raise DomainObjectError('Index out of bounds in attribute %s of domain %s'%\
                            (path[0], self.type.GetName()))
                    list.pop(idx)
                elif action == 'visual':
                    return self.type.HasVisualAttribute(path[0])
                
            if rest.startswith('.'):
                return list[idx]._TracePath(rest[1:], action, value)
            
    def GetSaveInfo(self):
        '''
        @return: structured dictionary containing all the necessary data for .frip file
        @rtype: dict
        '''
        return dict([(id, self.type.PackValue(id, value) if id != DEFAULT_IDENTITY else str(value))
            for id, value in self.values.iteritems()])
    
    def SetSaveInfo(self, data):
        '''
        Restore all the attribute values from dictionary loaded from .frip file
        
        @param data: structured dictionary as returned from 
        L{self.GetSaveInfo<self.GetSaveInfo>}
        @type data: dict
        '''
        for key, value in data.iteritems():
            if self.type.HasAttribute(key):
                if isinstance(value, dict):
                    self.GetValue(key).SetSaveInfo(value)
                elif isinstance(value, (list, str, unicode, NoneType)):
                    self.SetValue(key, value)
    
    def __iter__(self):
        for id in self.type.IterAttributeIDs():
            yield id, self.values[id]

    def __GetAttributeValue(self, id):
        return self.values.setdefault(id, self.type.GetDefaultValue(id))

    def __SetAttributeValue(self, id, value, index = None):
        if isinstance(value, CDomainObject):
            value.SetParent(self)

        if index is not None:
            self.__GetAttributeValue(id)[index] = value
        else:
            self.values[id] = value