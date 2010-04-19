import gtk
import pygtk
from lib.Gui.frmPropertiesWidgets.GTK.Button import CButton
from lib.Gui.frmPropertiesWidgets.GTK.ComboBox import CComboBox
from lib.Gui.frmPropertiesWidgets.GTK.EditableComboBox import CEditableComboBox
from lib.Gui.frmPropertiesWidgets.GTK.EditBox import CEditBox
from lib.Gui.frmPropertiesWidgets.GTK.TextArea import CTextArea
from lib.Gui.frmPropertiesWidgets.GTK.EditBoxWithButton import CEditBoxWithButton
from lib.Gui.frmPropertiesWidgets.GTK.Table import CTable
from lib.Gui.frmPropertiesWidgets.Abstract.AbstractDialog import CAbstractDialog

class CDialog(CAbstractDialog):
    
    def __init__(self,parent,title=''):
        self.dialog=gtk.Dialog(title,parent,gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT | gtk.WINDOW_TOPLEVEL)
        self.dialog.set_position(gtk.WIN_POS_MOUSE)
        self.dialog_tabs=self.dialog_tabs=gtk.Notebook()
        self.dialog.vbox.pack_start(self.dialog_tabs,True,True)
        self.dialog_tabs.show()
        self.dialog_tab={}
        self.dialog_tab_items_count={}
    
    def SetWidget(self,dialog):
        self.dialog=dialog
    
    def GetWidget(self):
        return self.dialog
    
    def SetTitle(self,title):
        self.dialog.set_title(title)
    
    def SetSize(self,x,y):
        self.dialog.resize(x,y)
    
    def GetSize(self):
        return self.dialog.get_size()
    
    def Close(self):
        self.dialog.destroy()
    
    def Show(self):
        self.dialog.show()
    
    def AppendButton(self,button):
        self.dialog.action_area.pack_start(button.GetWidget(),False,False,1)
    
    def AppendTab(self,title):
        tab=gtk.Frame()
        tab.show()
        self.dialog_tab[title]=tab
        self.dialog_tab_items_count[title]=0
        self.dialog_tabs.prepend_page(tab,gtk.Label(title))
        vbox=gtk.VBox(False)
        vbox.show()
        tab.add(vbox)
        table=gtk.Table(0,2)
        table.set_col_spacings(5)
        table.set_row_spacings(1)
        table.show()
        vbox.pack_start(table,False,False,0)
        
    
    def SetCurrentTab(self,idx):
        self.dialog_tabs.set_current_page(idx)
    
    def AppendItemToTab(self,tabname,item,itemname):
        table=self.dialog_tab[tabname].get_child().get_children()[0]
        rows=self.dialog_tab_items_count[tabname]
        self.dialog_tab_items_count[tabname]=rows+1
        if isinstance(item,CComboBox) or isinstance(item,CEditableComboBox) or isinstance(item,CEditBox) or isinstance(item,CEditBoxWithButton):
            table.resize(rows+1,2)
            lbl=gtk.Label(itemname)
            lbl.show()
            algn=gtk.Alignment(0,0.5)
            algn.set_padding(0,0,5,0)
            algn.show()
            algn.add(lbl)
            table.attach(algn,0,1,rows,rows+1,)
            table.attach((item.GetWidget()),1,2,rows,rows+1)
        elif isinstance(item,CTextArea):
            item.GetWidget().set_label(itemname)
            self.dialog_tab[tabname].get_child().pack_start(item.GetWidget(),True,True)
        elif isinstance(item,CTable):
            self.dialog_tab[tabname].get_child().pack_start(item.GetWidget(),True,True)
    
    def SetHandler(self,event,func,data):
        if event=='close':
            self.dialog.connect('delete-event',self.__DialogEventHandler,func,data)
    
    def __DialogEventHandler(self,dialog,event,func,data):
        func(*data)
        return True