from GuiObject import CGuiObject

class CWidget(CGuiObject):
    widgets = ()
    complexWidgets = ()
    name = ''
    glade = None
    __allWidgets = {}
    
    def __init__(self, app, wTree):
        if self.glade is not None:
            if abspath(self.glade) in app.wTrees:
                wTree = app.wTrees[abspath(self.glade)] = gtk.glade.XML(self.glade)
            else:
                wTree = app.wTrees[abspath(self.glade)]
        for widgetName in self.widgets:
            if widgetName in self.__allWidgets:
                raise Exception, '%s cannot be used in %s (allready used in %s)'%(widgetName, self.__class__.__name__, self.__allWidgets[widgetName])
            else:
                self.__allWidgets[widgetName] = self.__class__.__name__
            obj = wTree.get_widget(widgetName)
            if obj is None:
                raise Exception, '%s could not be loaded'%(widgetName, )
            setattr(self, widgetName, obj)
        for widgetClass in self.complexWidgets:
            setattr(self, widgetClass.name, widgetClass(app, wTree))
        
        CGuiObject.__init__(self, app)
        self.GetRelativeFile = wTree.relative_file
