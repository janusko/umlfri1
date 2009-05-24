from lib.Depend.gtk2 import pango
import lib.Depend

from common import CWindow, event
from lib.config import config
import lib.consts, os

class CfrmExport(CWindow):
    widgets = ('entExportFileName','fcbDirectorySelect', 'tbtnPDF', 'tbtnPNG', 'tbtnPS', 'tbtnSVG',
    'btnExport', 'btnCancelExport', 'hbuttonboxExportType', )
    name = 'frmExport'
    
    def __init__(self, app, wTree):
        CWindow.__init__(self, app, wTree)
        self.picDrawingArea = None        
        # default values
        self.tbtnSVG.set_active(True)
    
    def setArea(self, picDrawingArea):
        self.picDrawingArea = picDrawingArea
    
    def Show(self):
        self.entExportFileName.set_text(self.picDrawingArea.GetDiagram().GetName())
        self.form.run()
        self.Hide()

    @event("tbtnPDF", "toggled")
    @event("tbtnPNG", "toggled")
    @event("tbtnPS", "toggled")
    @event("tbtnSVG", "toggled")    
    def OnToogleButtonToogle(self, widget):
    # just makes sure that at least one export type
    # is selected -- the default export type is SVG
        isSomeToogled = False
        for toogleBtn in self.hbuttonboxExportType.get_children():
            if toogleBtn.get_active():
                isSomeToogled = True
                break
            
        if not isSomeToogled:
            self.tbtnSVG.set_active(True)
            

    @event("btnExport", "clicked")
    def OnLbtnProjectWebClicked(self, widget):
        
        filename = os.path.join(self.fcbDirectorySelect.get_current_folder(), self.entExportFileName.get_text())
        
        if self.tbtnSVG.get_active():        
            self.picDrawingArea.Export(filename + '.svg', 'svg')
        
        if self.tbtnPDF.get_active():        
            self.picDrawingArea.Export(filename + '.pdf', 'pdf')
        
        if self.tbtnPNG.get_active():        
            self.picDrawingArea.Export(filename + '.png', 'png')
        
        if self.tbtnPS.get_active():        
            self.picDrawingArea.Export(filename + '.ps', 'ps')

