from DomainObject import IDomainObject
from lib.Connections import CConnectionObject

class IConnectionObject(IDomainObject):
    __cls__ = CConnectionObject
    
