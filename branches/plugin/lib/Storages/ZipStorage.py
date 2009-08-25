import os.path
import os
import zipfile
import cStringIO
import re

import StorageList
from AbstractStorage import CAbstractStorage

from lib.Exceptions import *

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
    
    @staticmethod
    def duplicate(storage, path):
        root = path
        
        zip = zipfile.ZipFile(root, 'w')
        for path, files, dirs in storage.walk():
            for fname in files:
                zip.writestr('/'.join((path, fname)), storage.read_file(os.path.join(path, fname)))
        zip.close()
        
        return CZipStorage(root, '')
    
    def __init__(self, file, path):
        if isinstance(file, zipfile.ZipFile):
            self.zip = file
        else:
            self.zip = zipfile.ZipFile(file, 'r')
        self.path = path
    
    def __convertPath(self, path):
        return reMulSep.sub('/', '/'.join((self.path, path)).replace('\\', '/').strip('/'))
    
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
    
    def destroy(self):
        if self.path != '':
            raise StorageDestroyError("Cannot destroy storage from within zip file")
        
        os.unlink(self.zip.filename)
    
    def __walk(self, root, dir):
        fnames = []
        dnames = []
        for name, value in dir.iteritems():
            if value is None:
                fnames.append(name)
            else:
                dnames.append(name)
        
        yield root, dnames, fnames
        
        for d in dnames:
            if root == '':
                new_root = d
            else:
                new_root = root + '/' + d
                
            for item in self.__walk(new_root, dir[d]):
                yield item
    
    def walk(self):
        dir = {}
        for fname in self.zip.namelist():
            fname = fname.replace('\\', '/').lstrip('/')
            if not fname.startswith(self.path):
                continue
            
            fparts = fname[len(self.path):].split('/')
            
            while fparts and fparts[0] == '':
                del fparts[0]
            
            if not fparts:
                continue
            
            tmp = dir
            for part in fparts[:-1]:
                tmp = tmp.setdefault(part, {})
            
            if fparts[-1]:
                tmp[fparts[-1]] = None
        
        return list(self.__walk('', dir))
    
    def get_path(self):
        return os.path.join(self.zip.filename, self.path)

StorageList.classes.append(CZipStorage)
