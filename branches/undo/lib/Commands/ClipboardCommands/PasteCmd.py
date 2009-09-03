from lib.Commands import CBaseCommand
from lib.Drawing import  CElement
from lib.Exceptions.UMLException import UMLException
from lib.Exceptions.UserException import DrawingError


class CPasteCmd(CBaseCommand):
    
    def __init__(self, diagram, clipboard): 
        CBaseCommand.__init__(self)
        self.diagram = diagram
        self.clipboard = clipboard
        
    def Do(self):
        if self.clipboard.content:
            self.pasted = []
            for element in self.clipboard.content:
                try:
                    el = CElement(self.diagram, element.GetObject())
                except UMLException, e:
                    cause = str(e)
                    if 'DiagramHaveNotThisElement' in cause:
                        text = _('This diagram can not have this element.')
                    elif 'ElementAlreadyExists' in cause:
                        text = _('This element already exists on this diagram')
                    else:
                        text = cause
                    
                    for el in self.pasted:
                        self.diagram.DeleteElement(el)
                    raise DrawingError(text)
                
                self.diagram.AddToSelection(el)
                el.CopyFromElement(element)
                self.pasted.append(el)
        else:
            self.enabled = False

    def Undo(self):
        for el in self.pasted:
            el.Deselect()
            el.GetObject().RemoveAppears(self.diagram)
            self.diagram.DeleteElement(el)

    def Redo(self):
        for el in self.pasted:
            el.GetObject().AddAppears(self.diagram)
            self.diagram.AddElement(el)

    def GetDescription(self):
        return _('Pasting selection')
