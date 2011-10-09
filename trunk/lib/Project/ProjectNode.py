from lib.Exceptions.UserException import *
import weakref
from lib.Base import CBaseObject

class CProjectNode(CBaseObject):
    
    def __init__(self, parent = None, object = None):
        self.SetParent(parent)
        self.childs = []
        self.diagrams = []
        self.object = object
        self.object.Assign(self)

    def GetAppears(self):
        return self.GetObject().GetAppears()

    def AddAppears(self, diagram):
        self.GetObject().AddAppears(diagram)

    def GetDiagrams(self):
        return self.diagrams

    def HasDiagram(self):
        return len(self.diagrams) > 0

    def GetObject(self):
        return self.object

    def GetName(self):
        return self.object.GetName()

    def GetType(self):
        return self.object.GetType().GetId()

    def AddChild(self, child, pos = None):
        if child not in self.childs:
            if pos==None or pos<0 or pos>len(self.childs):
                self.childs.append(child)
            else:
                self.childs.insert(pos,child)
            child.SetParent(self)
            self.object.AddRevision()
        else:
            raise ProjectError("ExistsChild")


    def AddDiagram(self, diagram):
        if diagram not in self.diagrams:
            self.diagrams.append(diagram)
            diagram.Assign(self)
    
    def MoveDiagramToNewNode(self, newNode, diagram, pos = None):
        self.RemoveDiagram(diagram)
        if pos==None or pos<0 or pos>len(newNode.diagrams):
            newNode.diagrams.append(diagram)
        else:
            newNode.diagrams.insert(pos,diagram)
    
    def MoveNode(self, parentNode, pos = None):
        self.GetParent().RemoveChild(self)
        self.SetParent(parentNode)
        if pos==None:
            parentNode.AddChild(self)
        else:
            parentNode.AddChild(self,pos)
    
    def FindDiagram(self, name):
        for i in self.diagrams:
            if i.GetName() == name:
                return i
        return None


    def GetChild(self, name, type):
        for i in self.childs:
            if i.GetName() == name and i.GetType() == type:
                return i
        else:
            return None

    def GetIndexChild(self, index):
        if index <= len(self.childs) - 1:
            return self.childs[index]
        else:
            raise ProjectError("NodeNotExists")

    def GetChilds(self):
        for i in self.childs:
            yield i

    def HasChild(self):
        return len(self.childs) > 0

    def GetParent(self):
        return self.parent()
        
    def SetParent(self,parent):
        if parent is None:
            self.parent = lambda: None
        else:
            self.parent = weakref.ref(parent) 

    def RemoveChild(self, child):
        if child in self.childs:
            self.childs.remove(child)
            self.object.AddRevision()
        else:
            raise ProjectError("ChildNotExists")

    def RemoveDiagram(self, diagram):
        if diagram in self.diagrams:
            self.diagrams.remove(diagram)
        else:
            raise ProjectError("AreaNotExists")

    Parent = property(GetParent,SetParent)