from lib.Depend.gtk2 import gtk

import common
from lib.config import config
from common import event
from lib.datatypes import CColor, CFont

class CfrmOptions(common.CWindow):
    name = 'frmOptions'
    glade = 'appSettings.glade'
    
    widgets = ('cbElementLine', 'cbElementFill', 'cbElementFill2', 'cbElementFill3', 'cbElementShadow', 'cbElementNameText', 'cbElementText', 'fbElementNameText','fbElementText' ,'cbConnectionLine', 'cbConnectionArrow', 'cbConnectionArrowFill', 'cbConnectionNameText', 'cbConnectionText', 'fbConnectionNameText', 'fbConnectionText', 'sbSelectionPointsSize', 'cbSelectionPoints', 'cbSelectionRectangle' ,'sbSelectionRectangleWidth', 'cbDragRectangle', 'sbDragRectangleWidth', 'expElement', 'expSelection', 'expConnection', 'expDrag',
               'cmdDefaultOptions')
            
    def __init__(self, app, wTree):
        common.CWindow.__init__(self, app, wTree)
        
        self.form.action_area.child_set_property(self.cmdDefaultOptions, 'secondary', True)
    
    def CColorToGtkColor(self, color):
        return gtk.gdk.color_parse(str(color))
    
    def CFontToFontString(self, font):
        return str(font)
    
    def GtkColorToCColor(self, color):
        return CColor('#%02x%02x%02x'%(color.red >> 8, color.green >> 8, color.blue >> 8))
    
    def FontStringToCFont(self, font):
        return CFont(font)

    def Show(self):
        self.__Load()
        
        if self.form.run() == gtk.RESPONSE_OK:
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

        self.Hide()
    
    def __Load(self):
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
    
    @event("cmdDefaultOptions", "clicked")
    def on_cmdDefaultOptions_clicked(self, widget):
        config.LoadDefaults()
        self.form.response(gtk.RESPONSE_CANCEL)
        
    @event("fbElementNameText", "font-set")
    @event("fbElementText", "font-set")
    @event("fbConnectionNameText", "font-set")
    @event("fbConnectionText", "font-set")
    def on_fontButton_clicked(self, widget):
        if widget is self.fbElementNameText:
            if self.FontStringToCFont(self.fbElementNameText.get_font_name()).GetSize() <= 0  or self.FontStringToCFont(self.fbElementNameText.get_font_name()).GetSize() >=72:
                self.fbElementNameText.set_font_name(self.CFontToFontString(config['/Styles/Element/NameTextFont']))
        if widget is self.fbElementText:
            if self.FontStringToCFont(self.fbElementText.get_font_name()).GetSize() <= 0 or self.FontStringToCFont(self.fbElementText.get_font_name()).GetSize() >= 72:
                self.fbElementText.set_font_name(self.CFontToFontString(config['/Styles/Element/TextFont']))
        if widget is self.fbConnectionNameText:
            if self.FontStringToCFont(self.fbConnectionNameText.get_font_name()).GetSize() <= 0  or self.FontStringToCFont(self.fbConnectionNameText.get_font_name()).GetSize() >=72 :
                self.fbConnectionNameText.set_font_name(self.CFontToFontString(config['/Styles/Connection/NameTextFont']))
        if widget is self.fbConnectionText:
            if self.FontStringToCFont(self.fbConnectionText.get_font_name()).GetSize() <= 0 or self.FontStringToCFont(self.fbConnectionText.get_font_name()).GetSize() >= 72:
                self.fbConnectionText.set_font_name(self.CFontToFontString(config['/Styles/Connection/TextFont']))