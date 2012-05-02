from lib.Domains import CDomainObject
from lib.Base import CBaseObject

class CNodeEvalWrapper(CBaseObject):
    def __init__(self, object, node):
        self.__object = object
        self.__node = node
    
    def __convert(self, val):
        if isinstance(val, CDomainObject):
            return CNodeEvalWrapper(val, None)
        elif isinstance(val, list):
            return CNodeEvalWrapper(val, None)
        else:
            return val
    
    def __getattr__(self, name):
        return self.__convert(self.__object.GetValue(name))
    
    def __getitem__(self, name):
        return self.__convert(self.__object[name])
    
    def __iter__(self):
        if isinstance(self.__object, CDomainObject):
            for name, val in self.__object:
                yield name, self.__convert(val)   
            if self.__node is not None:
                yield '_Children', self._Children
                yield '_Icon', self._Icon
                yield '_Parent', self._Parent
        else:
            for val in self.__object:
                yield self.__convert(val)
    
    def __len__(self):
        return len(self.__object)
    
    @property
    def _Children(self):
        if self.__node:
            for child in self.__node.GetChilds():
                yield CNodeEvalWrapper(child.GetObject().GetDomainObject(), child)
    
    @property
    def _Icon(self):
        if not self.__node:
            return None
        return self.__node.GetObject().GetType().GetIcon()
    
    @property
    def _Parent(self):
        if not self.__node:
            return None
        parent = self.__node.GetParent()
        return CNodeEvalWrapper(parent.GetObject().GetDomainObject(), parent)
