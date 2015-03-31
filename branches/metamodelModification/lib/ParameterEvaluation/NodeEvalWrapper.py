from lib.Domains import CDomainObject
from lib.Base import CBaseObject

class CNodeEvalWrapper(CBaseObject):

    def __init__(self, object, node):
        self._object = object
        self._node = node

    def _CreateNodeEvalWrapper(self, object, node):
        return CNodeEvalWrapper(object, node)
    
    def __convert(self, val):
        if isinstance(val, CDomainObject):
            return self._CreateNodeEvalWrapper(val, None)
        elif isinstance(val, list):
            return self._CreateNodeEvalWrapper(val, None)
        else:
            return val
    
    def __getattr__(self, name):
        return self.__convert(self._object.GetValue(name))
    
    def __getitem__(self, name):
        return self.__convert(self._object[name])
    
    def __iter__(self):
        if isinstance(self._object, CDomainObject):
            for name, val in self._object:
                yield name, self.__convert(val)   
            if self._node is not None:
                yield '_Children', self._Children

            customAttributes = self._CreateCustomAttributes()
            if customAttributes is not None:
                for attrib in customAttributes:
                    yield attrib
        else:
            for val in self._object:
                yield self.__convert(val)
    
    def __len__(self):
        return len(self._object)

    def _CreateCustomAttributes(self):
        return None
    
    @property
    def _Children(self):
        if self._node:
            for child in self._node.GetChilds():
                yield self._CreateNodeEvalWrapper(child.GetObject().GetDomainObject(), child)
