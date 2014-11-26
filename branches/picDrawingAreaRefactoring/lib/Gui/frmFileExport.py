from frmFileImportExportBase import CfrmFileImportExportBase

import os.path

class CfrmFileExport(CfrmFileImportExportBase):
    name = 'frmExportToFile'

    def __init__(self, app, wTree):
        CfrmFileImportExportBase.__init__(self, app, wTree, 'export')

    def OnOk(self, filename, fileType):
        if '.' not in os.path.basename(filename):
            for extension in fileType.GetExtensions():
                filename += '.' + extension
        
        fileType.Export(filename)
