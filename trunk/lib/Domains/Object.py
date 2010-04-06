from lib.Exceptions import DomainObjectError
import re
from lib.consts import DEFAULT_IDENTITY
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
        for id in self.type.IterAttributeIDs():
            self.values[id] = self.type.GetDefaultValue(id)
    
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
            self.values=domainobject.values
        else:
            raise DomainObjectError('Domain type mismatch.')
    
    def GetValue(self, id):
        '''
        @return: value of attribute
        @rtype: various
        
        @param id: path to the attribute
        @type id: str
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
    
    def AppendItem(self, id):
        '''
        Append next object to the attribute with type list
        
        @param id: path to the attribute
        @type id: str
        
        @param id: path to the attribute
        @type id: str
        '''
        self._TracePath(id, 'append')
    
    def RemoveItem(self, id):
        '''
        Remove object from attribute with type list
        
        @param id: path to the attribute
        @type id: str
        '''
        self._TracePath(id, 'remove')
    
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
                    self.values[path[0]] = str(value)
                else:
                    self.values[path[0]] = self.type.TransformValue(value, id = path[0])
                return
            elif action == 'getvalue':
                if path[0] in self.values:
                    return self.values[path[0]]
                else:
                    raise DomainObjectError('Invalid attribute %s in domain %s' % (path[0], self.type.GetName()))
            elif action == 'gettype':
                if path[0] == '':
                    return self.type
                else:
                    return self.type.GetFactory().GetDomain(self.type.GetAttribute(path[0])['type'])
            elif action == 'getdomainname':
                if path[0] == '':
                    return self.type.GetName()
                else:
                    return self.type.GetAttribute(path[0])['type']
            elif action == 'append':
                if self.type.GetAttribute(path[0])['type'] == 'list':
                    self.values[path[0]].append(self.type.GetDefaultValue(domain = self.type.GetAttribute(path[0])['list']['type']))
                else:
                    raise DomainObjectError('Attribute %s of domain %s is not of type "list"'%\
                    (path[0], self.type.GetName()))
            elif action == 'remove':
                raise DomainObjectError('RemoveItem is allowed on item of a list only')
            elif action == 'visual':
                return self.type.HasVisualAttribute(path[0])
        
        elif path[1] == '.': #nested call
            if self.type.IsAtomic(id = path[0]): #atomic element doesn't have items
                raise DomainObjectError('Attribute %s of domain %s is atomic'%\
                    (path[0], self.type.GetName()))
            return self.values[path[0]]._TracePath(path[2], action, value)
        
        elif path[1] == '[': #index of list
            
            if self.type.GetAttribute(path[0])['type'] <> 'list':
                raise CDomainObjectError('Attribute %s of domain %s cannot be indexed'%\
                    (path[0], self.type.GetName()))
            
            idx, rest = path[2].split(']', 1)
            idx = int(idx)
            if self.type.IsAtomic(domain = self.type.GetAttribute(path[0])['list']['type']) or rest == '':
                if rest:
                    raise DomainObjectError('Nothing was expected after "]"')
                
                if action == 'setvalue':
                    self.values[path[0]][idx] = self.type.TransformValue(value, domain = self.type.GetAttribute(path[0])['list']['type'])
                    return
                elif action == 'getvalue':
                    return self.values[path[0]][idx]
                elif action == 'gettype':
                    return self.type.GetFactory().GetDomain(self.type.GetAttribute(path[0])['list']['type'])
                elif action == 'getdomainname':
                    return self.type.GetAttribute(path[0])['list']['type']
                elif action == 'append':
                    if self.type.GetAttribute(path[0])['list']['type'] == 'list':
                        self.values[path[0]][idx].append(self.type.GetDefaultValue(domain = self.type.GetAttribute(path[0])['list']['type']))
                    else:
                        raise DomainObjectError('Type of items in list %s of domain %s are not of type "list"'%\
                        (path[0], self.type.GetName()))
                elif action == 'remove':
                    self.values[path[0]].pop(idx)
                elif action == 'visual':
                    return self.type.HasVisualAttribute(path[0])
                
            if rest.startswith('.'):
                return self.values[path[0]][idx]._TracePath(rest[1:], action, value)
            
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
