from lib.Depend.gtk2 import gtk
from lib.Depend.gtk2 import gobject

from common import CWindow, event
from lib.Drawing import CElement, CConnection
from lib.Commands.AreaCommands import CAddConnectionCmd, CDeleteItemCmd


class CfrmProperties(CWindow):
    name = 'frmProperties'
    glade = 'properties.glade'
    
    widgets = ('nbProProperties', 'twConnections', )
    
    def __init__(self, app, wTree):
        CWindow.__init__(self, app, wTree)
        self.connModel = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_BOOLEAN)
        
        self.twConnections.append_column(gtk.TreeViewColumn(_("Object"), gtk.CellRendererText(), text = 0))
        self.twConnections.append_column(gtk.TreeViewColumn(_("Connection"), gtk.CellRendererText(), text = 1))
        renderer = gtk.CellRendererToggle()
        renderer.connect('toggled', self.__fixed_toggled)
        self.twConnections.append_column(gtk.TreeViewColumn(_("Visible"), renderer, active = 2))
        
        self.twConnections.set_model(self.connModel)
        
    
    def __fixed_toggled(self, cell, path):
        iter = self.connModel.get_iter((int(path),))
        self.connModel.set(iter, 2, not self.connModel.get_value(iter, 2))
        con = tuple(self.__elementObj.GetConnections())[int(path)]
        if con not in self.__connections:
            self.__connections.append(con)
        else:
            self.__connections.remove(con)
    
    def ShowProperties(self, what, elementObject, picDrawingArea, compositeCommand):
        self.__saved = False
        # this way of obtaining the composite command is a bit dorky,
        # but event nor connect can be used :(
        self.groupCmd = compositeCommand
        if isinstance(elementObject, CElement):
            isElement = True
            self.__elementObj = elementObject.GetObject()
            self.__connections = []
            self.element = elementObject
            if len(self.twConnections.get_columns()) < 3:
                renderer = gtk.CellRendererToggle()
                renderer.connect('toggled', self.__fixed_toggled)
                self.twConnections.append_column(gtk.TreeViewColumn(_("Visible"), renderer, active = 2))
        else:
            isElement = False
            self.__connections = None
            self.element = None
            self.__elementObj = elementObject
                
            if len(self.twConnections.get_columns()) == 3:
                self.twConnections.remove_column(self.twConnections.get_column(2))
        
        #Fill connections tree
        self.connModel.clear()
        for i in self.__elementObj.GetConnections():
            obj = i.GetConnectedObject(self.__elementObj)
            if isElement:
                self.connModel.set(self.connModel.append(), 0, obj.GetName(), 1, i.GetType().GetId(), 2, self.element.GetDiagram().HasConnectionObjectBool(i))
            else:
                self.connModel.set(self.connModel.append(), 0, obj.GetName(), 1, i.GetType().GetId())
       
        response = self.form.run()
        while response == gtk.RESPONSE_APPLY:
            self.__Save()
            picDrawingArea.Paint()
            response = self.form.run()
        if response == gtk.RESPONSE_OK: #or response == gtk.RESPONSE_APPLY :
            self.__Save()
        self.Hide()
        self.groupCmd = None
        return self.__saved
    
    def __Save(self):
        if self.__connections is not None:
            
            for i in self.__connections:
                con = self.element.GetDiagram().GetConnection(i)
                if con is not None:
                    d = CDeleteItemCmd(self.element.GetDiagram(), con)
                    self.groupCmd.Add(d)
                else:
                    diagram = self.element.GetDiagram()
                    if i.GetSource() is not self.__elementObj:
                        sour = diagram.HasElementObject(i.GetSource())
                        if sour is not None:
                            addConnection = CAddConnectionCmd(diagram, i, sour, self.element)
                            self.groupCmd.Add(addConnection)
                    elif i.GetDestination is not self.__elementObj:
                        dest = diagram.HasElementObject(i.GetDestination())
                        if dest is not None:
                            addConnection = CAddConnectionCmd(diagram, i, self.element, dest)
                            self.groupCmd.Add(addConnection)
            self.__connections = []
            self.__saved = True
