from lib.Depend.gtk2 import pango
import lib.Depend

from common import CWindow, event
import os

class CfrmExport(CWindow):
    name = 'frmExport'
    glade = 'project.glade'
    
    widgets = ('entExportFileName','fcbDirectorySelect', 'tbtnPDF', 'tbtnPNG', 'tbtnPS', 'tbtnSVG',
    'btnExport', 'btnCancelExport', 'hbuttonboxExportType', )
    
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
    def OnToggleButtonToggle(self, widget):
    # just makes sure that at least one export type
    # is selected -- the default export type is SVG
        isSomeToggled = False
        for toggleBtn in self.hbuttonboxExportType.get_children():
            if toggleBtn.get_active():
                isSomeToggled = True
                break
        if not isSomeToggled:
            self.tbtnSVG.set_active(True)
            

    @event("entExportFileName", "focus-out-event")
    def OnEntExportFileNameFocusLost(self, widget, event):
        
        if self.entExportFileName.get_text().strip(' ') == '':
            self.entExportFileName.set_text(self.picDrawingArea.GetDiagram().GetName())


    @event("btnExport", "clicked")
    def OnBtnExportClicked(self, widget):
        
        filename = os.path.join(self.fcbDirectorySelect.get_current_folder(), self.entExportFileName.get_text())
        
        if self.tbtnSVG.get_active():        
            self.picDrawingArea.Export(filename + '.svg', 'svg')
        
        if self.tbtnPDF.get_active():        
            self.picDrawingArea.Export(filename + '.pdf', 'pdf')
        
        if self.tbtnPNG.get_active():        
            self.picDrawingArea.Export(filename + '.png', 'png')
        
        if self.tbtnPS.get_active():        
            self.picDrawingArea.Export(filename + '.ps', 'ps')

