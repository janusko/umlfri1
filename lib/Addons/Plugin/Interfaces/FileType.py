from .Decorators import params, mainthread, polymorphic

class IFileType(object):
    def __init__(self, plugin, fileType):
        self.__plugin = plugin
        self.__fileType = fileType
    
    @property
    def uid(self):
        return self.__fileType.GetUID()
    
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
    
    def AttachExportHandler(self):
        self.__fileType.RegisterExportHandler(self.__exportHandler)
    
    def DetachExportHandler(self):
        self.__fileType.RegisterExportHandler(self.__exportHandler)
    
    def AttachImportHandler(self):
        self.__fileType.RegisterExportHandler(self.__importHandler)
    
    def DetachImportHandler(self):
        self.__fileType.RegisterExportHandler(self.__importHandler)
    
    def __exportHandler(self, fileName, fileType):
        self.__plugin.FireEvent(self, 'ExportHandler', fileName = fileName, fileType = fileType)
    
    def __importHandler(self, fileName, fileType):
        self.__plugin.FireEvent(self, 'ImportHandler', fileName = fileName, fileType = fileType)
