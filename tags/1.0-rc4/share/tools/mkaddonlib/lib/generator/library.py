import sys

class Library(object):
    def __init__(self, path):
        self.__path = path.split(':')
    
    def create(self, dir):
        for dir in self.__path:
            sys.path.append(dir)
    
    def finish(self):
        for dir in self.__path:
            sys.path.remove(dir)
