from .fileListItem import FileListItem

class Generator(FileListItem):
    def __init__(self, inputFile, outputFile, root):
        FileListItem.__init__(self, inputFile, outputFile, root)
    
    def generate(self, inputFile, root):
        locals = {}
        globals = {}
        execfile(inputFile, globals, locals)
        return locals['generate'](root)
