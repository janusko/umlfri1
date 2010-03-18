from lib.Base import CBaseObject

class CAbstractStorage(CBaseObject):
    @staticmethod
    def create(path):
        return None
    
    @staticmethod
    def duplicate(storage, path):
        return None
    
    def __init__(self):
        pass
    
    def listdir(self, path):
        return []
    
    def file(self, path):
        return None
    
    def read_file(self, path):
        return ''
    
    def exists(self, path):
        return False
    
    def subopen(self, path):
        return None
    
    def destroy(self):
        pass
    
    def walk(self):
        pass
    
    def get_path(self):
        return ''
