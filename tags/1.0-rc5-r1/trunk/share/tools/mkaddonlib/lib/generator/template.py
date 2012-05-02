from .fileListItem import FileListItem

import os
import os.path
from Cheetah.Template import Template as CheetahTemplate

class Template(FileListItem):
    def generate(self, inputFile, root):
        oldDir = os.getcwd()
        os.chdir(os.path.dirname(inputFile))
        try:
            return str(CheetahTemplate(file = inputFile, namespaces = {'root': root}))
        finally:
            os.chdir(oldDir)
