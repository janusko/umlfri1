import lib.GenericGui
from base import IBase

class IFileType(IBase):
    
    __cls__ = lib.GenericGui.CFileType
    
    def GetDescription(him):
        return him.GetDescription()
    
    def GetMimeType(him):
        return him.GetMimeType()
    
    def GetExportEnabled(him):
        return him.GetExportEnabled()
    
    def SetExportEnabled(him, value):
        if value:
            him.EnableExport()
        else:
            him.DisableExport()
    
    def GetImportEnabled(him):
        return him.GetImportEnabled()
    
    def SetImportEnabled(him, value):
        if value:
            him.EnableImport()
        else:
            him.DisableImport()
    
    def AddExtension(him, extension):
        him.AddExtension(extension)
    
    def RegisterExportHandler(him, handler):
        him.RegisterExportHandler(handler)
    
    def RegisterImportHandler(him, handler):
        him.RegisterImportHandler(handler)
