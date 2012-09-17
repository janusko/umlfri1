from VisualObject import CVisualObject

class CContainer(CVisualObject):
    def __init__(self):
        CVisualObject.__init__(self)
        self.childs = []

    def AppendChild(self, child):
        self.childs.append(child)
        child.SetParent(self)
    
    def GetResizable(self, context):
        rx, ry = False, False
        for i in self.childs:
            rcx, rcy = i.GetResizable(context)
            rx = rx or rcx
            ry = ry or rcy
            if rx and ry:
                return True, True
        return rx, ry

    def GetChild(self, index):
        return self.childs[index]

    def GetChilds(self):
        return self.childs

    def ComputeSize(self, context):
        w = 0
        h = 0
        for i in self.childs:
            wc, hc = i.GetSize(context)
            w = max(w, wc)
            h = max(h, hc)
        return (w, h)

    def Paint(self, context):
        size = context.ComputeSize(self)
        for i in self.childs:
            i.Paint(context)

    def RemoveChild(self, child):
        self.childs.remove(child)
