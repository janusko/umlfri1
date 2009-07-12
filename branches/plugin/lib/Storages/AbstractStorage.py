class CAbstractStorage(object):
    @staticmethod
    def create(path):
        return None
    
    def __init__(self):
        pass
    
    def listdir(self, path):
        return []
    
    def file(self, path):
        return None
    
    def read_file(self, path):
        return ''
    
    def exists(self, path):
        return False
