from lib.Commands.Properties import CApplyPropertyPatchCommand
from lib.Domains import CDomainObject, CDomainObjectComparator
from lib.Exceptions import DomainTypeError
from lib.Drawing import CElement, CConnection, CDiagram
from frmPropertiesWidgets import *

class CfrmProperties(object):
    
    def __init__(self):
        self.parent=None
        self.element=None
        self.element_changed=False
        self.element_change_ignored=False
        self.attributes={}
        self.tables={}
        self.table_values={}
        self.dialog_sizes={}
        self.domain_object=None
        self.old_domain_object=None
        self.apply_button=None
    
    def SetParent(self,parent):
        self.parent=parent.form
    
    def __ClearFormular(self,type):
        for id in type.IterAttributeIDs():
            if type.GetAttribute(id)['hidden']:
                continue
            if type.GetAttribute(id)['type']=='str' or type.GetAttribute(id)['type']=='int' or type.GetAttribute(id)['type']=='float':
                if isinstance(self.attributes[type.GetName()][id],CEditableComboBox):
                    self.attributes[type.GetName()][id].SetActiveItemText(str(type.GetDefaultValue(id)))
                elif isinstance(self.attributes[type.GetName()][id],CEditBox):
                    self.attributes[type.GetName()][id].SetText(str(type.GetDefaultValue(id)))
                self.attributes[type.GetName()][id].SetBackgroundColor('#FFFFFF')
            if type.GetAttribute(id)['type']=='bool' or type.GetAttribute(id)['type']=='enum':
                self.attributes[type.GetName()][id].SetActiveItemText(str(type.GetDefaultValue(id)))
            if type.GetAttribute(id)['type']=='text':
                self.attributes[type.GetName()][id].SetText(str(type.GetDefaultValue(id)))
                self.attributes[type.GetName()][id].SetBackgroundColor('#FFFFFF')
            if type.GetAttribute(id)['type']=='list':
                if self.attributes[type.GetName()].has_key(id):
                    self.attributes[type.GetName()][id].SetText('')
        self.tables[type.GetName()]['ref'].UnselectAll()
        self.tables[type.GetName()]['ref'].SetLastSelect(None)
    
    def __ToString(self,object):
        for joiner in object.GetType().IterJoiners():
            return joiner.CreateString(object)
        return 'not specified yet'
    
    def __ObjectsToString(self,objects):
        val=[]
        for obj in objects:
            val.append(self.__ToString(obj))
        return ';'.join(val)
        
    def __CreateTable(self,type,dialog):
        btnNew=CButton('_New', 'gtk-new')
        btnNew.SetHandler('clicked',self.__onTableNewButtonClick,(type,dialog))
        
        btnSave=CButton('_Save', 'gtk-save')
        btnSave.SetSensitive(False)
        btnSave.SetHandler('clicked',self.__onTableSaveButtonClick,(type,dialog))
        
        btnDelete=CButton('_Delete', 'gtk-delete')
        btnDelete.SetSensitive(False)
        btnDelete.SetHandler('clicked',self.__onTableDeleteButtonClick,(type,dialog))

        btnUp = CButton('Up', 'gtk-go-up', 'Move selected item up.')
        btnUp.SetSensitive(False)
        btnUp.SetHandler('clicked', self.__onTableUpButtonClick, (type, dialog))

        btnDown = CButton('Down', 'gtk-go-down', 'Move selected item down.')
        btnDown.SetSensitive(False)
        btnDown.SetHandler('clicked', self.__onTableDownButtonClick, (type, dialog))
        
        model=[]
        for key in type.IterAttributeIDs():
            if type.GetAttribute(key)['hidden']:
                continue
            model.append(type.GetAttribute(key)['name'])
        table=CTable(model,btnDelete,btnSave,btnNew, btnUp, btnDown)
        
        self.tables[type.GetName()]={}
        self.tables[type.GetName()]['ref']=table
        self.tables[type.GetName()]['new']=btnNew
        self.tables[type.GetName()]['save']=btnSave
        self.tables[type.GetName()]['delete']=btnDelete
        self.tables[type.GetName()]['up']  = btnUp
        self.tables[type.GetName()]['down'] = btnDown
        
        table.SetHandler('row-selected',self.__onTableRowSelect,(type,dialog))
        if len(type.GetName().split('.'))==2 or len(type.GetName().split('.'))%2==1:
            self.__FillTable(type)
        else:
            for key in self.table_values.keys():
                if key.find(type.GetName())!=-1:
                    self.table_values.pop(key)
        return table
    
    def __FillTable(self,type):
        table=self.tables[type.GetName()]['ref']
        table.Clear()
        atts=None
        if len(type.GetName().split('.'))<3:
            atts=self.domain_object.GetValue(type.GetName()[type.GetName().rfind('.')+1:])
        elif self.table_values.has_key(type.GetName()):
            atts = self.table_values[type.GetName()]
        if atts is not None and len(atts)>0:
            for att in atts:
                tmp=[]
                for key in type.IterAttributeIDs():
                    if type.GetAttribute(key)['hidden']:
                        continue
                    if type.GetAttribute(key)['type']=='list':
                        tmp.append(self.__ObjectsToString(att.GetValue(key)))
                    else:
                        tmp.append(str(att.GetValue(key)))
                table.AppendRow(tmp,att)
    
    def __onTableNewButtonClick(self,type,dialog):
        dialog.GrabFirst()
        if self.tables[type.GetName()]['save'].GetSensitive():
            question=CResponseDialog('Question',dialog)
            question.AppendResponse('continue','C_ontinue')
            question.AppendResponse('cancel','_Cancel',True)
            question.SetQuestion('There are unsaved changes and if you continue they will be\n lost. '\
                                          'What do you wish to do?')
            question.Show()
            response=question.Close()
            if response=='cancel':
                return
        self.__ClearFormular(type)
        self.tables[type.GetName()]['save'].SetSensitive(False)
        self.tables[type.GetName()]['delete'].SetSensitive(False)
        self.tables[type.GetName()]['up'].SetSensitive(False)
        self.tables[type.GetName()]['down'].SetSensitive(False)
        for key in self.table_values.keys():
            if key.find(type.GetName())!=-1 and len(key)!=len(type.GetName()):
                self.table_values.pop(key)
        if len(type.GetName().split('.'))>2 and len(type.GetName().split('.'))%2==1:
            for id in type.IterAttributeIDs():
                if type.GetAttribute(id)['hidden']:
                    continue
                if type.GetAttribute(id)['type']=='list':
                    self.tables[type.GetName()+'.'+id]['ref'].Clear()
    
    def __onTableSaveButtonClick(self,type,dialog):
        if self.__CheckValues(type):
            table=self.tables[type.GetName()]['ref']
            dialog.GrabFirst()
            if table.GetSelectedRowIndex()!=-1:
                domainobject=table.GetRowObject(table.GetSelectedRowIndex())
                idx=0
                for id in type.IterAttributeIDs():
                    if type.GetAttribute(id)['hidden']:
                        continue
                    if type.GetAttribute(id)['type'] in ('str', 'int', 'float'):
                        if isinstance(self.attributes[type.GetName()][id],CEditableComboBox):
                            val=self.attributes[type.GetName()][id].GetActiveItemText()
                        elif isinstance(self.attributes[type.GetName()][id],CEditBox):
                            val=self.attributes[type.GetName()][id].GetText()
                    elif type.GetAttribute(id)['type'] in ('bool', 'enum'):
                        val=self.attributes[type.GetName()][id].GetActiveItemText()
                    elif type.GetAttribute(id)['type']=='text':
                        val=self.attributes[type.GetName()][id].GetText()
                    elif type.GetAttribute(id)['type']=='list':
                        if self.table_values.has_key(type.GetName()+'.'+id):
                            domainobject.SetValue(id,[])
                            for object in self.table_values[type.GetName()+'.'+id]:
                                domainobject.AppendItem(id,object)
                            self.table_values[type.GetName()+'.'+id]=[]
                        val=self.__ObjectsToString(domainobject.GetValue(id))
                        table.SetCellValue(table.GetSelectedRowIndex(),idx,val)
                        idx+=1
                        continue
                    domainobject.SetValue(id,val)
                    table.SetCellValue(table.GetSelectedRowIndex(),idx,val)
                    idx+=1
                val=self.__ObjectsToString(table.GetAllRowObjects())
                id=type.GetName()[type.GetName().rfind('.')+1:]
                if self.attributes.has_key(type.GetName()[:type.GetName().rfind('.')]) and self.attributes[type.GetName()[:type.GetName().rfind('.')]].has_key(id):
                    self.attributes[type.GetName()[:type.GetName().rfind('.')]][id].SetText(val)
                if len(type.GetName().split('.'))<3:
                    self.element_changed=True
                    self.apply_button.SetSensitive(True)
            else:
                if len(type.GetName().split('.'))<3:
                    item=self.domain_object.AppendItem(type.GetName()[type.GetName().find('.')+1:])
                    self.element_changed=True
                    self.apply_button.SetSensitive(True)
                else:
                    item=CDomainObject(type)
                    self.table_values.setdefault(type.GetName(),[]).append(item)
                tmp=[]
                for id in type.IterAttributeIDs():
                    if type.GetAttribute(id)['hidden']:
                        continue
                    if type.GetAttribute(id)['type'] in ('str', 'int', 'float'):
                        if isinstance(self.attributes[type.GetName()][id],CEditableComboBox):
                            val=self.attributes[type.GetName()][id].GetActiveItemText()
                        elif isinstance(self.attributes[type.GetName()][id],CEditBox):
                            val=self.attributes[type.GetName()][id].GetText()
                        tmp.append(val)
                        item.SetValue(id,val)
                    elif type.GetAttribute(id)['type'] in ('bool', 'enum'):
                        val=self.attributes[type.GetName()][id].GetActiveItemText()
                        tmp.append(val)
                        item.SetValue(id,val)
                    elif type.GetAttribute(id)['type']=='text':
                        val=self.attributes[type.GetName()][id].GetText()
                        tmp.append(val)
                        item.SetValue(id,val)
                    elif type.GetAttribute(id)['type']=='list':
                        if self.table_values.has_key(type.GetName()+'.'+id):
                            for object in self.table_values[type.GetName()+'.'+id]:
                                item.AppendItem(id,object)
                            self.table_values[type.GetName()+'.'+id]=[]
                        tmp.append(self.__ObjectsToString(item.GetValue(id)))
                table.AppendRow(tmp,item)
                val=self.__ObjectsToString(table.GetAllRowObjects())
                id=type.GetName()[type.GetName().rfind('.')+1:]
                if self.attributes.has_key(type.GetName()[:type.GetName().rfind('.')]) and self.attributes[type.GetName()[:type.GetName().rfind('.')]].has_key(id):
                    self.attributes[type.GetName()[:type.GetName().rfind('.')]][id].SetText(val)
            self.__ClearFormular(type)
            self.tables[type.GetName()]['save'].SetSensitive(False)
            self.tables[type.GetName()]['delete'].SetSensitive(False)
            self.tables[type.GetName()]['up'].SetSensitive(False)
            self.tables[type.GetName()]['down'].SetSensitive(False)
        else:
            warning=CResponseDialog('Warning',dialog)
            warning.AppendResponse('ok','Ok')
            warning.SetWarning('Entered values are wrong and can not be saved.')
            warning.Show()
            warning.Close()
    
    def __onTableDeleteButtonClick(self,type,dialog):
        table=self.tables[type.GetName()]['ref']
        dialog.GrabFirst()
        if table.GetSelectedRowIndex()!=-1:
            idx=table.GetSelectedRowIndex()
            table.RemoveRow(idx)
            path=type.GetName()[type.GetName().rfind('.')+1:]+'['+str(idx)+']'
            if len(type.GetName().split('.'))<3:
                self.domain_object.RemoveItem(path)
                self.element_changed=True
                self.apply_button.SetSensitive(True)
            elif self.table_values.has_key(type.GetName()):
                self.table_values[type.GetName()].pop(idx)
            for key in self.table_values.keys():
                if key.find(type.GetName())!=-1 and len(key)!=len(type.GetName()):
                    self.table_values.pop(key)
            val=self.__ObjectsToString(table.GetAllRowObjects())
            id=type.GetName()[type.GetName().rfind('.')+1:]
            if self.attributes.has_key(type.GetName()[:type.GetName().rfind('.')]) and self.attributes[type.GetName()[:type.GetName().rfind('.')]].has_key(id):
                self.attributes[type.GetName()[:type.GetName().rfind('.')]][id].SetText(val)
            self.__ClearFormular(type)
            self.tables[type.GetName()]['save'].SetSensitive(False)
            self.tables[type.GetName()]['delete'].SetSensitive(False)
            self.tables[type.GetName()]['up'].SetSensitive(False)
            self.tables[type.GetName()]['down'].SetSensitive(False)

    def __onTableUpButtonClick(self, type, dialog):
        table = self.tables[type.GetName()]['ref']
        idxs = table.MoveItemUp()
        if idxs:
            item=self.domain_object.SwapItems(type.GetName()[type.GetName().find('.')+1:], idxs)
            self.element_changed=True
            self.apply_button.SetSensitive(True)
            self.apply_button.SetSensitive(True)

    def __onTableDownButtonClick(self, type, dialog):
        table = self.tables[type.GetName()]['ref']
        idxs = table.MoveItemDown()
        if idxs:
            item=self.domain_object.SwapItems(type.GetName()[type.GetName().find('.')+1:], idxs)
            self.element_changed=True
            self.apply_button.SetSensitive(True)
            self.apply_button.SetSensitive(True)

    def __onTableRowSelect(self,type,dialog):
        change=True
        table=self.tables[type.GetName()]['ref']
        if self.tables[type.GetName()]['save'].GetSensitive():
            if table.GetLastSelect()!=str(table.GetSelectedRowIndex()):
                question=CResponseDialog('Question',dialog)
                question.AppendResponse('continue','C_ontinue')
                question.AppendResponse('cancel','_Cancel',True)
                question.SetQuestion('There are unsaved changes and if you continue they will be\n lost. '\
                                              'What do you wish to do?')
                question.Show()
                response=question.Close()
                if response=='cancel':
                    dialog.GrabFirst()
                    table.SelectLast()
                    change=False
            else:
                table.SelectLast()
                change=False
        if change:
            table.SetLastSelect(str(table.GetSelectedRowIndex()))
            dialog.GrabTable()
            item=table.GetRowObject(table.GetSelectedRowIndex())
            for id in type.IterAttributeIDs():
                if type.GetAttribute(id)['hidden']:
                    continue
                val=str(item.GetValue(id))
                if type.GetAttribute(id)['type']=='str' or type.GetAttribute(id)['type']=='int' or type.GetAttribute(id)['type']=='float':
                    if isinstance(self.attributes[type.GetName()][id],CEditableComboBox):
                        self.attributes[type.GetName()][id].SetActiveItemText(val)
                    elif isinstance(self.attributes[type.GetName()][id],CEditBox):
                        val=self.attributes[type.GetName()][id].SetText(val)
                if type.GetAttribute(id)['type']=='bool' or type.GetAttribute(id)['type']=='enum':
                    self.attributes[type.GetName()][id].SetActiveItemText(val)
                if type.GetAttribute(id)['type']=='text':
                    self.attributes[type.GetName()][id].SetText(val)
                if type.GetAttribute(id)['type']=='list':
                    self.table_values.setdefault(type.GetName()+'.'+id,[])
                    self.table_values[type.GetName()+'.'+id]=[]
                    for obj in item.GetValue(id):
                        self.table_values[type.GetName()+'.'+id].append(obj.GetCopy())
                    if len(type.GetName().split('.'))%2==1:
                        self.__FillTable(type.GetFactory().GetDomain(type.GetAttribute(id)['list']['type']))
                    elif len(type.GetName().split('.'))%2==0 or len(type.GetName().split('.'))==2:
                        objects=item.GetValue(id)
                        self.attributes[type.GetName()][id].SetText(self.__ObjectsToString(objects))
            self.tables[type.GetName()]['delete'].SetSensitive(True)
            self.tables[type.GetName()]['save'].SetSensitive(False)
            self.tables[type.GetName()]['up'].SetSensitive(True)
            self.tables[type.GetName()]['down'].SetSensitive(True)
    
    def ShowPropertiesWindow(self,element,app):
        if isinstance(element,(CElement,CConnection,CDiagram)):
            self.element=element.GetObject()
        else:
            self.element=element
        self.application=app
        self.old_domain_object=None
        self.domain_object=self.element.GetDomainObject().GetCopy()
        type=self.element.GetDomainObject().GetType()
        self.attributes={}
        self.tables={}
        dlg=self.__CreateBoneWindow(type,'Properties',self.parent,True)
        dlg.Show()
        self.element_changed=False
    
    def ShowPropertiesWindowForDomainObject(self,domainobject,title):
        self.old_domain_object=domainobject
        self.domain_object=domainobject.GetCopy()
        type=domainobject.GetType()
        self.attributes={}
        self.tables={}
        dlg=self.__CreateBoneWindow(type,title,self.parent,True)
        dlg.Show()
        self.element_changed=False
    
    def __CreateBoneWindow(self,type,name,parent,main_dialog=False):
        dialog=CDialog(parent,name)
        if self.dialog_sizes.has_key(type.GetName()):
            x,y=self.dialog_sizes[type.GetName()]
            dialog.SetSize(x,y)
        dialog.SetHandler('close',self.__onMainDialogCloseButtonClick,(dialog,type,main_dialog))
        
        btnClose=CButton('_Close')
        dialog.AppendButton(btnClose)
        btnClose.SetHandler('clicked',self.__onMainDialogCloseButtonClick,(dialog,type,main_dialog))
        
        if main_dialog:
            btnOk=CButton('_Ok')
            dialog.AppendButton(btnOk)
            btnOk.SetHandler('clicked',self.__onMainDialogOkButtonClick,(dialog,type))
            
            btnApply=CButton('_Apply')
            dialog.AppendButton(btnApply)
            btnApply.SetHandler('clicked',self.__onMainDialogApplyButtonClick,(btnApply,dialog,type))
            self.apply_button=btnApply
        
        attributes_order={}
        for id in type.IterAttributeIDs():
            att=type.GetAttribute(id)
            if att['hidden']:
                continue
            if att['type']!='list':
                attributes_order.setdefault('General',[]).append(id)
            else:
                attributes_order.setdefault(att['name'],[]).append(id)
        for key in attributes_order:
            self.__ProcessDomainType(type,key,attributes_order[key],dialog,main_dialog)
        dialog.SetCurrentTab(0)
        
        return dialog
    
    def __onCloseDialogCheckButtonToggle(self,button):
        self.element_change_ignored=button.IsChecked()
    
    def __CreateStr(self,type,att,key):
        if att.has_key('enum'):
            entry=CEditableComboBox()
            for val in att['enum']:
                entry.AppendItem(val)
            entry.SetActiveItemText(type.GetDefaultValue(key))
        else:
            entry=CEditBox()
            entry.SetText(type.GetDefaultValue(key))
        self.attributes.setdefault(type.GetName(),{})
        self.attributes[type.GetName()][key]=entry
        if len(type.GetName().split('.'))==1:
            entry.SetHandler('changed',self.__onMainFormularEntryChange,(type,key))
        else:
            entry.SetHandler('changed',self.__onTableFormularEntryChange,(type,key))
        return entry
    
    def __CreateInt(self,type,att,key):
        if att.has_key('enum'):
            entry=CEditableComboBox('int')
            for val in att['enum']:
                entry.AppendItem(str(val))
            entry.SetActiveItemText(str(type.GetDefaultValue(key)))
        else:
            entry=CEditBox(style='int')
            entry.SetText(str(type.GetDefaultValue(key)))
        self.attributes.setdefault(type.GetName(),{})
        self.attributes[type.GetName()][key]=entry
        if len(type.GetName().split('.'))==1:
            entry.SetHandler('changed',self.__onMainFormularEntryChange,(type,key))
        else:
            entry.SetHandler('changed',self.__onTableFormularEntryChange,(type,key))
        return entry
    
    def __CreateFloat(self,type,att,key):
        if att.has_key('enum'):
            entry=CEditableComboBox('float')
            for val in att['enum']:
                entry.AppendItem(str(val))
            entry.SetActiveItemText(str(type.GetDefaultValue(key)))
        else:
            entry=CEditBox(style='float')
            entry.SetText(str(type.GetDefaultValue(key)))
        self.attributes.setdefault(type.GetName(),{})
        self.attributes[type.GetName()][key]=entry
        if len(type.GetName().split('.'))==1:
            entry.SetHandler('changed',self.__onMainFormularEntryChange,(type,key))
        else:
            entry.SetHandler('changed',self.__onTableFormularEntryChange,(type,key))
        return entry
    
    def __CreateEnum(self,type,att,key):
        combobox=CComboBox()
        for val in att['enum']:
            combobox.AppendItem(val)
        combobox.SetActiveItemText(str(type.GetDefaultValue(key)))
        self.attributes.setdefault(type.GetName(),{})
        self.attributes[type.GetName()][key]=combobox
        if len(type.GetName().split('.'))==1:
            combobox.SetHandler('changed',self.__onMainFormularEntryChange,(type,key))
        else:
            combobox.SetHandler('changed',self.__onTableFormularEntryChange,(type,key))
        return combobox
    
    def __CreateBool(self,type,att,key):
        combobox=CComboBox()
        combobox.AppendItem('False')
        combobox.AppendItem('True')
        combobox.SetActiveItemText(str(type.GetDefaultValue(key)))
        self.attributes.setdefault(type.GetName(),{})
        self.attributes[type.GetName()][key]=combobox
        if len(type.GetName().split('.'))==1:
            combobox.SetHandler('changed',self.__onMainFormularEntryChange,(type,key))
        else:
            combobox.SetHandler('changed',self.__onTableFormularEntryChange,(type,key))
        return combobox
        
    def __CreateText(self,type,att,key):
        text=CTextArea()
        text.SetText(str(type.GetDefaultValue(key)))
        self.attributes.setdefault(type.GetName(),{})
        self.attributes[type.GetName()][key]=text
        if len(type.GetName().split('.'))==1:
            text.SetHandler('changed',self.__onMainFormularEntryChange,(type,key))
        else:
            text.SetHandler('changed',self.__onTableFormularEntryChange,(type,key))
        return text
    
    def __CreateEditBoxWithButton(self,type,att,key,dialog):
        list=CEditBoxWithButton('Edit...')
        self.attributes.setdefault(type.GetName(),{})
        self.attributes[type.GetName()][key]=list
        list.SetHandler('clicked',self.__onShowChildDialogButtonClick,(type.GetFactory().GetDomain(att['list']['type']),dialog))
        list.SetHandler('changed',self.__onTableFormularEntryChange,(type,key))
        return list
    
    def __onMainFormularEntryChange(self,type,key):
        att=type.GetAttribute(key)
        if att['type']=='int' or att['type']=='float' or\
           att['type']=='text' or att['type']=='str':
            min=att['min'] if att.has_key('min') else None
            max=att['max'] if att.has_key('max') else None
            try:
                entry=self.attributes[type.GetName()][key]
                if isinstance(entry,(CEditBox,CTextArea)):
                    val=type.TransformValue(entry.GetText(),key)
                elif isinstance(entry,CEditableComboBox):
                    val=type.TransformValue(entry.GetActiveItemText(),key)
                type.CheckValue(val,key)
                entry.SetBackgroundColor('#FFFFFF')
                self.element_changed=True
                self.apply_button.SetSensitive(True)
            except ValueError:
                entry.SetBackgroundColor('#FFFF66')
            except DomainTypeError:
                entry.SetBackgroundColor('#FFFF66')
        else:
            self.element_changed=True
            self.apply_button.SetSensitive(True)
    
    def __onTableFormularEntryChange(self,type,key):
        att=type.GetAttribute(key)
        if att['type']=='int' or att['type']=='float' or\
           att['type']=='text' or att['type']=='str':
            min=att['min'] if att.has_key('min') else None
            max=att['max'] if att.has_key('max') else None
            try:
                entry=self.attributes[type.GetName()][key]
                if isinstance(entry,(CEditBox,CTextArea)):
                    val=type.TransformValue(entry.GetText(),key)
                elif isinstance(entry,CEditableComboBox):
                    val=type.TransformValue(entry.GetActiveItemText(),key)
                type.CheckValue(val,key)
                entry.SetBackgroundColor('#FFFFFF')
                self.tables[type.GetName()]['save'].SetSensitive(True)
            except ValueError:
                entry.SetBackgroundColor('#FFFF66')
            except DomainTypeError:
                entry.SetBackgroundColor('#FFFF66')
        else:
            self.tables[type.GetName()]['save'].SetSensitive(True)
    
    #tato metoda pridava na dialog jednotlive vlastnosti podla ich typu
    def __ProcessDomainType(self,type,tabname,atts_order,dialog,main_dialog=False):

        dialog.AppendTab(tabname)
        is_list=False
        for key in atts_order:
            att=type.GetAttribute(key)
            if att['hidden']:
                continue

            attribute_name = key

            def append_item(item):
                dialog.AppendItemToTab(tabname, attribute_name, item, att['name'])

            def append_item_using_factory(item_factory):
                append_item(item_factory(type, att, key))

            if att['type']=='str':
                append_item_using_factory(self.__CreateStr)
            elif att['type']=='enum':
                append_item_using_factory(self.__CreateEnum)
            elif att['type']=='bool':
                append_item_using_factory(self.__CreateBool)
            elif att['type']=='text':
                append_item_using_factory(self.__CreateText)
            elif att['type']=='list':
                is_list=True
                type=type.GetFactory().GetDomain(att['list']['type'])
                for key in type.IterAttributeIDs():
                    att=type.GetAttribute(key)
                    if att['hidden']:
                        continue

                    list_item_attribute_name = attribute_name + '.' + key

                    def append_item(item):
                        dialog.AppendItemToTab(tabname, list_item_attribute_name, item, att['name'])

                    def append_item_using_factory(item_factory):
                        append_item(item_factory(type, att, key))

                    if att['type']=='str':
                        append_item_using_factory(self.__CreateStr)
                    elif att['type']=='enum':
                        append_item_using_factory(self.__CreateEnum)
                    elif att['type']=='bool':
                        append_item_using_factory(self.__CreateBool)
                    elif att['type']=='text':
                        append_item_using_factory(self.__CreateText)
                    elif att['type']=='list':
                        append_item(self.__CreateEditBoxWithButton(type,att,key,dialog))
                    elif att['type']=='int':
                        append_item_using_factory(self.__CreateInt)
                    elif att['type']=='float':
                        append_item_using_factory(self.__CreateFloat)
            elif att['type']=='int':
                append_item_using_factory(self.__CreateInt)
            elif att['type']=='float':
                append_item_using_factory(self.__CreateFloat)
        if not main_dialog or is_list:
            dialog.AppendItemToTab(tabname,'table',self.__CreateTable(type,dialog),att['name'])
        else:
            for id in type.IterAttributeIDs():
                if type.GetAttribute(id)['hidden']:
                    continue
                val=str(self.domain_object.GetValue(id))
                if type.GetAttribute(id)['type']=='str':
                    if isinstance(self.attributes[type.GetName()][id],CEditableComboBox):
                        self.attributes[type.GetName()][id].SetActiveItemText(val)
                    else:
                        self.attributes[type.GetName()][id].SetText(val)
                if type.GetAttribute(id)['type']=='int':
                    if isinstance(self.attributes[type.GetName()][id],CEditableComboBox):
                        self.attributes[type.GetName()][id].SetActiveItemText(val)
                    else:
                        self.attributes[type.GetName()][id].SetText(val)
                if type.GetAttribute(id)['type']=='float':
                    if isinstance(self.attributes[type.GetName()][id],CEditableComboBox):
                        self.attributes[type.GetName()][id].SetActiveItemText(val)
                    else:
                        self.attributes[type.GetName()][id].SetText(val)
                if type.GetAttribute(id)['type']=='bool' or type.GetAttribute(id)['type']=='enum':
                    self.attributes[type.GetName()][id].SetActiveItemText(val)
                if type.GetAttribute(id)['type']=='text':
                    self.attributes[type.GetName()][id].SetText(val)
            self.apply_button.SetSensitive(False)
    
    #metoda vytvori novy poddialog dialogu
    def __onShowChildDialogButtonClick(self,type,parent):
        dname=type.GetName().split('.')
        dname=dname[len(dname)-1]
        dlg=self.__CreateBoneWindow(type,parent.GetTitle()+' - '+dname,parent.GetWidget())
        dlg.Show()
    
    #zatvorenie dialogu cez Close button
    def __onMainDialogCloseButtonClick(self,dialog,type,main_dialog):
        self.dialog_sizes[type.GetName()]=dialog.GetSize()
        if self.element_changed and not self.element_change_ignored and main_dialog and self.__CheckValues(type):
            val=self.__CloseFunction(dialog)
            if val=='close':
                self.element_changed = False
                dialog.Close()
            elif val=='save':
                self.element_changed = False
                self.__SaveFunction(type)
                dialog.Close()
        else:
            dialog.Close()
    
    #stlacenie apply button dialogu
    def __onMainDialogApplyButtonClick(self,button,dialog,type):
        if self.__CheckValues(type):
            self.__SaveFunction(type)
            self.element_changed=False
            button.SetSensitive(False)
        else:
            warning=CResponseDialog('Warning',dialog)
            warning.AppendResponse('ok','Ok')
            warning.SetWarning('Entered values are wrong and can not be saved.')
            warning.Show()
            warning.Close()
    
    #stlacenie save button dialogu
    def __onMainDialogOkButtonClick(self,dialog,type):
        if self.__CheckValues(type):
            self.dialog_sizes[type.GetName()]=dialog.GetSize()
            self.__SaveFunction(type)
            self.element_changed=False
            dialog.Close()
        else:
            warning=CResponseDialog('Warning',dialog)
            warning.AppendResponse('ok','Ok')
            warning.SetWarning('Entered values are wrong and can not be saved.')
            warning.Show()
            warning.Close()
    
    def __CheckValues(self,type):
        try:
            for id in type.IterAttributeIDs():
                if type.GetAttribute(id)['hidden']:
                    continue
                if type.GetAttribute(id)['type'] in ('str', 'int', 'float'):
                    if isinstance(self.attributes[type.GetName()][id],CEditableComboBox):
                        val=self.attributes[type.GetName()][id].GetActiveItemText()
                    elif isinstance(self.attributes[type.GetName()][id],CEditBox):
                        val=self.attributes[type.GetName()][id].GetText()
                    type.CheckValue(val,id)
                elif type.GetAttribute(id)['type']=='text':
                    val=self.attributes[type.GetName()][id].GetText()
                    type.CheckValue(val,id)
            return True
        except DomainTypeError:
            return False
    
    def __CloseFunction(self,parent):
        close_dialog=CResponseDialog('Question',parent)
        close_dialog.AppendResponse('close','_Close')
        close_dialog.AppendResponse('cancel','C_ancel')
        close_dialog.AppendResponse('save','_Save & close',True)
        close_dialog.SetQuestion('There are unsaved changes.What do you want to do?')
        button=CCheckButton('Do not show this dialog again.')
        button.SetHandler('toggled',self.__onCloseDialogCheckButtonToggle,tuple([button]))
        close_dialog.SetToggleButton(button)
        close_dialog.Show()
        ret_val=close_dialog.Close()
        if ret_val is None or ret_val=='cancel':
           return 'cancel'
        elif ret_val=='close':
           return 'close'
        if ret_val=='save':
           return 'save'
    
    def __SaveFunction(self,type):
        for id in type.IterAttributeIDs():
            if type.GetAttribute(id)['hidden']:
                continue
            if type.GetAttribute(id)['type'] in ('str', 'int', 'float'):
                if isinstance(self.attributes[type.GetName()][id],CEditableComboBox):
                    val=self.attributes[type.GetName()][id].GetActiveItemText()
                elif isinstance(self.attributes[type.GetName()][id],CEditBox):
                    val=self.attributes[type.GetName()][id].GetText()
            elif type.GetAttribute(id)['type'] in ('bool', 'enum'):
                val=self.attributes[type.GetName()][id].GetActiveItemText()
            elif type.GetAttribute(id)['type']=='text':
                val=self.attributes[type.GetName()][id].GetText()
            elif type.GetAttribute(id)['type']=='list':
                continue
            self.domain_object.SetValue(id,val)
        if self.old_domain_object is not None:
            self.old_domain_object.SetValues(self.domain_object)
        #self.domain_object=self.old_domain_object.GetCopy()
        if self.element is not None:
            diff = CDomainObjectComparator(self.element.GetDomainObject(), self.domain_object)
            l = list(diff)
            cmd = CApplyPropertyPatchCommand(self.element, list(diff))
            self.application.GetCommands().Execute(cmd)
