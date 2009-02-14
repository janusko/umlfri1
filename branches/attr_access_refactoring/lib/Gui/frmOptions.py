from lib.Depend.gtk2 import gtk

import common
from lib.config import config
from common import event
from lib.datatypes import CColor, CFont

class CfrmOptions(common.CWindow):
    #widgets = ('labelOptions',)
    widgets = ('cbElementLine', 'cbElementFill', 'cbElementFill2', 'cbElementFill3', 'cbElementShadow', 'cbElementNameText', 'cbElementText', 'fbElementNameText','fbElementText' ,'cbConnectionLine', 'cbConnectionArrow', 'cbConnectionArrowFill', 'cbConnectionNameText', 'cbConnectionText', 'fbConnectionNameText', 'fbConnectionText', 'sbSelectionPointsSize', 'cbSelectionPoints', 'cbSelectionRectangle' ,'sbSelectionRectangleWidth', 'cbDragRectangle', 'sbDragRectangleWidth', 'txtRootPath', 'txtTemplatesPath', 'txtImagesPath', 'txtGuiPath', 'txtLocalesPath', 'txtUserDirPath', 'txtUserConfigDirPath', 'txtRecentFilesPath', 'expElement', 'expSelection', 'expConnection', 'expDrag')
    name = 'frmOptions'
    
    def CColorToGtkColor(self, color):
        return gtk.gdk.color_parse(str(color))
    
    def CFontToFontString(self, font):
        return str(font)
    
    def GtkColorToCColor(self, color):
        return CColor('#%02x%02x%02x'%(color.red >> 8, color.green >> 8, color.blue >> 8))
    
    def FontStringToCFont(self, font):
        return CFont(font)

    def Show(self):
        self.cbElementLine.set_color(self.CColorToGtkColor(config['/Styles/Element/LineColor']))
        self.cbElementFill.set_color(self.CColorToGtkColor(config['/Styles/Element/FillColor']))
        self.cbElementFill2.set_color(self.CColorToGtkColor(config['/Styles/Element/Fill2Color']))
        self.cbElementFill3.set_color(self.CColorToGtkColor(config['/Styles/Element/Fill3Color']))
        self.cbElementShadow.set_color(self.CColorToGtkColor(config['/Styles/Element/ShadowColor']))
        self.cbElementNameText.set_color(self.CColorToGtkColor(config['/Styles/Element/NameTextColor']))
        self.cbElementText.set_color(self.CColorToGtkColor(config['/Styles/Element/TextColor']))
        self.cbConnectionLine.set_color(self.CColorToGtkColor(config['/Styles/Connection/LineColor']))
        self.cbConnectionArrow.set_color(self.CColorToGtkColor(config['/Styles/Connection/ArrowColor']))
        self.cbConnectionArrowFill.set_color(self.CColorToGtkColor(config['/Styles/Connection/ArrowFillColor']))
        self.cbConnectionNameText.set_color(self.CColorToGtkColor(config['/Styles/Connection/NameTextColor']))
        self.cbConnectionText.set_color(self.CColorToGtkColor(config['/Styles/Connection/TextColor']))
        self.cbSelectionPoints.set_color(self.CColorToGtkColor(config['/Styles/Selection/PointsColor']))
        self.cbSelectionRectangle.set_color(self.CColorToGtkColor(config['/Styles/Selection/RectangleColor']))
        self.cbDragRectangle.set_color(self.CColorToGtkColor(config['/Styles/Drag/RectangleColor']))
        self.fbElementNameText.set_font_name(self.CFontToFontString(config['/Styles/Element/NameTextFont']))
        self.fbElementText.set_font_name(self.CFontToFontString(config['/Styles/Element/TextFont']))
        self.fbConnectionNameText.set_font_name(self.CFontToFontString(config['/Styles/Connection/NameTextFont']))
        self.fbConnectionText.set_font_name(self.CFontToFontString(config['/Styles/Connection/TextFont']))
        self.sbSelectionPointsSize.set_value(config['/Styles/Selection/PointsSize'])
        self.sbSelectionRectangleWidth.set_value(config['/Styles/Selection/RectangleWidth'])
        self.sbDragRectangleWidth.set_value(config['/Styles/Drag/RectangleWidth'])
        self.txtRootPath.set_text(config['/Paths/Root'])
        self.txtTemplatesPath.set_text(config['/Paths/Templates'])
        self.txtImagesPath.set_text(config['/Paths/Images'])
        self.txtGuiPath.set_text(config['/Paths/Gui'])
        self.txtLocalesPath.set_text(config['/Paths/Locales'])
        self.txtUserDirPath.set_text(config['/Paths/UserDir'])
        self.txtUserConfigDirPath.set_text(config['/Paths/UserConfig'])
        self.txtRecentFilesPath.set_text(config['/Paths/RecentFiles'])
        
        if self.form.run() == gtk.RESPONSE_OK:
            #config['/Styles/Element/LineColor'] = self.cbElementLine.get_color()
            #(gtk.gdk.color_parse(config['/Styles/Element/NameTextColor'])
            config['/Styles/Element/LineColor'] = self.GtkColorToCColor(self.cbElementLine.get_color())
            config['/Styles/Element/FillColor'] = self.GtkColorToCColor(self.cbElementFill.get_color())
            config['/Styles/Element/Fill2Color'] = self.GtkColorToCColor(self.cbElementFill2.get_color())
            config['/Styles/Element/Fill3Color'] = self.GtkColorToCColor(self.cbElementFill3.get_color())
            config['/Styles/Element/ShadowColor'] = self.GtkColorToCColor(self.cbElementShadow.get_color())
            config['/Styles/Element/NameTextColor'] = self.GtkColorToCColor(self.cbElementNameText.get_color())
            config['/Styles/Element/TextColor'] = self.GtkColorToCColor(self.cbElementText.get_color())
            config['/Styles/Connection/LineColor'] = self.GtkColorToCColor(self.cbConnectionLine.get_color())
            config['/Styles/Connection/ArrowColor'] = self.GtkColorToCColor(self.cbConnectionArrow.get_color())
            config['/Styles/Connection/ArrowFillColor'] = self.GtkColorToCColor(self.cbConnectionArrowFill.get_color())
            config['/Styles/Connection/NameTextColor'] = self.GtkColorToCColor(self.cbConnectionNameText.get_color())
            config['/Styles/Connection/TextColor'] = self.GtkColorToCColor(self.cbConnectionText.get_color())
            config['/Styles/Selection/PointsColor'] = self.GtkColorToCColor(self.cbSelectionPoints.get_color())
            config['/Styles/Selection/RectangleColor'] = self.GtkColorToCColor(self.cbSelectionRectangle.get_color())
            config['/Styles/Drag/RectangleColor'] = self.GtkColorToCColor(self.cbDragRectangle.get_color())
            config['/Styles/Element/NameTextFont'] = self.FontStringToCFont(self.fbElementNameText.get_font_name())
            config['/Styles/Element/TextFont'] = self.FontStringToCFont(self.fbElementText.get_font_name())
            config['/Styles/Connection/NameTextFont'] = self.FontStringToCFont(self.fbConnectionNameText.get_font_name())
            config['/Styles/Connection/TextFont'] = self.FontStringToCFont(self.fbConnectionText.get_font_name())
            config['/Styles/Selection/PointsSize'] = self.sbSelectionPointsSize.get_value_as_int()
            config['/Styles/Selection/RectangleWidth'] = self.sbSelectionRectangleWidth.get_value_as_int()
            config['/Styles/Drag/RectangleWidth'] = self.sbDragRectangleWidth.get_value_as_int()
            config['/Paths/Root'] = self.txtRootPath.get_text()
            config['/Paths/Templates'] = self.txtTemplatesPath.get_text()
            config['/Paths/Images'] = self.txtImagesPath.get_text()
            config['/Paths/Gui'] = self.txtGuiPath.get_text()
            config['/Paths/Locales'] = self.txtLocalesPath.get_text()
            config['/Paths/UserDir'] = self.txtUserDirPath.get_text()
            config['/Paths/UserConfig'] = self.txtUserConfigDirPath.get_text()
            config['/Paths/RecentFiles'] = self.txtRecentFilesPath.get_text()

        self.Hide()
        
    @event("expElement", "activate")
    @event("expConnection", "activate")
    @event("expSelection", "activate")
    @event("expDrag", "activate")
    def on_exapander_activate(self, widget):
        if widget is self.expElement:
            #self.expElement.set_expanded(False)
            self.expConnection.set_expanded(False)
            self.expSelection.set_expanded(False)
            self.expDrag.set_expanded(False)
        if widget is self.expConnection:
            self.expElement.set_expanded(False)
            #self.expConnection.set_expanded(False)
            self.expSelection.set_expanded(False)
            self.expDrag.set_expanded(False)
        if widget is self.expSelection:
            self.expElement.set_expanded(False)
            self.expConnection.set_expanded(False)
            #self.expSelection.set_expanded(False)
            self.expDrag.set_expanded(False)
        if widget is self.expDrag:
            self.expElement.set_expanded(False)
            self.expConnection.set_expanded(False)
            self.expSelection.set_expanded(False)
            #self.expDrag.set_expanded(False)
