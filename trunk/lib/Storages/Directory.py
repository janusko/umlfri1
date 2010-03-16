import os.path
import os
import shutil

import StorageList

from AbstractStorage import CAbstractStorage

from lib.Base import CBaseObject

class CDirectory(CBaseObject):
    @staticmethod
    def create(path):
        if not os.path.isdir(path):
            return None
        return CDirectory(path)
    
    @staticmethod
    def duplicate(storage, path):
        root = path
        
        os.makedirs(root)
        
        for path, dirs, files in storage.walk():
            for dname in dirs:
                os.mkdir(os.path.join(root, path, dname))
            
            for fname in files:
                file(os.path.join(root, path, fname), 'wb').write(storage.read_file(os.path.join(path, fname)))
        
        return CDirectory(root)
    
    def __init__(self, path):
        self.path = path
    
    def listdir(self, path):
        return os.listdir(os.path.join(self.path, path))
    
    def file(self, path):
        return open(os.path.join(self.path, path), 'rb')
    
    def read_file(self, path):
        return self.file(path).read()
    
    def exists(self, path):
        return os.path.isfile(os.path.join(self.path, path))
    
    def subopen(self, path):
        return StorageList.open_storage(os.path.join(self.path, path))
    
    def destroy(self):
        shutil.rmtree(self.path)
    
    def walk(self):
        return os.walk(self.path)

StorageList.classes.append(CDirectory)
