import uuid
from Registrar import registrar
from lib.Exceptions.DevException import UIDException

class CBaseObject(object):
    __uid = None
    
    def GetUID(self):
        uid = self.__uid
        if uid is None:
            uid = self.__uid = str(uuid.uuid1())
            registrar._Register(uid, self)
        
        return self.__uid
    
    def SetUID(self, value):
        if self.__uid is not None:
            raise UIDException("cantSet")
        
        self.__uid = value
        registrar._Register(value, self)
