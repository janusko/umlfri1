import gtk
import pygtk
import gobject
from lib.Gui.frmPropertiesWidgets.GTK.Button import CButton
from lib.Gui.frmPropertiesWidgets.Abstract.AbstractTable import CAbstractTable

class CTable(CAbstractTable):
    
    def __init__(self,model,delete,save,new):
        self.last_select=None
        self.row_object=[]
        cols=[]
        types=[]
        for name in model:
            cell=gtk.CellRendererText()
            col=gtk.TreeViewColumn(name)
            col.pack_start(cell)
            col.set_resizable(True)
            col.set_expand(True)
            col.set_attributes(cell,text=model.index(name))
            cols.append(col)
            types.append(gobject.TYPE_STRING)
        liststore=gtk.ListStore(*types)
        self.table=gtk.TreeView(liststore)
        self.table.set_size_request(-1, 100)
        self.table.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_HORIZONTAL)
        for i in range(len(model)):
            self.table.append_column(cols[i])
        window=gtk.ScrolledWindow()
        window.set_policy(gtk.POLICY_AUTOMATIC,gtk.POLICY_AUTOMATIC)
        window.add(self.table)
        vbox=gtk.VBox()
        hbox=gtk.HBox()
        hbox.pack_end(new.GetWidget(),False,False,1)
        hbox.pack_end(save.GetWidget(),False,False,1)
        hbox.pack_end(delete.GetWidget(),False,False,1)
        vbox.pack_start(hbox,False,False)
        vbox.pack_start(window,True,True)
        self.frm=gtk.Frame()
        self.frm.add(vbox)
        self.frm.show_all()
        
    
    def GetWidget(self):
        return self.frm
    
    def Clear(self):
        self.table.get_model().clear()
    
    def AppendRow(self,data,row_object):
        self.table.get_model().append(data)
        self.row_object.append(row_object)
    
    def RemoveRow(self,idx):
        self.table.get_model().remove(self.table.get_model().get_iter(idx))
        self.row_object.remove(self.row_object[idx])
    
    def GetRowObject(self,idx):
        return self.row_object[idx]
    
    def GetAllRowObjects(self):
        return self.row_object
    
    def SetCellValue(self,row,col,value):
        self.table.get_model().set_value(self.table.get_model().get_iter(row),col,value)
    
    def GetSelectedRowIndex(self):
        model,iter=self.table.get_selection().get_selected()
        if iter!=None:
            return model.get_path(iter)[0]
        else:
            return -1
    
    def UnselectAll(self):
        self.table.get_selection().unselect_all()
    
    def SelectLast(self):
        if self.last_select is not None:
            self.table.get_selection().select_path(self.last_select)
        else:
            self.table.get_selection().unselect_all()
    
    def SetLastSelect(self,path):
        self.last_select=path
     
    def GetLastSelect(self):
        return self.last_select
    
    def SetHandler(self,event,func,data):
        if event=='row-selected':
            self.table.connect('cursor-changed',self.__TableEventHandler,func,data)
    
    def __TableEventHandler(self,button,func,data):
        func(*data)