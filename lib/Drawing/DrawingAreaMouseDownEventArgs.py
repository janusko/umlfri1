from gtk.gdk import CONTROL_MASK, SHIFT_MASK


class CDrawingAreaMouseDownEventArgs():

    def __init__(self, position, button, isDoubleClick = False, wasSpacePressed = False, modifiers = 0):
        self.position = position
        self.button = button
        self.isDoubleClick = isDoubleClick
        self.wasSpacePressed = wasSpacePressed
        self.modifiers = modifiers

    def IsControlPressed(self):
        return self.modifiers & CONTROL_MASK

    def IsShiftPressed(self):
        return self.modifiers & SHIFT_MASK