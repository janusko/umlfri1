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
        self.dialog_tabs=gtk.Notebook()
        self.dialog_tabs.connect('focus',self.__Focus_handler)
        self.dialog.vbox.pack_start(self.dialog_tabs,True,True)
        self.dialog_tabs.show()
        self.dialog_tab={}
        self.dialog_tab_items_count={}
        self.dialog.connect('key-press-event',self.__CtrlTab_handler)
    
    def SetWidget(self,dialog):
        self.dialog=dialog
    
    def GetWidget(self):
        return self.dialog
    
    def SetTitle(self,title):
        self.dialog.set_title(title)
    
    def GetTitle(self):
        return self.dialog.get_title()
    
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
        self.dialog_tab[title]=tab
        self.dialog_tab_items_count[title]=0
        self.dialog_tabs.prepend_page(tab,gtk.Label(title))
        vbox=gtk.VBox(False)
        tab.add(vbox)
        table=gtk.Table(0,2)
        table.set_col_spacings(5)
        table.set_row_spacings(1)
        vbox.pack_start(table,False,False,0)
        vpaned = gtk.VPaned()
        vbox.pack_start(vpaned)
        tab.show_all()
        
    
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
            vpaned = self.dialog_tab[tabname].get_child().get_children()[1]
            if len(vpaned.get_children()) < 1:
                vpaned.add1(item.GetWidget())
            elif  len(vpaned.get_children()) < 2:
                vpaned.add2(item.GetWidget())
            else:
                self.dialog_tab[tabname].get_child().pack_start(item.GetWidget(),True,True)
            item.GetWidget().set_label(itemname)
        elif isinstance(item,CTable):
            vpaned = self.dialog_tab[tabname].get_child().get_children()[1]
            if len(vpaned.get_children()) < 1:
                vpaned.add1(item.GetWidget())
            elif  len(vpaned.get_children()) < 2:
                vpaned.add2(item.GetWidget())
            else:
                self.dialog_tab[tabname].get_child().pack_start(item.GetWidget(),True,True)
    
    def SetHandler(self,event,func,data):
        if event=='close':
            self.dialog.connect('delete-event',self.__DialogEventHandler,func,data)
    
    def __DialogEventHandler(self,dialog,event,func,data):
        func(*data)
        return True
    
    def __CtrlTab_handler(self,widget,event):
        if event.get_state()==gtk.gdk.CONTROL_MASK and event.keyval==65289:
            ntb=self.dialog.vbox.get_children()[0]
            if ntb.get_current_page()==(len(ntb.get_children())-1):
                ntb.set_current_page(0)
            else:
                ntb.next_page()
        elif event.get_state()==gtk.gdk.CONTROL_MASK and event.keyval==116:
            ntb=self.dialog.vbox.get_children()[0]
            items=ntb.get_children()[ntb.get_current_page()].get_child().get_children()
            if isinstance(items[len(items)-1].get_child(),gtk.VBox):
                treeview=items[len(items)-1].get_child().get_children()[1].get_child()
                if treeview.get_model().get_iter_first()!=None:
                    treeview.set_cursor('0')
                    treeview.grab_focus()
                else:
                    treeview.grab_focus()
        elif event.keyval==65289:
            if isinstance(widget,gtk.Notebook):
                return False
            else:
                ntb=self.dialog.vbox.get_children()[0]
                items=ntb.get_children()[ntb.get_current_page()].get_child().get_children()
                entries=[]
                table=[]
                for item in items:
                    if isinstance(item,gtk.Table):
                        chlds=item.get_children()
                        chlds.reverse()
                        for it in chlds:
                            if not isinstance(it,gtk.Alignment):
                                entries.append(it)
                    elif isinstance(item,gtk.Frame):
                        if isinstance(item.get_child(),gtk.ScrolledWindow):
                            entries.append(item.get_child().get_child())
                if widget.get_focus().get_parent() in entries:
                    widget=widget.get_focus().get_parent()
                else:
                    widget=widget.get_focus()
                if widget in entries:
                    if len(entries)-1==entries.index(widget):
                        if not isinstance(entries[0],gtk.HBox):
                            entries[0].grab_focus()
                        else:
                            entries[0].get_children()[1].grab_focus()
                    else:
                        if not isinstance(entries[entries.index(widget)+1],gtk.HBox):
                            entries[entries.index(widget)+1].grab_focus()
                        else:
                            entries[entries.index(widget)+1].get_children()[1].grab_focus()
                else:
                    return False
            return True
    
    def GrabFirst(self):
        ntb=self.dialog.vbox.get_children()[0]
        items=ntb.get_children()[ntb.get_current_page()].get_child().get_children()
        entries=[]
        table=[]
        for item in items:
            if isinstance(item,gtk.Table):
                chlds=item.get_children()
                chlds.reverse()
                for it in chlds:
                    if not isinstance(it,gtk.Alignment):
                        entries.append(it)
            elif isinstance(item,gtk.Frame):
                if isinstance(item.get_child(),gtk.ScrolledWindow):
                    entries.append(item.get_child().get_child())
        if isinstance(entries[0],gtk.HBox):
            entries[0].get_children()[1].grab_focus()
        elif isinstance(entries[0],gtk.ScrolledWindow):
            entries[0].get_child().grab_focus()
        else:
            entries[0].grab_focus()
    
    def GrabTable(self):
        ntb=self.dialog.vbox.get_children()[0]
        items=ntb.get_children()[ntb.get_current_page()].get_child().get_children()
        treeview=items[len(items)-1].get_child().get_children()[1].get_child()
        treeview.grab_focus()
    
    def __Focus_handler(self,ntb,num):
        chlds=ntb.get_children()[ntb.get_current_page()].get_child().get_children()[0].get_children()
        chlds[len(chlds)-2].grab_focus()
        return True
