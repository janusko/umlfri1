import os
import os.path

class FileListItem(object):
    def __init__(self, inputFile, outputFile, root):
        self.__inputFile = inputFile
        self.__outputFile = outputFile
        self.__root = root
    
    def create(self, dir):
        reldir = os.path.dirname(self.__outputFile)
        relfile = os.path.basename(self.__outputFile)
        dir = os.path.abspath(os.path.join(dir, reldir))
        
        self.__mkdir(dir)
        
        with file(os.path.join(dir, relfile)) as f:
            f.write(self.generate(self.__inputFile, self.__root))
    
    def generate(self, inputFile, root):
        raise Exception()
    
    def finish(self):
        pass
    
    def __mkdir(self, dir):
        if not os.path.exists(dir):
            self.__mkdir(os.path.dirname(dir))
            os.mkdir(dir)
