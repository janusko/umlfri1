from common import CWindow, event
from lib.datatypes import CColor
import os
import re

class CfrmExport(CWindow):
    name = 'frmExport'
    glade = 'export.glade'
    
    widgets = ('entExportFileName','fcbDirectorySelect', 'tbtnPDF', 'tbtnPNG', 'tbtnPS', 'tbtnSVG',
    'btnExport', 'btnCancelExport', 'hbuttonboxExportType', 'chbBackground', 'cbBackground',
    'spinExportZoom', 'spinExportPadding')
    
    def __init__(self, app, wTree):
        CWindow.__init__(self, app, wTree)
        self.picDrawingArea = None        
    
    def setArea(self, picDrawingArea):
        self.picDrawingArea = picDrawingArea
    
    def Show(self):
        self.tbtnPDF.set_active(True)
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

    @event("chbBackground", "toggled")
    def onChbBackgroundToggled(self, widget):
        self.cbBackground.set_sensitive(widget.get_active())

    @event("entExportFileName", "focus-out-event")
    def OnEntExportFileNameFocusLost(self, widget, event):

        if self.entExportFileName.get_text().strip(' ') == '':
            self.entExportFileName.set_text(self.picDrawingArea.GetDiagram().GetName())
        

    @event("entExportFileName", "changed")
    def OnEntExportFileNameKeyPress(self, event):
        #do not allow these characters in filename
        p = re.compile("[:?\\\/*\"<>|]")
        filename = self.entExportFileName.get_text()
        filename = p.sub("", filename)
        self.entExportFileName.set_text(filename)

        
    @event("btnExport", "clicked")
    def OnBtnExportClicked(self, widget):
        
        filename = os.path.join(self.fcbDirectorySelect.get_current_folder(), self.entExportFileName.get_text())
        if self.chbBackground.get_active():
            color = self.cbBackground.get_color()
            color = CColor('#%02x%02x%02x'%(color.red >> 8, color.green >> 8, color.blue >> 8))
        else:
            color = None
        
        zoom = self.spinExportZoom.get_value_as_int()
        padding = self.spinExportPadding.get_value_as_int()
        
        if self.tbtnSVG.get_active():        
            self.picDrawingArea.Export(filename + '.svg', 'svg', zoom, padding, color)
        
        if self.tbtnPDF.get_active():        
            self.picDrawingArea.Export(filename + '.pdf', 'pdf', zoom, padding, color)
        
        if self.tbtnPNG.get_active():        
            self.picDrawingArea.Export(filename + '.png', 'png', zoom, padding, color)
        
        if self.tbtnPS.get_active():        
            self.picDrawingArea.Export(filename + '.ps', 'ps', zoom, padding, color)

