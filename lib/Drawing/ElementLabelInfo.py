from math import pi
import weakref

from lib.Math2D import CLine
from CacheableObject import CCacheableObject
from Context import CDrawingContext

positionAngles = {
    'right'      : 0,
    'righttop'   : pi * 1 / 4,
    'top'        : pi * 2 / 4,
    'lefttop'    : pi * 3 / 4,
    'left'       : pi * 4 / 4,
    'leftbottom' : pi * 5 / 4,
    'bottom'     : pi * 6 / 4,
    'rightbottom': pi * 7 / 4,
}


class EElementLabelInfo(Exception): pass

class CElementLabelInfo(CCacheableObject):
    '''
    Stores information about graphical representation of label
    '''

    def __init__(self, element, position, logicalLabel):
        '''
        @param element: owner of label
        @type  element: L{CElement<Element.CElement>}
        
        @param logicalLabel: reference to logical representation of label.
        @type logicalLabel: L{CVisualObject
        <lib.Drawing.Objects.VisualObject.CVisualObject>}
        '''

        CCacheableObject.__init__(self)
        self.dist = 0
        self.angle = pi/2
        self.position = position
        self.actualSize = (0, 0)
        self.element = weakref.ref(element)
        self.logicalLabel = logicalLabel

    def GetSaveInfo(self):
        '''Get information about self to be saved to .frip file
        
        This information can be used to restore values of attributes
        
        @return: dictionary containing essential information
        @rtype: dict
        '''
        return {
            'dist': self.dist,
            'angle': self.angle}

    def SetSaveInfo(self, dist = 0, angle = pi/2):
        '''Get information about self to be saved to .frip file
        
        This information can be used to restore values of attributes
        
        @return: dictionary containing essential information
        @rtype: dict
        '''
        self.dist = float(dist)
        self.angle = float(angle)
        self.position = None

    def GetDiagram(self):
        '''
        @return: diagram to which parent element (owner) belongs
        @rtype:  L{CDiagram<Diagram.CDiagram>}
        '''
        return self.element().GetDiagram()

    def GetObject(self):
        '''
        @return: Logical Label Object
        @rtype: L{CElementObject<lib.Elements.Object.CElementObject>}
        '''
        return self.element().GetObject()

    def GetElement(self):
        return self.element()

    def GetPosition(self):
        '''
        @return: absolute position of top-left corner in 2-tuple (x, y)
        @rtype: tuple
        '''
        width, height = self.GetSize()
        x, y = self.GetAbsolutePosition()
        x, y = x - width / 2.0, y - height / 2.0
        if x < 0 or y < 0:
            self.SetPosition((x, y))
        return int(max((0, x))), int(max((0, y)))

    def SetLogicalLabel(self, logicalLabel):
        '''
        Set reference to logical representation of label
        
        Real size of label cannot be known before this is set. Defaults to 
        (0, 0)
        
        @param logicalLabel: reference to logical representation of label.
        @type logicalLabel: L{CVisualObject
        <lib.Drawing.Objects.VisualObject.CVisualObject>}
        '''
        self.logicalLabel = logicalLabel

    def SetPosition(self, pos):
        '''
        Set absolute position of top-left corner of label
        
        @param pos: (x, y)
        @type  pos: tuple
        '''
        width, height = self.GetSize()
        pos = max((0, pos[0])), max((0, pos[1]))
        self.RecalculatePosition((pos[0] + width / 2.0, pos[1] + height / 2.0))

    def GetSize(self):
        '''
        @return: size of label in 2-tuple (width, height)
        @rtype:  tuple
        '''
        return self.actualSize

    def GetMinimalSize(self):
        '''
        The same as L{GetSize<self.GetSize>}.
        
        @return: size of label in 2-tuple (width, height)
        @rtype:  tuple
        '''
        return self.GetSize()

    def GetSquare(self):
        '''
        Get absolute position of rectangle to which label fits
        
        @return: ((left, top), (right, bottom)) positions of corners
        @rtype:  tuple
        '''

        width, height = self.GetSize()
        x, y = self.GetAbsolutePosition()

        return ( (int(x - width / 2.), int(y - height / 2.) ),
                 (int(x + width / 2.), int(y + height / 2.) ) )

    def GetAbsolutePosition(self):
        '''
        Get center position of label
        
        Center position is used for internal calculations relative to absolute
        and vice-versa
        
        @return: (x, y) position of the middle point of the label
        @rtype: tuple
        '''

        center = self.GetElement().GetCenter()
        return CLine.CreateAsVector(center, self.angle, self.dist).GetEnd().GetPos()

    def RecalculatePosition(self, pos = None):
        '''
        Update relative position according to element's center.

        if pos is None then current position of label is used.

        @param pos: new absolute position (x, y) of label or None
        @type pos: tuple / NoneType
        '''
        x, y = (pos or self.GetAbsolutePosition())
        line = CLine(self.element().GetCenter(), (x, y))
        self.angle = line.Angle()
        self.dist = abs(line)

        self.GetPosition()

    def AreYouAtPosition(self, point):
        '''
        @return: True if (x, y) hits label
        @rtype: bool
        
        @param point: (x, y) position
        @type  point: tuple
        '''
        x, y = point
        ((x1, y1), (x2, y2)) = self.GetSquare()
        return x1 <= x <= x2 and y1 <= y <= y2

    def AreYouInRange(self, topleft, bottomright, all = False):
        '''
        Check whether label is within rectangular area
        
        Can use two policy decision, depending on value of parameter all:
        
            - Whole label must be inside the rectangular area (all == True)
            - Label and rectangular area must have some intersection
        
        @return: True if label is in area
        @rtype: bool
        
        @param topleft: (x, y) position of top-left corner
        @type  topleft: tuple
        
        @param bottomright: (x, y) position of bottom-right corner
        @type  bottomright: tuple
        
        @param all: policy switch
        @type  all: bool
        '''

        class Test(object):
            def __init__(self, square):
                (self.x1, self.y1), (self.x2, self.y2) = square
            def __call__(self, pos):
                return self.x1 <= pos[0] <= self.x2 \
                    and self.y1 <= pos[1] <= self.y2

        t, l = topleft
        b, r = bottomright
        ((x1, y1), (x2, y2)) = self.GetSquare()
        if all:
            return l <= x1 <= x2 <= r and t <= y1 <= y2 <= b
        else:
            return (
                any( map( Test(((x1, y1), (x2, y2))),
                    ((t,l),(t,r),(b,l),(b,r)))) or
                (x1 <= l <= r <= x2 and t <= y1 <= y2 <= b ) or
                (l <= x1 <= x2 <= r and y1 <= t <= b <= y2 ) )

    def SetToDefaultPosition(self, position):
        '''Set absolute and relative position according to default position
        defined by parameter position. Can be moved by offset by appending sign
        "+" or "-" and float number to recognized names of position.

        @param position: one of "center", "source", "destination"
        @type  position: str
        '''

        if position.count('+'): # if there is offset specified
            position, offset = position.split('+', 1) # separate them
            try:
                offset = float(offset)
            except ValueError:
                raise EElementLabelInfo('UndefinedOffset')
        elif position.count('-'): # offset as negative number
            position, offset = position.split('-', 1) # separate them
            try:
                offset = -float(offset)
            except ValueError:
                raise EElementLabelInfo('UndefinedOffset')
        else:
            offset = None

        if position in positionAngles:
            self.angle = 2 * pi - positionAngles[position]
        else:
            raise EElementLabelInfo("UndefinedPosition")

        if offset is not None:
            self.dist = offset
        else:
            self.dist = 60.0

        self.RecalculatePosition()

    def Paint(self, canvas):
        if self.position:
            self.SetToDefaultPosition(self.position)
            self.position = None

        context = CDrawingContext(self.element(), (0,0))
        self.actualSize = self.logicalLabel.GetSize(context)

        (x, y) = self.GetPosition()

        context.SetPosition((x, y))

        self.logicalLabel.Paint(context, canvas)
