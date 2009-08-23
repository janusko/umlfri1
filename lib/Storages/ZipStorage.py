import os.path
import os
import zipfile
import cStringIO
import re

import StorageList

from AbstractStorage import CAbstractStorage

reMulSep = re.compile('/{2,}')

class CZipStorage(CAbstractStorage):
    @staticmethod
    def create(path):
        if os.path.isdir(path):
            return None
        
        file = path.replace('\\', '/').split('/')
        path = []
        while True:
            if not file:
                return
            f = os.path.join(*file)
            if not file[0]:
                f = os.path.sep + f
            if zipfile.is_zipfile(f):
                break
            path.insert(0, file.pop(-1))
        
        f = os.path.join(*file)
        if not file[0]:
            f = os.path.sep + f
        return CZipStorage(f, '/'.join(path))
    
    def __init__(self, file, path):
        if isinstance(file, zipfile.ZipFile):
            self.zip = file
        else:
            self.zip = zipfile.ZipFile(file, 'r')
        self.path = path
    
    def __convertPath(path):
        return reMulSep.sub('/', '/'.join((self.path, path)).rstrip('/\\'))
    
    def listdir(self, path):
        path = self.__convertPath(path)
        return [os.path.basename(name) for name in self.zip.namelist() if os.path.dirname(name) == path]
    
    def file(self, path):
        return cStringIO.StringIO(self.read_file(path))
    
    def read_file(self, path):
        path = self.__convertPath(path)
        return self.zip.read(path)
    
    def exists(self, path):
        path = self.__convertPath(path)
        return path in self.zip.namelist()
    
    def subopen(self, path):
        path = self.__convertPath(path)
        return CZipStorage(self.zip, path)

StorageList.classes.append(CZipStorage)
