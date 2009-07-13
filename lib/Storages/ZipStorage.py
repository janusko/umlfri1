import os.path
import os
import zipfile
import cStringIO
import re

reMulSep = re.compile('/{2,}')

from AbstractStorage import CAbstractStorage

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
        self.zip = zipfile.ZipFile(file, 'r')
        self.path = path
    
    def listdir(self, path):
        path = reMulSep.sub('/', '/'.join((self.path, path)).rstrip('/\\'))
        return [os.path.basename(name) for name in self.zip.namelist() if os.path.dirname(name) == path]
    
    def file(self, path):
        return cStringIO.StringIO(self.read_file(path))
    
    def read_file(self, path):
        path = reMulSep.sub('/', '/'.join((self.path, path))).lstrip('/')
        return self.zip.read(path)
    
    def exists(self, path):
        path = reMulSep.sub('/', '/'.join((self.path, path))).lstrip('/')
        return path in self.zip.namelist()
        
    @staticmethod
    def _createStruct(list, prefix = '', idx=0):
        
        files = []
        dirs = {}
        
        while idx < len(list):
            line = list[idx]
            if line.startswith(prefix):
                name =  line[len(prefix):]
                if line.endswith('/'):
                    dirs[name[:-1]], idx = CZipStorage._createStruct(list, line, idx+1)
                else:
                    files.append(name)
                    idx += 1
            else:
                return (dirs, files), idx
        return (dirs, files), idx
    
    @staticmethod
    def _walk(name, dir):
        dirlist = dir[0].keys()
        yield name, dirlist, dir[1]
        for idir in dirlist:
            for item in CZipStorage._walk(os.path.join(name, idir), dir[0][idir]):
                yield item
    
    def walk(self):
        dir = CZipStorage._createStruct(self.zip.namelist())[0]
        for item in CZipStorage._walk('', dir):
            yield item
