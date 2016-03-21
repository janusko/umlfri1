from frmFileImportExportBase import CfrmFileImportExportBase

class CfrmFileImport (CfrmFileImportExportBase):
    name = "frmImport"

    def __init__(self, app, wTree):
        CfrmFileImportExportBase.__init__(self, app, wTree, 'import')

    def OnOk(self, filename, fileType):        
        fileType.Import(filename)
