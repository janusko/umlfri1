from lib.Drawing.DrawingAreaKeyPressEventArgs import CDrawingAreaKeyPressEventArgs

class CDrawingAreaKeyUpEventArgs(CDrawingAreaKeyPressEventArgs):

    def __init__(self, pressedKeys, modifiers = 0):
        CDrawingAreaKeyPressEventArgs.__init__(self, pressedKeys, modifiers)