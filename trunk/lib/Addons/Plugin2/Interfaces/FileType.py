from ..PluginBase import params, mainthread, polymorphic

class IFileType(object):
    def __init__(self, fileType):
        self.__fileType = fileType
    
    def GetDescription(self):
        return self.__fileType.GetDescription()
    
    def GetMimeType(self):
        return self.__fileType.GetMimeType()
    
    def GetExportEnabled(self):
        return self.__fileType.GetExportEnabled()
    
    @params(bool)
    def SetExportEnabled(self, value):
        if value:
            self.__fileType.EnableExport()
        else:
            self.__fileType.DisableExport()
    
    def GetImportEnabled(self):
        return self.__fileType.GetImportEnabled()
    
    @params(bool)
    def SetImportEnabled(self, value):
        if value:
            self.__fileType.EnableImport()
        else:
            self.__fileType.DisableImport()
    
    @params(str)
    def AddExtension(self, extension):
        self.__fileType.AddExtension(extension)
    
    @params(callable)
    def RegisterExportHandler(self, handler):
        self.__fileType.RegisterExportHandler(handler)
    
    @params(callable)
    def RegisterImportHandler(self, handler):
        self.__fileType.RegisterImportHandler(handler)
