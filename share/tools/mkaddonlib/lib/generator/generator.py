from .fileListItem import FileListItem

class Generator(FileListItem):
    def generate(self, inputFile, root):
        locals = {}
        globals = {}
        execfile(inputFile, globals, locals)
        return locals['generate'](root)
