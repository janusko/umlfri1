from lib.Depend.gtk2 import gobject
from lib.Depend.gtk2 import gtk

from lib.Commands.Project import CCreateElementObjectCommand, CCreateDiagramCommand, CMoveNodeCommand, CMoveDiagramCommand
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
            
         
    def get_iter_from_node(self, node, parent = None):
        if parent is None:
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
        node = self.GetSelectedNode()
        type = self.application.GetProject().GetMetamodel().GetDiagramFactory().GetDiagram(diagramId)
        cmd = CCreateDiagramCommand(type, node)
        self.application.GetCommands().Execute(cmd)
    
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
    
    # Adopted from the discussion at http://www.daa.com.au/pipermail/pygtk/2003-November/006304.html
    def IterCopy(self, model, iter_to_copy, target_iter, pos):
        source_row = model[iter_to_copy]
        if pos == gtk.TREE_VIEW_DROP_INTO_OR_BEFORE or pos == gtk.TREE_VIEW_DROP_INTO_OR_AFTER:
            new_iter = model.append(parent=target_iter, row=source_row)
        elif pos == gtk.TREE_VIEW_DROP_BEFORE:
            new_iter = model.insert_before(parent=None, sibling=target_iter, row=source_row)
        elif pos == gtk.TREE_VIEW_DROP_AFTER:
            new_iter = model.insert_after(parent=None, sibling=target_iter, row=source_row)
        else:
            return

        for i in range(model.iter_n_children(iter_to_copy)):
            next_iter_to_copy = model.iter_nth_child(iter_to_copy, i)
            self.IterCopy(model, next_iter_to_copy, new_iter, gtk.TREE_VIEW_DROP_INTO_OR_BEFORE)
    
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
            model, source_iter = widget.get_selection().get_selected()
            target_iter = model.get_iter(path)
            
            node, = self.TreeStore.get(source_iter, 3)
            target, = self.TreeStore.get(target_iter, 3)
            if isinstance(node, CProjectNode):
                if isinstance(target, CDiagram):
                    newParent = target.GetNode()
                    newPosition = 0
                elif pos in (gtk.TREE_VIEW_DROP_INTO_OR_BEFORE, gtk.TREE_VIEW_DROP_INTO_OR_AFTER):
                    newParent = target
                    newPosition = newParent.GetChildrenCount()
                else:
                    newParent = target.GetParent()
                    if newParent is None:
                        newPosition = 0
                    else:
                        newPosition = newParent.GetChildIndex(target)
                    
                    if pos == gtk.TREE_VIEW_DROP_AFTER:
                        newPosition += 1
                
                if node.GetParent() is newParent:
                    oldPosition = newParent.GetChildIndex(node)
                    if oldPosition < newPosition:
                        # position fix if both project nodes have same parents and old position is lower
                        newPosition -= 1
                
                cmd = CMoveNodeCommand(node, newParent, newPosition)
                self.application.GetCommands().Execute(cmd)
            elif isinstance(node, CDiagram):
                if isinstance(target, CProjectNode):
                    if pos in (gtk.TREE_VIEW_DROP_INTO_OR_BEFORE, gtk.TREE_VIEW_DROP_INTO_OR_AFTER):
                        newParent = target
                        newPosition = newParent.GetChildrenCount()
                    else:
                        newParent = target.GetParent()
                        newPosition = newParent.GetDiagramCount()
                else:
                    newParent = target.GetNode()
                    newPosition = newParent.GetDiagramIndex(target)
                    
                    if pos == gtk.TREE_VIEW_DROP_AFTER:
                        newPosition += 1
                
                if node.GetNode() is newParent:
                    oldPosition = newParent.GetDiagramIndex(node)
                    if oldPosition < newPosition:
                        # position fix if both diagrams have same parents and old position is lower
                        newPosition -= 1
                
                cmd = CMoveDiagramCommand(node, newParent, newPosition)
                self.application.GetCommands().Execute(cmd)
    
    @event("application.bus", "diagram-created")
    def on_diagram_created(self, bus, diagrams):
        for diagram in diagrams:
            parent = diagram.GetNode()
            iter = self.get_iter_from_node(parent)
            newIter = self.TreeStore.insert(iter, len(parent.GetDiagrams())-1)
            self.TreeStore.set(newIter,
                               0, diagram.GetName(),
                               1, PixmapFromPath(self.application.GetProject().GetMetamodel().GetStorage(), diagram.GetType().GetIcon()),
                               2, '=Diagram=',
                               3, diagram)
    
    @event("application.bus", "diagram-removed")
    def on_diagram_removed(self, bus, diagrams):
        for diagram in diagrams:
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
    
    @event('application.bus', 'node-moved-in-tree')
    def ObjectMoved(self, bus, params):
        for node, oldParent in params:
            newParent = node.GetParent()
            newPosition = newParent.GetChildIndex(node)
            
            iterNode = self.get_iter_from_node(node, oldParent)
            iterParent = self.get_iter_from_node(newParent)
            
            if not self.TreeStore.iter_has_child(iterParent):
                self.IterCopy(self.TreeStore, iterNode, iterParent, gtk.TREE_VIEW_DROP_INTO_OR_AFTER)
            elif newPosition > 0:
                iterAfter = self.get_iter_from_node(newParent.GetChild(newPosition - 1))
                self.IterCopy(self.TreeStore, iterNode, iterAfter, gtk.TREE_VIEW_DROP_AFTER)
            else:
                iterBefore = self.TreeStore.iter_children(iterParent)
                while iterBefore is not None and isinstance(self.TreeStore.get(iterBefore, 3)[0], CDiagram):
                    iterBefore = self.TreeStore.iter_next(iterBefore)
                if iterBefore is None:
                    self.IterCopy(self.TreeStore, iterNode, iterParent, gtk.TREE_VIEW_DROP_INTO_OR_AFTER)
                else:
                    self.IterCopy(self.TreeStore, iterNode, iterBefore, gtk.TREE_VIEW_DROP_BEFORE)
            
            self.TreeStore.remove(iterNode)
    
    @event('application.bus', 'diagram-moved-in-tree')
    def DiagramMoved(self, bus, params):
        for diagram, oldParent in params:
            newParent = diagram.GetNode()
            newPosition = newParent.GetDiagramIndex(diagram)
            
            iterDiagram = self.get_iter_from_node(diagram, oldParent)
            iterParent = self.get_iter_from_node(newParent)
            
            diagramRow = self.TreeStore[iterDiagram]
            
            if not self.TreeStore.iter_has_child(iterParent):
                self.TreeStore.append(parent=iterParent, row = diagramRow)
            elif newPosition > 0:
                iterAfter = self.get_iter_from_node(newParent.GetDiagram(newPosition - 1))
                self.TreeStore.insert_after(parent = None, sibling = iterAfter, row = diagramRow)
            else:
                iterBefore = self.TreeStore.iter_children(iterParent)
                self.TreeStore.insert_before(parent = None, sibling = iterBefore, row = diagramRow)
            
            self.TreeStore.remove(iterDiagram)
    
    @event('application.bus', 'project-expand-node')
    def ExpandNode(self, bus, params):
        for node in params:
            iterNode = self.get_iter_from_node(node)
            iterPath = self.TreeStore.get_path(iterNode)
            
            
            self.twProjectView.expand_to_path(iterPath)
