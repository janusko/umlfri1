from .fileListItem import FileListItem

class File(FileListItem):
    def __init__(self, inputFile, outputFile):
        FileListItem.__init__(self, inputFile, outputFile, None)
    
    def generate(self, inputFile, root):
        with file(inputFile, 'r') as f:
            return f.read()
