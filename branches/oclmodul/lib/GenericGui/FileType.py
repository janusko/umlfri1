from lib.Base import CBaseObject

class CFileType(CBaseObject):
    _persistent = True
    
    def __init__(self, mimeType, description):
        self.__mimeType = mimeType
        self.__description = description
        self.__importEnabled = False
        self.__exportEnabled = False
        self.__extensions = []
        self.__importHandler = None
        self.__exportHandler = None
    
    def GetMimeType(self):
        return self.__mimeType
    
    def GetDescription(self):
        return self.__description
    
    def GetImportEnabled(self):
        return self.__importEnabled
    
    def GetImportPossible(self):
        return bool(self.__extensions) and self.__importEnabled and self.__importHandler is not None
    
    def EnableImport(self):
        self.__importEnabled = True
    
    def DisableImport(self):
        self.__importEnabled = False
    
    def GetExportEnabled(self):
        return self.__exportEnabled
    
    def GetExportPossible(self):
        return bool(self.__extensions) and self.__exportEnabled and self.__exportHandler is not None
    
    def EnableExport(self):
        self.__exportEnabled = True
    
    def DisableExport(self):
        self.__exportEnabled = False
    
    def GetExtensions(self):
        for extension in self.__extensions:
            yield extension
    
    def AddExtension(self, extension):
        self.__extensions.append(extension)
    
    def RemoveExtension(self, extension):
        self.__extensions.remove(extension)
    
    def RegisterImportHandler(self, handler):
        self.__importHandler = handler
    
    def RegisterExportHandler(self, handler):
        self.__exportHandler = handler
    
    def Import(self, file):
        self.__importHandler(file)
    
    def Export(self, file):
        self.__exportHandler(file)
