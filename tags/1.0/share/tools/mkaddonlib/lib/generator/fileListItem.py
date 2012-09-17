import os
import os.path

class FileListItem(object):
    def __init__(self, inputFile, outputFile, root):
        self.__inputFile = inputFile
        self.__outputFile = outputFile
        self.__root = root
    
    def create(self, dir):
        subitems = self.subItems(self.__inputFile, self.__outputFile)
        
        if subitems is not None:
            for subitem in subitems:
                subitem.create(dir)
        else:
            reldir = os.path.dirname(self.__outputFile)
            relfile = os.path.basename(self.__outputFile)
            dir = os.path.abspath(os.path.join(dir, reldir))
            
            self.__mkdir(dir)
            
            self.createFile(self.__inputFile, os.path.join(dir, relfile), self.__root)
        
    def createFile(self, inputFile, outputFile, root):
        with file(outputFile, 'w') as f:
            f.write(self.generate(inputFile, root))
    
    def subItems(self, inputFile, outputFile):
        return None
    
    def generate(self, inputFile, root):
        raise Exception()
    
    def finish(self):
        pass
    
    def __mkdir(self, dir):
        if not os.path.exists(dir):
            self.__mkdir(os.path.dirname(dir))
            os.mkdir(dir)
