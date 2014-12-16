from lib.Drawing.DrawingAreaKeyPressEventArgs import CDrawingAreaKeyPressEventArgs, KEY_LEFT, KEY_UP, KEY_RIGHT, \
    KEY_DOWN


class CDrawingAreaKeyUpEventArgs(CDrawingAreaKeyPressEventArgs):

    def __init__(self, pressedKeys, releasedKey, modifiers = 0):
        CDrawingAreaKeyPressEventArgs.__init__(self, pressedKeys, modifiers)

        self.releasedKey = releasedKey


    def WasArrowKeyPressed(self):
        return self.releasedKey in (KEY_LEFT, KEY_UP, KEY_RIGHT, KEY_DOWN)

    def WasKeyReleased(self, key):
        return self.releasedKey == key