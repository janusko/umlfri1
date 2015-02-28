import gtk
from gtk.gdk import CONTROL_MASK, SHIFT_MASK

SCROLL_LEFT = gtk.gdk.SCROLL_LEFT
SCROLL_UP = gtk.gdk.SCROLL_UP
SCROLL_RIGHT = gtk.gdk.SCROLL_RIGHT
SCROLL_DOWN = gtk.gdk.SCROLL_DOWN

class CDrawingAreaScrollEventArgs():

    def __init__(self, direction, modifiers = 0):
        self.direction = direction
        self.modifiers = modifiers

    def IsControlPressed(self):
        return self.modifiers & CONTROL_MASK

    def IsShiftPressed(self):
        return self.modifiers & SHIFT_MASK

    def IsScrollingLeft(self):
        return self.IsScrollingInDirection(SCROLL_LEFT)

    def IsScrollingUp(self):
        return self.IsScrollingInDirection(SCROLL_UP)

    def IsScrollingRight(self):
        return self.IsScrollingInDirection(SCROLL_RIGHT)

    def IsScrollingDown(self):
        return self.IsScrollingInDirection(SCROLL_DOWN)

    def IsScrollingInDirection(self, direction):
        return self.direction == direction