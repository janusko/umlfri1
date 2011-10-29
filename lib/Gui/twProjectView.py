from lib.Depend.gtk2 import gobject
from lib.Depend.gtk2 import gtk

from lib.Commands.Project import CCreateElementObjectCommand, CCreateDiagramCommand
from common import CWidget
from lib.Project import CProject, CProjectNode
from lib.Elements import CElementObject
from lib.Drawing import CElement, CDiagram
from lib.Exceptions.UserException import *
from lib.Drawing.Canvas.GtkPlus import PixmapFromPath

from common import  event

class CtwProjectView(CWidget):
    name = 'twProjectView'
    widgets = ('twProjectView',
               
               'menuTreeElement',
               'mnuTreeAddDiagram', 'mnuTreeAddElement','mnuTreeDelete', 'mnuTreeFindInDiagrams',
               'mnuTreeSetAsDefault', 'mnuTreeUnSetDefault','mnuOpenSpecification'
              )
    
    __gsignals__ = {
        'selected_diagram':  (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT, gobject.TYPE_PYOBJECT)), 
        'selected-item-tree':  (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT, )),
        'create-diagram':   (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_STRING, )),
        'repaint':  (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ()),
        'close-diagram': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,)),
    }
    
    def __init__(self, app, wTree):
        CWidget.__init__(self, app, wTree)
        
        self.TreeStore = gtk.TreeStore(str, gtk.gdk.Pixbuf, str, object)
        self.EventButton = (0,0)
        
        self.Column = gtk.TreeViewColumn(_('Elements'))
        self.twProjectView.append_column(self.Column)
        self.twProjectView.set_reorderable(True)
        
        self.StrRenderer = gtk.CellRendererText()
        self.PbRenderer = gtk.CellRendererPixbuf()
        
        self.Column.pack_start(self.PbRenderer, False)
        self.Column.add_attribute(self.PbRenderer, 'pixbuf', 1)
        self.Column.pack_start(self.StrRenderer, True)
        self.Column.add_attribute(self.StrRenderer, 'text', 0)
            
        
        self.twProjectView.set_model(self.TreeStore)
        self.twProjectView.get_selection().set_mode(gtk.SELECTION_SINGLE)
        
        self.TARGETS = [
        ('MY_TREE_MODEL_ROW', gtk.TARGET_SAME_WIDGET, 0),
        ('text/plain', 0, 1),
        ('TEXT', 0, 2),
        ('STRING', 0, 3),
        ]
        
        self.twProjectView.enable_model_drag_source(gtk.gdk.BUTTON1_MASK, self.TARGETS, gtk.gdk.ACTION_DEFAULT | gtk.gdk.ACTION_MOVE | gtk.gdk.ACTION_COPY)
        self.twProjectView.enable_model_drag_dest(self.TARGETS, gtk.gdk.ACTION_DEFAULT)
    
    def ClearProjectView(self):
        self.TreeStore.clear()
    
    def Redraw(self, firstTime = False):
        """
        This function load ProjectTree Add menu from enabled diagrams and options of elements
        
        """
        for item in self.mnuTreeAddDiagram.get_children():
            self.mnuTreeAddDiagram.remove(item)
        
        for item in self.mnuTreeAddElement.get_children():
            self.mnuTreeAddElement.remove(item)
        
        for item in self.application.GetProject().GetMetamodel().GetElementFactory().IterTypes():
            if item.GetOptions().get('DirectAdd', False):
                newItem = gtk.ImageMenuItem(item.GetId())
                self.mnuTreeAddElement.append(newItem)
                newItem.connect("activate", self.on_mnuAddElement_activate, item.GetId())
                img = gtk.Image()
                img.set_from_pixbuf(PixmapFromPath(self.application.GetProject().GetMetamodel().GetStorage(), self.application.GetProject().GetMetamodel().GetElementFactory().GetElement(item.GetId()).GetIcon()))
                newItem.set_image(img)
                img.show()
                newItem.show()
        
        for diagram in self.application.GetProject().GetMetamodel().GetDiagrams():
            mi = gtk.ImageMenuItem(diagram)
            
            img = gtk.Image()
            img.set_from_pixbuf(PixmapFromPath(self.application.GetProject().GetMetamodel().GetStorage(), self.application.GetProject().GetMetamodel().GetDiagramFactory().GetDiagram(diagram).GetIcon()))
            img.show()
            
            mi.set_image(img)
            mi.show()   
            mi.connect("activate", self.on_mnuTreeAddDiagram_activate, diagram)
            self.mnuTreeAddDiagram.append(mi)
        
        project = self.application.GetProject()
        root = project.GetRoot()
        self.TreeStore.clear()
        parent = self.TreeStore.append(None)
        self.TreeStore.set(parent, 0, root.GetName(), 1, PixmapFromPath(self.application.GetProject().GetMetamodel().GetStorage(), root.GetObject().GetType().GetIcon()), 2, root.GetType(), 3, root)
        self.__DrawTree(root, parent)
        if firstTime:
            self.twProjectView.expand_to_path(self.TreeStore.get_path(parent))

    def __DrawTree(self, root, parent):
        
        for diagram in root.GetDiagrams():
            novy = self.TreeStore.append(parent)
            self.TreeStore.set(novy, 0, diagram.GetName() , 1, PixmapFromPath(self.application.GetProject().GetMetamodel().GetStorage(), diagram.GetType().GetIcon()), 2, '=Diagram=',3,diagram)
        
        for node in root.GetChilds():
            novy = self.TreeStore.append(parent)
            self.TreeStore.set(novy, 0, node.GetName() , 1, PixmapFromPath(self.application.GetProject().GetMetamodel().GetStorage(), node.GetObject().GetType().GetIcon()), 2, node.GetType(),3,node)
            self.__DrawTree(node, novy)
            
         
    def get_iter_from_node(self, node):
        if isinstance(node, CDiagram):
            parent = node.GetNode()
        elif isinstance(node, CProjectNode):
            parent = node.GetParent()
        else:
            node = node.GetNode()
            parent = node.GetParent()
        
        if parent is not None:
            parentIter = self.get_iter_from_node(parent)
            childIter = self.TreeStore.iter_children(parentIter)
            if parentIter is None:
                return None
        else:
            childIter = self.TreeStore.get_iter_root()
        
        while childIter is not None:
            childNode = self.TreeStore.get(childIter, 3)[0]
            if childNode is node:
                return childIter
            childIter = self.TreeStore.iter_next(childIter)
        
        return None
    
    def ShowElement(self,Element):
        object = Element.GetObject()
        iter = self.get_iter_from_node(object)
        self.twProjectView.expand_to_path(self.TreeStore.get_path(iter))
        self.twProjectView.get_selection().select_iter(iter)
        self.twProjectView.scroll_to_cell(self.TreeStore.get_path(iter))  
    
    def ShowDiagram(self, diagram):
        iter = self.get_iter_from_node(diagram)
        self.twProjectView.expand_to_path(self.TreeStore.get_path(iter))
        self.twProjectView.get_selection().select_iter(iter)
                    
    
    def AddElement(self, element, diagram, parentElement = None):
        if parentElement is None:
            parent = diagram.GetNode()
        elif isinstance(parentElement, CProjectNode):
            parent = parentElement
        else:
            parent = parentElement

        node = CProjectNode(parent, element)
        self.application.GetProject().AddNode(node, parent)
        novy = self.TreeStore.append(self.get_iter_from_node(parent))
        self.TreeStore.set(novy, 0, element.GetName() , 1, PixmapFromPath(self.application.GetProject().GetMetamodel().GetStorage(), element.GetType().GetIcon()), 2, element.GetType().GetId(),3,node)
        self.twProjectView.get_selection().select_iter(novy)
        self.emit('selected-item-tree',self.twProjectView.get_model().get(novy,3)[0])
        self.twProjectView.scroll_to_cell(self.TreeStore.get_path(novy))        
        
        
    def AddDiagram(self, diagram):
        iter = self.twProjectView.get_selection().get_selected()[1]
        if iter is None:
            iter = self.twProjectView.get_model().get_iter_root()
            self.twProjectView.get_selection().select_iter(iter)
        model = self.twProjectView.get_model()
        
        if model.get(iter,2)[0] == "=Diagram=":
            iter = model.iter_parent(iter)
        node = model.get(iter,3)[0]
        node.AddDiagram(diagram)
        novy = self.TreeStore.insert(iter,len(node.GetDiagrams())-1)
        self.TreeStore.set(novy, 0, diagram.GetName() , 1, PixmapFromPath(self.application.GetProject().GetMetamodel().GetStorage(), diagram.GetType().GetIcon()), 2, '=Diagram=',3,diagram)
        path = self.TreeStore.get_path(novy)
        self.twProjectView.expand_to_path(path)
        self.twProjectView.get_selection().select_iter(novy)
        self.emit('selected-item-tree',self.twProjectView.get_model().get(novy,3)[0])
        self.twProjectView.scroll_to_cell(self.TreeStore.get_path(novy))        
        
    
    def UpdateElement(self, object):
        if isinstance(object, CElementObject):
            iter = self.get_iter_from_node(object)
            node = object.GetNode()
            model = self.twProjectView.get_model()
            self.TreeStore.set_value(iter, 0, object.GetName())

        if isinstance(object, CDiagram):
            iter = self.get_iter_from_node(object)
            node = object.GetNode()
            
            model = self.twProjectView.get_model()
            self.TreeStore.set_value(iter, 0, object.GetName())
    
    
    @event("twProjectView","button-press-event")
    def button_clicked(self, widget, event):
        self.EventButton = (event.button, event.time) 
        
    @event("mnuOpenSpecification","activate")
    def on_mnuOpenSpecification_activate(self,widget):
        iter = self.twProjectView.get_selection().get_selected()[1]
        node=self.twProjectView.get_model().get(iter,3)[0]
        self.emit('selected-item-tree',node)
        
        props = self.application.GetWindow('frmProperties')
        props.SetParent(self.application.GetWindow('frmMain'))
        props.ShowPropertiesWindow(node.GetObject(), self.application)
    
    @event("twProjectView", "row-activated")
    def on_twProjectView_set_selected(self, treeView, path, column):
        model = self.twProjectView.get_model()
        iter =  model.get_iter(path)
        if model.get(iter,2)[0] == "=Diagram=":
            diagram = model.get(iter,3)[0]
            if diagram is None:
                raise ProjectError("Diagram is None.")
            else:
                self.emit('selected_diagram',diagram, None)
    
    @event("twProjectView", "cursor-changed")
    def on_twProjectView_change_selection(self, treeView):
        self.application.bus.emit('project-selection-changed', self.GetSelectedNode())
        
        iter = treeView.get_selection().get_selected()[1]
        if iter is None:
            return
        model = self.twProjectView.get_model()
        if model.get(iter,2)[0] == "=Diagram=":
            self.mnuTreeFindInDiagrams.set_sensitive(False)
            self.mnuTreeSetAsDefault.set_sensitive(True)
            self.mnuTreeUnSetDefault.set_sensitive(True)
            default = model.get(iter,3)[0] in self.application.GetProject().GetDefaultDiagrams()
            self.mnuTreeSetAsDefault.set_property("visible", not default)
            self.mnuTreeUnSetDefault.set_property("visible", default)
        else:
            self.mnuTreeFindInDiagrams.set_sensitive(True)
            self.mnuTreeSetAsDefault.set_sensitive(False)
            self.mnuTreeUnSetDefault.set_sensitive(False)
        if self.EventButton[0] == 3:
            self.mnuTreeDelete.set_sensitive(len(treeView.get_model().get_path(iter)) > 1)
            self.menuTreeElement.popup(None,None,None,self.EventButton[0],self.EventButton[1])
        
        self.emit('selected-item-tree',treeView.get_model().get(iter,3)[0])
    
    def on_mnuAddElement_activate(self, widget, element):
        node = self.GetSelectedNode()
        type = self.application.GetProject().GetMetamodel().GetElementFactory().GetElement(element)
        cmd = CCreateElementObjectCommand(type, node)
        self.application.GetCommands().Execute(cmd)
    
    def on_mnuTreeAddDiagram_activate(self, widget, diagramId):
        self.emit('create-diagram', diagramId)
    
    def RemoveFromArea(self,node):
        for i in node.GetDiagrams():
            self.emit('close-diagram',i)
            
        for j in node.GetChilds():
            self.RemoveFromArea(j)

        for d in self.application.GetProject().GetDiagrams():
            d.DeleteObject(node.GetObject())
    
    
    def DeleteElement(self, elementObject):
        rootIter = self.twProjectView.get_model().get_iter_root()
        
        if elementObject is self.twProjectView.get_model().get(rootIter,3)[0].GetObject():
            return
        
        iter = self.get_iter_from_node(elementObject)
        node = elementObject.GetNode()

        self.TreeStore.remove(iter)
        self.RemoveFromArea(node)
        self.application.GetProject().RemoveNode(node)
    
    @event("mnuTreeDelete","activate")
    def on_mnuTreeDelete_activate(self, menuItem):
        iter = self.twProjectView.get_selection().get_selected()[1]
        self.twProjectView.get_selection().select_iter(self.twProjectView.get_model().iter_parent(iter))
        self.emit('selected-item-tree',self.twProjectView.get_model().get(self.twProjectView.get_model().iter_parent(iter),3)[0])
        model = self.twProjectView.get_model()
        if model.get(iter,2)[0] != "=Diagram=":
            node = model.get(iter,3)[0]
            self.TreeStore.remove(iter)
            self.RemoveFromArea(node)
            self.application.GetProject().RemoveNode(node)
            self.emit('repaint')
        else:
            diagram = model.get(iter,3)[0]
            itr = model.iter_parent(iter)
            node = model.get(itr,3)[0]
            node.RemoveDiagram(diagram)
            self.TreeStore.remove(iter)
            self.emit('close-diagram',diagram)
        
    @event("mnuTreeFindInDiagrams","activate")
    def on_mnuTreeFindInDiagrams(self, menuItem):
        iter = self.twProjectView.get_selection().get_selected()[1]
        model = self.twProjectView.get_model()
        node = model.get(iter,3)[0]
        cnt = len(list(node.GetAppears()))
        if cnt == 0:
            pass
        elif cnt == 1:
            self.emit('selected_diagram',list(node.GetAppears())[0], node.GetObject())
        elif cnt > 1:
            diagram = self.application.GetWindow('frmFindInDiagram').ShowDialog(list(node.GetAppears()), object)
        
            if diagram is not None:
                self.emit('selected_diagram', diagram, node.GetObject())

    def GetSelectedDiagram(self):
        iter = self.twProjectView.get_selection().get_selected()[1]
        if iter == None:
            return None
        node = self.twProjectView.get_model().get(iter,3)[0]
        if isinstance(node,CDiagram):
            return node
        else:
            return None
        
    def GetSelectedElement(self):
        iter = self.twProjectView.get_selection().get_selected()[1]
        if iter == None:
            return None
        node = self.twProjectView.get_model().get(iter,3)[0]
        if isinstance(node,CProjectNode):
            return node
        else:
            return None
    
    def GetSelectedNode(self):
        iter = self.twProjectView.get_selection().get_selected()[1]
        if iter is None:
            return self.application.GetProject().GetRoot()
        node, = self.TreeStore.get(iter, 3)
        if isinstance(node, CDiagram):
            node = node.GetNode()
        return node
        
    def GetRootNode(self):
        iter = self.twProjectView.get_model().get_iter_root()
        self.twProjectView.get_selection().select_iter(iter)
        node = self.twProjectView.get_model().get(iter,3)[0]
        return node
        
    @event("twProjectView","drag-data-get")
    def on_drag_data_get(self, widget,drag_context, selection_data, info, time):
        treeselection = widget.get_selection()
        model, iter = treeselection.get_selected()
        data = model.get_value(iter, 0)
        selection_data.set(selection_data.target, 8, data)

        
    
    def CheckSanity(self, model, iter_to_copy, target_iter):
        path_of_iter_to_copy = model.get_path(iter_to_copy)
        path_of_target_iter = model.get_path(target_iter)
        if path_of_target_iter[0:len(path_of_iter_to_copy)] == path_of_iter_to_copy:
            return False
        elif len(path_of_target_iter) < 2:
            return False
        else:
            return True
    
    
    def IterCopy(self, treeview, model, iter_to_copy, target_iter, pos):
        new_pos_str=(model.get_string_from_iter(target_iter)).split(':')
        old_pos_str=(model.get_string_from_iter(iter_to_copy)).split(':')
        new_el_pos=int(new_pos_str[len(new_pos_str)-1])
        old_el_pos=int(old_pos_str[len(old_pos_str)-1])
        
        if treeview.get_model().get(iter_to_copy,2)[0] == "=Diagram=":
            node_to_copy = treeview.get_model().get(treeview.get_model().iter_parent(iter_to_copy),3)[0]
        else:
            node_to_copy = treeview.get_model().get(iter_to_copy,3)[0]
        if treeview.get_model().get(target_iter,2)[0] == "=Diagram=":
            target_node = treeview.get_model().get(treeview.get_model().iter_parent(target_iter),3)[0]
        else:
            target_node = treeview.get_model().get(target_iter,3)[0]
        
        if (pos == gtk.TREE_VIEW_DROP_INTO_OR_BEFORE) or (pos == gtk.TREE_VIEW_DROP_INTO_OR_AFTER):
            if treeview.get_model().get(target_iter,2)[0] == "=Diagram=":
                raise ProjectError("BadMove")#MoveElementToDiagram
            elif treeview.get_model().get(iter_to_copy,2)[0] == "=Diagram=":
                node_to_copy.MoveDiagramToNewNode(target_node,treeview.get_model().get(iter_to_copy,3)[0])
                new_iter = model.insert(target_iter,len(target_node.diagrams)-1)
            else:
                node_to_copy.MoveNode(target_node)
                new_iter = model.append(target_iter)
        
        elif pos == gtk.TREE_VIEW_DROP_BEFORE:
            if treeview.get_model().get(iter_to_copy,2)[0] == "=Diagram=":
                if treeview.get_model().get(target_iter,2)[0] != "=Diagram=":
                    if new_el_pos>len(target_node.GetParent().diagrams):
                        raise ProjectError("BadMove")#MoveDiagramBeforeElement
                    else:
                        if target_node.GetParent()==node_to_copy and old_el_pos<new_el_pos:
                            new_el_pos=new_el_pos-1
                        node_to_copy.MoveDiagramToNewNode(target_node.GetParent(),treeview.get_model().get(iter_to_copy,3)[0],new_el_pos)
                else:
                    if target_node==node_to_copy and old_el_pos<new_el_pos:
                        new_el_pos=new_el_pos-1
                    node_to_copy.MoveDiagramToNewNode(target_node,treeview.get_model().get(iter_to_copy,3)[0],new_el_pos)
            elif treeview.get_model().get(target_iter,2)[0] == "=Diagram=":
                raise ProjectError("BadMove")#MoveElementBeforeDiagram
            else:
                if target_node.GetParent()==node_to_copy.GetParent() and old_el_pos<new_el_pos:
                    new_el_pos=new_el_pos-1
                node_to_copy.MoveNode(target_node.GetParent(),new_el_pos-len(target_node.GetParent().diagrams))
            new_iter = model.insert_before(None, target_iter)
        
        elif pos == gtk.TREE_VIEW_DROP_AFTER:
            if treeview.get_model().get(iter_to_copy,2)[0] == "=Diagram=":
                if treeview.get_model().get(target_iter,2)[0] != "=Diagram=":
                    raise ProjectError("BadMove")#MoveDiagramAfterElement
                else:
                    if (target_node==node_to_copy and old_el_pos>new_el_pos) or (target_node!=node_to_copy):
                        new_el_pos=new_el_pos+1
                    node_to_copy.MoveDiagramToNewNode(target_node,treeview.get_model().get(iter_to_copy,3)[0],new_el_pos)
            elif treeview.get_model().get(target_iter,2)[0] == "=Diagram=":
                if new_el_pos+1<len(target_node.diagrams):
                    raise ProjectError("BadMove")#MoveElementAfterDiagram
                else:
                    if (target_node==node_to_copy.GetParent() and old_el_pos>new_el_pos) or (target_node!=node_to_copy.GetParent()):
                        new_el_pos=new_el_pos+1
                    node_to_copy.MoveNode(target_node,new_el_pos-len(target_node.diagrams))
            else:
                if (target_node.GetParent()==node_to_copy.GetParent() and old_el_pos>new_el_pos) or (target_node.GetParent()!=node_to_copy.GetParent()):
                    new_el_pos=new_el_pos+1
                node_to_copy.MoveNode(target_node.GetParent(),new_el_pos-len(target_node.GetParent().diagrams))
            new_iter = model.insert_after(None, target_iter)
                    
        for i in range(4):
            model.set_value(new_iter, i, model.get_value(iter_to_copy, i))
              
        if model.iter_has_child(iter_to_copy):
            for i in range(0, model.iter_n_children(iter_to_copy)):
                next_iter_to_copy = model.iter_nth_child(iter_to_copy, i)
                self.IterCopy(treeview, model, next_iter_to_copy, new_iter, gtk.TREE_VIEW_DROP_INTO_OR_BEFORE)
    
    @event("mnuTreeSetAsDefault", "activate", "set")
    @event("mnuTreeUnSetDefault", "activate", "unset")
    def on_set_as_default_activate(self, widget, action):
        iter = self.twProjectView.get_selection().get_selected()[1]
        model = self.twProjectView.get_model()
        if model.get(iter,2)[0] == "=Diagram=":
            diagram = model.get(iter,3)[0]
            if action == 'set':
                self.application.GetProject().AddDefaultDiagram(diagram)
            else:
                self.application.GetProject().DeleteDefaultDiagram(diagram)
    
    @event("twProjectView","drag_data_received")
    def on_drag_data_received(self, widget, context, x, y, selection, info, etime):
        if widget.get_dest_row_at_pos(x, y) is not None:
            path, pos = widget.get_dest_row_at_pos(x, y)
            model, iter_to_copy = widget.get_selection().get_selected()
            target_iter = model.get_iter(path)
                       
            if self.CheckSanity(model, iter_to_copy, target_iter):
                try:
                    self.IterCopy(widget, model, iter_to_copy, target_iter, pos)
                except ProjectError, e:
                    if e.GetName() == "BadMove":
                        context.finish(False, False, etime)
                        return
                context.finish(True, True, etime)
            else:
                context.finish(False, False, etime)
    
    @event("application.bus", "diagram-created")
    def on_diagram_created(self, bus, diagram):
        parent = diagram.GetNode()
        iter = self.get_iter_from_node(parent)
        newIter = self.TreeStore.insert(iter, len(parent.GetDiagrams())-1)
        self.TreeStore.set(newIter,
                           0, diagram.GetName(),
                           1, PixmapFromPath(self.application.GetProject().GetMetamodel().GetStorage(), diagram.GetType().GetIcon()),
                           2, '=Diagram=',
                           3, diagram)
    
    @event("application.bus", "diagram-removed")
    def on_diagram_removed(self, bus, diagram):
        iter = self.get_iter_from_node(diagram)
        self.TreeStore.remove(iter)
    
    @event("application.bus", "element-object-created")
    def on_element_created(self, widget, elements):
        for element in elements:
            node = element.GetNode()
            parent = node.GetParent()
            iter = self.get_iter_from_node(parent)
            newIter = self.TreeStore.append(iter)
            self.TreeStore.set(newIter,
                               0, element.GetName(),
                               1, PixmapFromPath(self.application.GetProject().GetMetamodel().GetStorage(), element.GetType().GetIcon()),
                               2, element.GetType().GetId(),
                               3, node)
    
    @event("application.bus", "element-object-removed")
    def on_element_removed(self, widget, elements):
        for element in elements:
            iter = self.get_iter_from_node(element)
            self.TreeStore.remove(iter)
    
    @event('application.bus', 'diagram-changed')
    @event('application.bus', 'element-changed')
    def ObjectChanged(self, bus, params):
        for obj, path in params:
            if path:
                if not isinstance(obj, CElementObject):
                    obj = obj.GetObject()
                iter = self.get_iter_from_node(obj)
                self.TreeStore.set(iter, 0, obj.GetName())
