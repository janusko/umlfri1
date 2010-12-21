import re

class Identifier(object):
    __reIdentifierSplitter = re.compile('([A-Z][a-z0-9]+)')
    
    def __init__(self, identifier):
        self.__identifier = identifier
        self.__splittedIdentifier = [part.lower() for part in self.__reIdentifierSplitter.split(identifier) if part]
    
    @property
    def default(self):
        return self.__identifier
    
    @property
    def upperCamelCase(self):
        return ''.join([part.capitalize() for part in self.__splittedIdentifier])
    
    @property
    def lowerCamelCase(self):
        return self.__splittedIdentifier[0] + ''.join([part.capitalize() for part in self.__splittedIdentifier[1:]])
    
    @property
    def lowerUnderscoreSeparated(self):
        return '_'.join(self.__splittedIdentifier)
    
    @property
    def upperUnderscoreSeparated(self):
        return '_'.join(self.__splittedIdentifier).upper()
    
    @property
    def lowerCase(self):
        return ''.join(self.__identifier)
    
    @property
    def uppweCase(self):
        return ''.join(self.__upperCase)
    
    def __add__(self, str):
        return Identifier(self.lowerCamelCase + str)
    
    def __radd__(self, str):
        return Identifier(str + self.upperCamelCase)
