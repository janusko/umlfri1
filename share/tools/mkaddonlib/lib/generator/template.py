from .fileListItem import FileListItem

from Cheetah.Template import Template as CheetahTemplate

class Template(FileListItem):
    def __init__(self, inputFile, outputFile, root):
        FileListItem.__init__(self, inputFile, outputFile, root)
    
    def generate(self, inputFile, root):
        return str(CheetahTemplate(file(inputFile).read(), {'root': root}))
