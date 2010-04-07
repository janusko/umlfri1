from lib.Depend.gtk2 import gtk
from lib.Depend.gtk2 import gobject
from lib.Exceptions.UserException import ProjectError
from lib.Drawing import CElement, CConnection
from lib.Domains.Object import CDomainObject
import pygtk

class CfrmProperties():
    
    def __init__(self):
        self.parent=None
        self.element_changed=False
        self.element_change_ignored=False
        self.attributes={}
        self.tables={}
        self.dialog_sizes={}
        self.domain_object=None
        self.old_domain_object=None
    
    def SetParent(self,parent):
        self.parent=parent.form
    
    def TableNew_handler(self,widget,type):
        self.__ClearFormular(type)
    
    def __ClearFormular(self,type):
        for id in type.IterAttributeIDs():
            if type.GetAttribute(id)['type']=='str':
                self.attributes[type.GetName()][id].set_text('')
            if type.GetAttribute(id)['type']=='bool' or type.GetAttribute(id)['type']=='enum':
                model=self.attributes[type.GetName()][id].get_model()
                iter=model.get_iter('0')
                tmp=[]
                while iter!=None:
                    tmp.append(model.get_value(iter,0))
                    iter=model.iter_next(iter)
                if type.GetAttribute(id).has_key('default'):
                    self.attributes[type.GetName()][id].set_active(tmp.index(type.GetAttribute(id)['default']))
                else:
                    self.attributes[type.GetName()][id].set_active(0)
            if type.GetAttribute(id)['type']=='text':
                buffer=self.attributes[type.GetName()][id].get_buffer()
                buffer.delete(buffer.get_iter_at_offset(0),buffer.get_iter_at_offset(buffer.get_char_count()))
        treeview=self.tables[type.GetName()]
        treeview.get_selection().unselect_all()
    
    def TableSave_handler(self,widget,type):
        treeview=self.tables[type.GetName()]
        liststore,iter=treeview.get_selection().get_selected()
        if iter!=None:
            path=liststore.get_value(iter,0)+'['+str(liststore.get_path(iter)[0])+']'
            idx=1
            for id in type.IterAttributeIDs():
                if type.GetAttribute(id)['type']=='str':
                    val=self.attributes[type.GetName()][id].get_text()
                elif type.GetAttribute(id)['type']=='bool' or type.GetAttribute(id)['type']=='enum':
                    val=self.attributes[type.GetName()][id].get_active_text()
                elif type.GetAttribute(id)['type']=='text':
                    buffer=self.attributes[type.GetName()][id].get_buffer()
                    val=buffer.get_text(buffer.get_iter_at_offset(0),buffer.get_iter_at_offset(buffer.get_char_count()),True)
                elif type.GetAttribute(id)['type']=='list':
                    val=[]
                self.domain_object.SetValue(path+'.'+id,val)
                liststore.set_value(iter,idx,val)
                idx+=1
        else:
            if len(type.GetName().split('.'))<3:
                path=type.GetName()[type.GetName().find('.')+1:]
                self.domain_object.AppendItem(path)
                path=path+'['+str(len(self.domain_object.GetValue(path))-1)+']'
                tmp=[type.GetName()[type.GetName().find('.')+1:]]
                for id in type.IterAttributeIDs():
                    if type.GetAttribute(id)['type']=='str':
                        val=self.attributes[type.GetName()][id].get_text()
                    elif type.GetAttribute(id)['type']=='bool' or type.GetAttribute(id)['type']=='enum':
                        val=self.attributes[type.GetName()][id].get_active_text()
                    elif type.GetAttribute(id)['type']=='text':
                        buffer=self.attributes[type.GetName()][id].get_buffer()
                        val=buffer.get_text(buffer.get_iter_at_offset(0),buffer.get_iter_at_offset(buffer.get_char_count()),True)
                    elif type.GetAttribute(id)['type']=='list':
                        val=[]
                    tmp.append(val)
                    self.domain_object.SetValue(path+'.'+id,val)
                liststore.append(tmp)
            else:
                
                pass
        self.__ClearFormular(type)
    
    def RowSelected_handler(self,treeview,type):
        selection=treeview.get_selection()
        model,iter=selection.get_selected()
        path=model.get_value(iter,0)+'['+str(model.get_path(iter)[0])+']'
        for id in type.IterAttributeIDs():
            val=str(self.domain_object.GetValue(path+'.'+id))
            if type.GetAttribute(id)['type']=='str':
                self.attributes[type.GetName()][id].set_text(val)
            if type.GetAttribute(id)['type']=='bool' or type.GetAttribute(id)['type']=='enum':
                model=self.attributes[type.GetName()][id].get_model()
                iter=model.get_iter('0')
                tmp=[]
                while iter!=None:
                    tmp.append(model.get_value(iter,0))
                    iter=model.iter_next(iter)
                self.attributes[type.GetName()][id].set_active(tmp.index(val))
            if type.GetAttribute(id)['type']=='text':
                self.attributes[type.GetName()][id].get_buffer().set_text(val)
    
    def __CreateTable(self,vbox,type):
        types=[]
        cols=[]
        idx=1
        types.append(gobject.TYPE_STRING)
        for key in type.IterAttributeIDs():
            types.append(gobject.TYPE_STRING)
            cell=gtk.CellRendererText()
            col=gtk.TreeViewColumn(type.GetAttribute(key)['name'])
            col.pack_start(cell)
            col.set_resizable(True)
            col.set_expand(True)
            col.set_attributes(cell, text=idx)
            idx+=1
            cols.append(col)
        liststore=gtk.ListStore(*types)
        treeview=gtk.TreeView(liststore)
        treeview.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_HORIZONTAL)
        for i in range(type.GetAttributesCount()):
            treeview.append_column(cols[i])
        
        self.tables.setdefault(type.GetName(),treeview)
        
        vb=gtk.VBox()
        hbox_btns=gtk.HBox()
        hbox_tv=gtk.HBox()
        vb.pack_start(hbox_btns,False,False)
        
        btnNew=gtk.Button('New')
        btnNew.set_size_request(82,26)
        hbox_btns.pack_end(btnNew,False,False,1)
        btnNew.connect('clicked',self.TableNew_handler,type)
        
        btnSave=gtk.Button('Save')
        btnSave.set_size_request(82,26)
        hbox_btns.pack_end(btnSave,False,False,1)
        btnSave.connect('clicked',self.TableSave_handler,type)
        
        btnDelete=gtk.Button('Delete')
        btnDelete.set_size_request(82,26)
        hbox_btns.pack_end(btnDelete,False,False,1)
        
        vb.pack_start(hbox_tv,True,True,1)
        hbox_tv.pack_start(treeview,True,True,1)
        vbox.pack_end(vb)
        
        treeview.connect('cursor-changed',self.RowSelected_handler,type)
        
        if len(type.GetName().split('.'))<3:
            for att in self.domain_object.GetValue(type.GetName()[type.GetName().rfind('.')+1:]):
                tmp=[type.GetName()[type.GetName().find('.')+1:]]
                for key in type.IterAttributeIDs():
                    tmp.append(str(att.GetValue(key)))
                liststore.append(tmp)
        else:
            selection=self.tables[type.GetName()[:type.GetName().rfind('.')]].get_selection()
            model,iter=selection.get_selected()
            if iter!=None:
                path=model.get_value(iter,0)+'['+str(model.get_path(iter)[0])+']'+type.GetName()[type.GetName().rfind('.'):]
                for att in self.domain_object.GetValue(path):
                    tmp=[path]
                    for key in type.IterAttributeIDs():
                        tmp.append(str(att.GetValue(key)))
                    liststore.append(tmp)
    
    def ShowPropertiesWindow(self,element,picda):
        self.old_domain_object=element.GetObject().GetDomainObject()
        self.domain_object=element.GetObject().GetDomainObject().GetCopy()
        type=element.GetObject().GetDomainObject().GetType()
        self.attributes={}
        self.tables={}
        dlg=self.__CreateBoneWindow(self.parent,type,'Properties',True)
        dlg.show_all()
    
    def __CreateBoneWindow(self,parent,type,name='Unnamed',main_dialog=False):
        dialog=gtk.Dialog(self.__GetName(name),parent,gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT | gtk.WINDOW_TOPLEVEL)
        if self.dialog_sizes.has_key(type.GetName()):
            x,y=self.dialog_sizes[type.GetName()]
            dialog.resize(x,y)
        dialog.set_icon(parent.get_icon())
        dialog.set_position(gtk.WIN_POS_MOUSE)
        dialog.connect('delete-event',self.Dialog_delete_event_handler,type)
        
        btnClose=gtk.Button(self.__GetName('_Close'))
        btnClose.set_size_request(82,26)
        dialog.action_area.pack_start(btnClose,False,False,1)
        btnClose.connect('clicked',self.Close_handler,dialog,type)
        
        if main_dialog:
            btnSave=gtk.Button(self.__GetName('_Ok'))
            btnSave.set_size_request(82,26)
            dialog.action_area.pack_end(btnSave,False,False,1)
            btnSave.grab_focus()
            btnSave.connect('clicked',self.Save_handler,dialog,type)
            
            btnApply=gtk.Button(self.__GetName('_Apply'))
            btnApply.set_size_request(82,26)
            dialog.action_area.pack_end(btnApply,False,False,1)
            btnApply.set_sensitive(False)
            btnApply.connect('clicked',self.Apply_handler,dialog,type)
        
        ntb=gtk.Notebook()
        dialog.vbox.pack_start(ntb,True,True)
        attributes_order={}
        for id in type.IterAttributeIDs():
            att=type.GetAttribute(id)
            if att['type']!='list':
                attributes_order.setdefault('General',[]).append(id)
            else:
                attributes_order.setdefault(att['name'],[]).append(id)
        for key in attributes_order:
            frm=gtk.Frame()
            ntb.prepend_page(frm,gtk.Label(key))
            self.__ProcessDomainType(type,frm,attributes_order[key],dialog,main_dialog)
        ntb.set_current_page(0)
        
        return dialog
    
    def __GetName(self,name):
        return name
    
    def __CloseDialog(self):
        dialog=gtk.Dialog(self.__GetName('Question'),self.parent,gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT | gtk.DIALOG_NO_SEPARATOR)
        dialog.set_icon(self.parent.get_icon())
        dialog.set_position(gtk.WIN_POS_MOUSE)
        dialog.add_buttons(self.__GetName('_Close'),0,self.__GetName('_Cancel'),1,self.__GetName('_Save & close'),2)
        hbox=gtk.HBox()
        dialog.vbox.pack_start(hbox,False,False)
        hbox.set_size_request(150,80)
        hbox.show()
        img=gtk.Image()
        img.set_from_stock(gtk.STOCK_DIALOG_QUESTION,gtk.ICON_SIZE_DIALOG)
        img.show()
        hbox.pack_start(img,False,False,10)
        dialog.vbox.pack_end(hbox,False,False)
        lbl=gtk.Label('Close without saving?')
        lbl.show()
        hbox.pack_start(lbl,False,False,5)
        hbox.show()
        hbox=gtk.HBox()
        dialog.vbox.pack_end(hbox,False,False)
        hbox.show()
        check=gtk.CheckButton(self.__GetName('Do not show this dialog again.'))
        check.connect('toggled',self.CloseDialog_toggled_handler)
        check.show()
        hbox.pack_start(check,False,False,10)
        dialog.set_resizable(False)
        return dialog
    
    def CloseDialog_toggled_handler(self,widget):
        self.element_change_ignored=widget.get_active()
    
    def __CreateStr(self,vbox,type,att,key):
        lbl=gtk.Label((att['name'])+':')
        algn=gtk.Alignment(0,0.5)
        algn.add(lbl)
        algn.set_size_request(70,10)
        entry=gtk.Entry()
        entry.set_name(att['name'])
        hbox=gtk.HBox()
        hbox.pack_start(algn,False,False,5)
        hbox.pack_start(entry,True,True,1)
        vbox.pack_start(hbox,False,False,1)
        self.attributes.setdefault(type.GetName(),{})
        self.attributes[type.GetName()].setdefault(key,entry)
    
    def __CreateEnum(self,vbox,type,att,key):
        lbl=gtk.Label((att['name'])+':')
        algn=gtk.Alignment(0,0.5)
        algn.add(lbl)
        algn.set_size_request(70,10)
        combobox=gtk.combo_box_new_text()
        for val in att['enum']:
            combobox.append_text(val)
            if att.has_key('default') and val==att['default']:
                combobox.set_active(att['enum'].index(val))
        if not att.has_key('default'):
            combobox.set_active(0)
        combobox.set_name(att['name'])
        frm=gtk.Frame()
        frm.add(combobox)
        frm.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        hbox=gtk.HBox()
        hbox.pack_start(algn,False,False,5)
        hbox.pack_start(frm,True,True,1)
        vbox.pack_start(hbox,False,False,1)
        self.attributes.setdefault(type.GetName(),{})
        self.attributes[type.GetName()].setdefault(key,combobox)    
    
    def __CreateBool(self,vbox,type,att,key):
        lbl=gtk.Label((att['name'])+':')
        algn=gtk.Alignment(0,0.5)
        algn.add(lbl)
        algn.show()
        algn.set_size_request(70,10)
        combobox=gtk.combo_box_new_text()
        combobox.append_text('False')
        combobox.append_text('True')
        if att.has_key('default'):
            if att['default']=='True':
                combobox.set_active(1)
            else:
                combobox.set_active(0)
        else:
            combobox.set_active(0)
        combobox.set_name(att['name'])
        frm=gtk.Frame()
        frm.add(combobox)
        frm.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        hbox=gtk.HBox()
        hbox.pack_start(algn,False,False,5)
        hbox.pack_start(frm,True,True,1)
        vbox.pack_start(hbox,False,False,1)
        self.attributes.setdefault(type.GetName(),{})
        self.attributes[type.GetName()].setdefault(key,combobox)
        
    def __CreateText(self,vbox,type,att,key):
        text=gtk.TextView()
        text.set_name(att['name'])
        text.set_editable(True)
        swindow=gtk.ScrolledWindow()
        swindow.add(text)
        swindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        frm=gtk.Frame()
        frm.add(swindow)
        frm.set_label(att['name']+':')
        frm.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        vb=gtk.VBox()
        vb.pack_start(frm,True,True)
        vbox.pack_start(vb,True,True)
        self.attributes.setdefault(type.GetName(),{})
        self.attributes[type.GetName()].setdefault(key,text)
    
    #tato metoda pridava na dialog jednotlive vlastnosti podla ich typu
    def __ProcessDomainType(self,type,frame,atts_order,dialog,main_dialog=False):
        is_list=False
        vbox=gtk.VBox(False)
        vbox.get_colormap().alloc_color(20, 20, 20)
        frame.add(vbox)
        for key in atts_order:
            att=type.GetAttribute(key)
            if att['type']=='str':
                self.__CreateStr(vbox,type,att,key)
            elif att['type']=='enum':
                self.__CreateEnum(vbox,type,att,key)
            elif att['type']=='bool':
                self.__CreateBool(vbox,type,att,key)
            elif att['type']=='text':
                self.__CreateText(vbox,type,att,key)
            elif att['type']=='list':
                is_list=True
                type=type.GetFactory().GetDomain(att['list']['type'])
                for key in type.IterAttributeIDs():
                    att=type.GetAttribute(key)
                    if att['type']=='str':
                        self.__CreateStr(vbox,type,att,key)
                    if att['type']=='enum':
                        self.__CreateEnum(vbox,type,att,key)
                    if att['type']=='bool':
                        self.__CreateBool(vbox,type,att,key)
                    if att['type']=='text':
                        self.__CreateText(vbox,type,att,key)
                    elif att['type']=='list':
                        btn=gtk.Button(att['name']+'...')
                        btn.show()
                        vbox.pack_start(btn,False,False)
                        btn.connect('clicked',self.ChildDialog_handler,type.GetFactory().GetDomain(att['list']['type']),dialog)
            elif att['type']=='int':
                lbl=gtk.Label((att['name']))
                lbl.show()
                vbox.pack_start(lbl,False,False)
                self.attributes.setdefault(type.GetName(),{})
                self.attributes[type.GetName()].setdefault(key,'reference...')
            elif att['type']=='float':
                lbl=gtk.Label((att['name']))
                vbox.pack_start(lbl,False,False)
                self.attributes.setdefault(type.GetName(),{})
                self.attributes[type.GetName()].setdefault(key,'reference...')
        if not main_dialog or is_list:
            self.__CreateTable(vbox,type)
        else:
            for id in type.IterAttributeIDs():
                val=str(self.domain_object.GetValue(id))
                if type.GetAttribute(id)['type']=='str':
                    self.attributes[type.GetName()][id].set_text(val)
                if type.GetAttribute(id)['type']=='bool' or type.GetAttribute(id)['type']=='enum':
                    model=self.attributes[type.GetName()][id].get_model()
                    iter=model.get_iter('0')
                    tmp=[]
                    while iter!=None:
                        tmp.append(model.get_value(iter,0))
                        iter=model.iter_next(iter)
                    self.attributes[type.GetName()][id].set_active(tmp.index(val))
                if type.GetAttribute(id)['type']=='text':
                    self.attributes[type.GetName()][id].get_buffer().set_text(val)
    
    #metoda vytvori novy poddialog dialogu
    def ChildDialog_handler(self,widget,type,dialog):
        dname=type.GetName().split('.')
        dname=dname[len(dname)-1]
        dlg=self.__CreateBoneWindow(dialog,type,'Properties - '+dname)
        dlg.show_all()
    
    #handlery dialogoveho okna
    
    #yatvorenie dialogu cez X
    def Dialog_delete_event_handler(self,widget,event,type):
        self.dialog_sizes[type.GetName()]=widget.get_size()
        if self.element_changed and not self.element_change_ignored:
            val=self.__CloseFunction()
            if val=='close' or val==gtk.RESPONSE_DELETE_EVENT:
                self.element_changed = False
                return False
            elif val=='save':
                self.element_changed = False
                self.__SaveFunction(type)
                return False
            else:
                return True
    
    #zatvorenie dialogu cez Close button
    def Close_handler(self,widget,dialog,type):
        self.dialog_sizes[type.GetName()]=dialog.get_size()
        if self.element_changed and not self.element_change_ignored:
            val=self.__CloseFunction()
            if val=='close':
                self.element_changed = False
                dialog.destroy()
            elif val=='save':
                self.element_changed = False
                self.__SaveFunction(type)
                dialog.destroy()
        else:
            dialog.destroy()
    
    #stlacenie apply button dialogu
    def Apply_handler(self,widget,dialog,type):
        self.__SaveFunction(type)
        self.element_changed=False
    
    #stlacenie save button dialogu
    def Save_handler(self,widget,dialog,type):
        self.dialog_sizes[type.GetName()]=dialog.get_size()
        self.__SaveFunction(type)
        self.element_changed=False
        dialog.destroy()
    
    def __CloseFunction(self,):
        close_dialog=self.__CloseDialog()
        close_dialog.action_area.get_children()[0].grab_focus()
        ret_val=close_dialog.run()
        close_dialog.destroy()
        if ret_val==0:
           return 'close'
        elif ret_val==1:
           return 'cancel'
        if ret_val==2:
           return 'save'
    
    def __SaveFunction(self,type):
        for id in type.IterAttributeIDs():
            if type.GetAttribute(id)['type']=='str':
                val=self.attributes[type.GetName()][id].get_text()
            elif type.GetAttribute(id)['type']=='bool' or type.GetAttribute(id)['type']=='enum':
                val=self.attributes[type.GetName()][id].get_active_text()
            elif type.GetAttribute(id)['type']=='text':
                buffer=self.attributes[type.GetName()][id].get_buffer()
                val=buffer.get_text(buffer.get_iter_at_offset(0),buffer.get_iter_at_offset(buffer.get_char_count()),True)
            elif type.GetAttribute(id)['type']=='list':
                continue
            self.domain_object.SetValue(id,val)
        self.old_domain_object.SetValues(self.domain_object)
        
    