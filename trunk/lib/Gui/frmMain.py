import pygtk
import gtk
from common import CWindow, event
import common

import os.path

from lib.Drawing import CElement
from lib.Elements import CElementObject
from dialogs import CWarningDialog, CQuestionDialog, ECancelPressed
from lib.Drawing import CDrawingArea
from tbToolBox import CtbToolBox
from twProjectView import CtwProjectView
from mnuItems import CmnuItems
from picDrawingArea import CpicDrawingArea
from nbProperties import CnbProperties
from tabs import CTabs
from lib.lib import UMLException


class CfrmMain(CWindow):
    name = 'frmMain'
    widgets = ('hboxWorkSpace', 'mnuUseCaseDiagram',
        'twProjectView', 'lwProperties',
        #mItemFile
        'mnuOpen', 'mnuSave', 'mnuSaveAs', 'mnuQuit',
        #mItemEdit
        'mnuCut', 'mnuCopy', 'mnuPaste', 'mnuDelete',
        #mItemDiagrams
        #mItemView
        'mnuViewTools',
        #mItemHelp
        'mnuAbout',
        #toolbar
        'cmdOpen', 'cmdSave','cmdCopy','cmdCut','cmdPaste',
        'mnuExportSvg',
        #mZ-Order 'mMenuShift',
        'mmShift_SendBack', 'mmShift_BringForward', 'mmShift_ToBottom', 'mmShift_ToTop'
        )

    complexWidgets = (CtbToolBox, CtwProjectView, CmnuItems, CpicDrawingArea, CnbProperties, CTabs)

    def __init__(self, app, wTree):
        CWindow.__init__(self, app, wTree)

        self.form.maximize()
        self.mnuExportSvg.set_sensitive(False)

    # Diagrams
    @event("mnuViewTools", "activate")
    def on_mnuViewTools_activate(self, mnu):
        self.tbToolBox.SetVisible(mnu.get_active())

    # Help
    @event("mnuAbout", "activate")
    def on_mnuAbout_activate(self, mnu):
        tmp = self.application.GetWindow('frmAbout')
        tmp.SetParent(self)
        tmp.Show()
    
    @event('mnuExportSvg', 'activate')
    def on_mnuExportSvg_activate(self, widget):
        filedlg = gtk.FileChooserDialog('Choose SVG file', self.form, gtk.FILE_CHOOSER_ACTION_SAVE, (gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_SAVE,gtk.RESPONSE_OK))
        filter = gtk.FileFilter()
        filter.set_name("SVG vector images")
        filter.add_pattern('*.svg')
        filedlg.add_filter(filter)
        try:
            while True:
                if filedlg.run() == gtk.RESPONSE_OK:
                    filename = filedlg.get_filename()
                    if '.' not in os.path.basename(filename):
                        filename += '.svg'
                    if os.path.isfile(filename):
                        self.picDrawingArea.ExportSvg(filename)
                        return
                else:
                    return
        finally:
            filedlg.destroy()

    # Actions
    @event("form", "destroy")
    @event("mnuQuit", "activate")
    def ActionQuit(self, widget):
        self.application.Quit()

    @event("cmdOpen", "clicked")
    @event("mnuOpen", "activate")
    def ActionOpen(self, widget):
        filename, copy = self.application.GetWindow("frmOpen").ShowDialog(self)
        if filename is not None:
            try:
                if self.application.Project.GetFileName() is not None and CQuestionDialog(self.form, 'Do you want to save proejct?', True).run():
                    self.application.Project.SaveProject()
            except ECancelPressed:
                return
            self.application.Project.LoadProject(filename, copy)
            self.nbTabs.CloseAll()
            self.twProjectView.Redraw()


    @event("cmdSave", "clicked")
    @event("mnuSave", "activate")
    def ActionSave(self, widget):
        if self.application.Project.GetFileName() is None:
            self.ActionSaveAs(widget)
        else:
            self.application.Project.SaveProject()

    @event("mnuSaveAs", "activate")
    def ActionSaveAs(self, widget):
        filename = self.application.GetWindow("frmSave").ShowDialog(self)
        if filename is not None:
            self.application.Project.SaveProject(filename)

    @event("mnuDelete","activate")
    def on_mnuDelete_click(self, widget):
        self.picDrawingArea.DeleteElements()
    
    @event("cmdCut", "clicked")
    @event("mnuCut","activate")
    def on_mnuCut_click(self, widget):
        if len(tuple(self.picDrawingArea.GetDrawingArea().GetSelected())) > 0:
            self.application.Clipboard.SetContent(tuple(self.picDrawingArea.GetDrawingArea().GetSelected()))
            for i in self.picDrawingArea.GetDrawingArea().GetSelected():
                if isinstance(i, CElement):
                    self.picDrawingArea.GetDrawingArea().DeleteElement(i)
            self.picDrawingArea.Paint()
        

    @event("cmdCopy", "clicked")
    @event("mnuCopy","activate")
    def on_mnuCopy_click(self, widget):
        if len(tuple(self.picDrawingArea.GetDrawingArea().GetSelected())) > 0:
            self.application.Clipboard.SetContent(tuple(self.picDrawingArea.GetDrawingArea().GetSelected()))
    
    
    @event("cmdPaste", "clicked")
    @event("mnuPaste","activate")
    def on_mnuPaste_click(self, widget):
        drawingArea = self.picDrawingArea.GetDrawingArea()
        drawingArea.DeselectAll()
        for i in self.application.Clipboard.GetContent() or []:
            if isinstance(i,CElement):
                try:
                    Element = CElement(drawingArea, i.GetObject())
                except UMLException, e:
                    if e.GetName() == "ElementAlreadyExists":
                        return CWarningDialog(self.form, "Pozeraj sa co robis").run()
                    elif e.GetName() == "DiagramHaveNotThisElement": 
                        return CWarningDialog(self.form, "Zly element: " + i.GetObject().GetType().GetId()).run()
                Element.CopyFromElement(i)
                i.GetObject().AddAppears(drawingArea)
                drawingArea.AddToSelection(Element)
        self.picDrawingArea.Paint()


    def ActionLoadToolBar(self, widget):
        pass

    # Moje vlastne signale
    @event("picDrawingArea", "add-element")
    def on_add_element(self, widget, Element, drawingArea):
        self.twProjectView.AddElement(Element, drawingArea)



    @event("mnuItems", "create-diagram")
    @event("twProjectView","create-diagram")
    def on_mnuItems_create_diagram(self, widget, diagramId):
        area = CDrawingArea(self.application.Project.GetDiagramFactory().GetDiagram(diagramId))
        self.twProjectView.AddDrawingArea(area)
        self.nbTabs.AddTab(area)
        self.picDrawingArea.SetDrawingArea(area)
        self.tbToolBox.SetButtons(diagramId)

    @event("picDrawingArea", "get-selected")
    def on_picDrawingArea_get_selected(self, widget):
        return self.tbToolBox.GetSelected()


    @event("twProjectView", "selected_drawing_area")
    def on_select_drawing_area(self, widget, drawingArea):
        self.nbTabs.AddTab(drawingArea)
        self.picDrawingArea.SetDrawingArea(drawingArea)

    @event("twProjectView", "close-drawing-area")
    def on_remove_drawing_area(self, widget, drawingArea):
        self.nbTabs.CloseTab(drawingArea)

    @event("nbTabs", "change_current_page")
    def on_change_drawing_area(self, widget, drawingArea):
        if drawingArea is None:
            self.picDrawingArea.Hide()
            self.tbToolBox.SetButtons(None)
            self.mnuExportSvg.set_sensitive(False)
        else:
            self.picDrawingArea.Show()
            self.picDrawingArea.SetDrawingArea(drawingArea)
            self.tbToolBox.SetButtons(drawingArea.GetType().GetId())
            self.mnuExportSvg.set_sensitive(True)

    @event("picDrawingArea", "set-selected")
    def on_picDrawingArea_set_selected(self, widget, selected):
        self.tbToolBox.SetSelected(selected)

    @event("picDrawingArea", "selected-item")
    def on_picDrawingArea_selected_item(self, widget, selected):
        self.nbProperties.Fill(selected)

    @event("picDrawingArea","delete-element-from-all")
    def on_picDrawingArea_delete_selected_item(self, widget, selected):
        self.twProjectView.DeleteElement(selected)

    @event("twProjectView", "selected-item-tree")
    def on_twTreeView_selected_item(self, widget, selected):
        self.picDrawingArea.DrawingArea.DeselectAll()
        self.picDrawingArea.Paint()
        self.nbProperties.Fill(selected)

    @event("twProjectView", "repaint")
    def on_repaint_picDravingArea(self, widget):
        self.picDrawingArea.Paint()


    @event("nbProperties", "content-update")
    def on_nbProperties_content_update(self, widget, element, property):
        if element.GetObject().GetType().HasVisualAttribute(property):
            self.picDrawingArea.Paint()
            self.twProjectView.UpdateElement(element.GetObject())

    @event("tbToolBox", "toggled")
    def on_tbToolBox_toggled(self, widget, ItemId, ItemType):
        self.picDrawingArea.ResetAction()
        
    @event("picDrawingArea","drop-from-treeview")
    def on_drop_from_treeview(self, widget, position):
        node = self.twProjectView.GetSelectedNode()
        if node is not None:
            drawingArea = self.picDrawingArea.GetDrawingArea()
            try:
                Element = CElement(drawingArea, node.GetObject()).SetPosition(position)
            except UMLException, e:
                if e.GetName() == "ElementAlreadyExists":
                    return CWarningDialog(self.form, "Pozeraj sa co robis").run()
                elif e.GetName() == "DiagramHaveNotThisElement": 
                    return CWarningDialog(self.form, "Zly element: " + node.GetObject().GetType().GetId()).run()
                
            node.AddAppears(drawingArea)
    
    @event("picDrawingArea", "run-dialog")
    def on_run_dialog(self, widget, type, message):
        if type == 'warning':
            return CWarningDialog(self.form, message).run()
        else:
            pass
    
    #Z-Order 
# 'mmShift_SendBack', 'mmShift_BringForward', 'mmShift_ToBottom', 'mmShift_ToTop'    
    @event("mmShift_SendBack", "activate")
    def on_mnuItems_mmShift_SendBack(self, menuItem):
        self.picDrawingArea.on_pmShift_SendBack_activate(None)
        
    @event("mmShift_BringForward", "activate")
    def on_mnuItems_mmShift_BringForward(self, menuItem):
        self.picDrawingArea.on_pmShift_BringForward_activate(None)
        
    @event("mmShift_ToBottom", "activate")
    def on_mnuItems_mmShift_ToBottom(self, menuItem):
        self.picDrawingArea.on_pmShift_ToBottom_activate(None)
        
    @event("mmShift_ToTop", "activate")
    def on_mnuItems_mmShift_ToTop(self, menuItem):
        self.picDrawingArea.on_pmShift_ToTop_activate(None)        
