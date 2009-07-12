import os.path
import os

from AbstractStorage import CAbstractStorage

class CDirectory(CAbstractStorage):
    @staticmethod
    def create(path):
        if not os.path.isdir(path):
            return None
        return CDirectory(path)
    
    def __init__(self, path):
        self.path = path
    
    def listdir(self, path):
        return os.listdir(os.path.join(self.path, path))
    
    def file(self, path):
        return open(os.path.join(self.path, path), 'rb')
    
    def read_file(self, path):
        return self.file(path).read()
    
    def exists(self, path):
        return os.path.is_file(path)
