from .fileListItem import FileListItem
from .file import File

import glob
import os
import os.path

class Directory(FileListItem):
    def __init__(self, inputFile, outputFile, glob):
        FileListItem.__init__(self, inputFile, outputFile, None)
        
        self.__glob = glob
    
    def subItems(self, inputFile, outputFile):
        for item in glob.glob(os.path.join(inputFile, self.__glob)):
            yield File(item, os.path.join(outputFile, os.path.basename(item)))
        
        for item in os.listdir(inputFile):
            itemPath = os.path.join(inputFile, item)
            if os.path.isdir(itemPath) and not item.startswith('.'):
                yield Directory(itemPath, os.path.join(outputFile, item), self.__glob)
