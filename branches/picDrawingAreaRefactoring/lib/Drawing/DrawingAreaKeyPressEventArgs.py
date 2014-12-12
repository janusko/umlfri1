import gtk
from gtk.gdk import CONTROL_MASK, SHIFT_MASK

KEY_A = gtk.keysyms.a
KEY_LEFT = gtk.keysyms.Left
KEY_RIGHT = gtk.keysyms.Right
KEY_UP = gtk.keysyms.Up
KEY_DOWN = gtk.keysyms.Down
KEY_DELETE = gtk.keysyms.Delete
KEY_SPACE = gtk.keysyms.space
KEY_ESCAPE = gtk.keysyms.Escape

class CDrawingAreaKeyPressEventArgs():

    def __init__(self, pressedKeys, modifiers = 0):
        self.pressedkeys = pressedKeys
        self.modifiers = modifiers

    def IsControlPressed(self):
        return self.modifiers & CONTROL_MASK

    def IsShiftPressed(self):
        return self.modifiers & SHIFT_MASK

    def IsArrowKeyPressed(self):
        return self.pressedkeys in (KEY_LEFT, KEY_UP, KEY_RIGHT, KEY_DOWN)

    def IsKeyPressed(self, key):
        return key in self.pressedkeys