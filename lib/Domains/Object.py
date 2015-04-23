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
        self.SetType(type)
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
        from lib.Domains.RuntimeType import CRuntimeDomainType
        if isinstance(type, CRuntimeDomainType):
            self.rawType = type.GetParentType()
            self.type = CRuntimeDomainType(self.rawType, self)
        else:
            self.rawType = type
            self.type = CRuntimeDomainType(type, self)

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
        for id in old.rawType.IterAttributeIDs():
            attribute = old.rawType.GetAttribute(id)
            attributeType = attribute['type']
            oldValue = old.__GetValueInternal(id, useRuntimeType=False)
            if not old.rawType.IsDomainAtomic(attributeType):
                newObject = CDomainObject(oldValue.GetType())
                self.__CopyFromObjectToObject(oldValue, newObject)
                copy.__SetValueInternal(id, newObject, useRuntimeType=False)
            elif attributeType != 'list':
                copy.__SetValueInternal(id, oldValue, useRuntimeType=False)
            else:
                itemType = attribute['list']['type']
                for att in oldValue:
                    if old.rawType.IsDomainAtomic(itemType):
                        copy.AppendItem(id, att)
                    else:
                        item = copy.AppendItem(id)
                        self.__CopyFromObjectToObject(att, item)
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
        if self.GetType().GetName() != domainobject.GetType().GetName():
            raise DomainObjectError('Domain type mismatch.')

        for id in self.rawType.IterAttributeIDs():
            attribute = self.rawType.GetAttribute(id)
            attributeType = attribute['type']
            value = domainobject.__GetValueInternal(id, useRuntimeType=False)
            if not self.rawType.IsDomainAtomic(attributeType):
                newObject = CDomainObject(value.GetType())
                self.__CopyFromObjectToObject(value, newObject)
                self.__SetValueInternal(id, newObject, useRuntimeType=False)
            if attributeType != 'list':
                self.__SetValueInternal(id, value, useRuntimeType=False)
            else:
                itemType = attribute['list']['type']
                for att in domainobject.GetValue(id):
                    if self.rawType.IsDomainAtomic(itemType):
                        self.AppendItem(id, att)
                    else:
                        item = self.AppendItem(id)
                        self.__CopyFromObjectToObject(att, item)

    def GetValue(self, id, useRuntimeType=True):
        '''
        @return: value of attribute
        @rtype: various
        
        @param id: path to the attribute
        @type id: str
        
        @return: value with entered id
        @rtype: object
        '''
        return self._TracePath(id, 'getvalue')
    
    def SetValue(self, id, value, useRuntimeType=True):
        '''
        Set new value to the attribute
        
        @param id: path to the attribute
        @type id: str
        
        @param value: new value to be set
        @type value: various
        '''
        self._TracePath(id, 'setvalue', value)
    
    def AppendItem(self, id, item=None, useRuntimeType=True):
        '''
        Append next object to the attribute with type list
        
        @param id: path to the attribute
        @type id: str
        
        @param item: new item
        @type item: variously varies
        
        @return: appended value
        @rtype: object
        '''
        return self._TracePath(id, 'append', item, useRuntimeType)
    
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
    
    def _TracePath(self, id, action, value = None, useRuntimeType=True):
        '''
        Find attribute defined by id and perform action
        
        @param id: path to the attribute
        '''
        
        path = re.split(r'(\[|\.)', id, 1)
        
        if len(path) == 1: #work with current attribute
            attributeID = path[0]
            if action == 'setvalue':
                self.__SetValueInternal(attributeID, value, useRuntimeType)
                return
            elif action == 'getvalue':
                return self.__GetValueInternal(attributeID, useRuntimeType)
            elif action == 'gettype':
                if attributeID == '':
                    return self.type
                else:
                    if not self.type.HasAttribute(attributeID):
                        raise DomainObjectError('Invalid attribute %s in domain %s' % (attributeID, self.type.GetName()))
                    attribute = self.type.GetAttribute(attributeID)
                    type = attribute['type']
                    if not self.type.IsDomainAtomic(type):
                        value = self.__GetAttributeValue(attributeID)
                        return value.GetType()
                    elif type == 'list':
                        type = attribute['list']['type']
                        return self.type.GetFactory().GetDomain(type)
                    else:
                        return type
            elif action == 'getdomainname':
                if attributeID == '':
                    return self.type.GetName()
                else:
                    if not self.type.HasAttribute(attributeID):
                        raise DomainObjectError('Invalid attribute %s in domain %s' % (attributeID, self.type.GetName()))
                    return self.type.GetAttribute(attributeID)['type']
            elif action == 'append':
                items = self.__GetValueInternal(attributeID)
                attribute = self.__GetAttribute(attributeID, useRuntimeType)
                if attribute['type'] != 'list':
                    raise DomainObjectError('Attribute %s of domain %s is not of type "list"'%\
                    (attributeID, self.type.GetName()))

                if value is None:
                    value = self.__GetDefaultValue(attribute['list']['type'], useRuntimeType)
                self.__SetParentForValue(value)
                items.append(value)
                return value
            elif action == 'swap':
                if not self.type.HasAttribute(attributeID):
                    raise DomainObjectError('Invalid attribute %s in domain %s' % (attributeID, self.type.GetName()))
                if self.type.GetAttribute(attributeID)['type'] == 'list':
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
                    (attributeID, self.type.GetName()))
            elif action == 'remove':
                raise DomainObjectError('RemoveItem is allowed on item of a list only')
            elif action == 'visual':
                return self.type.HasVisualAttribute(attributeID)
        
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
                    self.__SetParentForValue(value)
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
        saveinfo = {}
        for id in self.type.IterAttributeIDs():
            if id not in self.values:
                continue
            value = self.values[id]
            saveinfo[id] = self.type.PackValue(id, value) if id != DEFAULT_IDENTITY else str(value)

        return saveinfo

    def SetSaveInfo(self, data):
        '''
        Restore all the attribute values from dictionary loaded from .frip file
        
        @param data: structured dictionary as returned from 
        L{self.GetSaveInfo<self.GetSaveInfo>}
        @type data: dict
        '''
        for key, value in data.iteritems():
            if self.rawType.HasAttribute(key):
                if isinstance(value, dict):
                    self.GetValue(key).SetSaveInfo(value)
                elif isinstance(value, (list, str, unicode, NoneType)):
                    self.__SetValueInternal(key, value, False)
    
    def __iter__(self):
        for id in self.type.IterAttributeIDs():
            yield id, self.__GetAttributeValue(id)

    def __ChooseType(self, useRuntimeType):
        if useRuntimeType:
            return self.type
        else:
            return self.rawType

    def __GetAttribute(self, id, useRuntimeType=True):
        return self.__ChooseType(useRuntimeType).GetAttribute(id)

    def __GetDefaultValue(self, domain, useRuntimeType=True):
        return self.__ChooseType(useRuntimeType).GetDefaultValue(domain=domain)

    def __SetValueInternal(self, key, value, useRuntimeType=True):
        type = self.__ChooseType(useRuntimeType)

        if key == DEFAULT_IDENTITY:
            self.__SetAttributeValue(key, str(value), type=type)
        else:
            if not type.HasAttribute(key):
                raise DomainObjectError('Invalid attribute %s in domain %s' % (key, type.GetName()))
            self.__SetAttributeValue(key, type.TransformValue(value, id=key), type=type)

    def __GetValueInternal(self, attributeID, useRuntimeType=True):
        type = self.__ChooseType(useRuntimeType)

        if not type.HasAttribute(attributeID):
            raise DomainObjectError('Invalid attribute %s in domain %s' % (attributeID, type.GetName()))
        return self.__GetAttributeValue(attributeID, type)

    def __GetAttributeValue(self, id, type=None):
        if type is None:
            type = self.type
        if id in self.values:
            return self.values[id]
        else:
            value = type.GetDefaultValue(id)
            self.values[id] = value
            self.__SetParentForValue(value)
            return value

    def __SetAttributeValue(self, id, value, index=None, type=None):
        self.__SetParentForValue(value)

        if index is not None:
            self.__GetAttributeValue(id, type)[index] = value
        else:
            self.values[id] = value

    def __SetParentForValue(self, value):
        if isinstance(value, CDomainObject):
            value.SetParent(self)