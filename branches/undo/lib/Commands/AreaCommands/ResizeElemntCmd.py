from lib.Commands import CBaseCommand


class CResizeElemntCmd(CBaseCommand):

    def __init__(self, element, canvas, delta, selSq): 
        CBaseCommand.__init__(self)
        self.element = element
        self.canvas = canvas
        self.delta = delta
        self.selSq = selSq

    def Do(self):
        self.element.Resize(self.canvas, self.delta, self.selSq)
        
    def Undo(self):
        self.element.Resize(self.canvas, (-self.delta[0], -self.delta[1]), self.selSq)

    def Redo(self):
        self.element.Resize(self.canvas, self.delta, self.selSq)
        
    def GetDescription(self):
        return _('Resizing %s') %(self.element.GetObject().GetName())
