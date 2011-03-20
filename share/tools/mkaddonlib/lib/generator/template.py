from .fileListItem import FileListItem

import os
import os.path
from Cheetah.Template import Template as CheetahTemplate

class Template(FileListItem):
    def __init__(self, inputFile, outputFile, root):
        FileListItem.__init__(self, inputFile, outputFile, root)
    
    def generate(self, inputFile, root):
        oldDir = os.getcwd()
        os.chdir(os.path.dirname(inputFile))
        try:
            return str(CheetahTemplate(file = inputFile, namespaces = {'root': root}))
        finally:
            os.chdir(oldDir)
