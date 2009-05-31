from Condition import CCondition
from Container import CContainer
from Ellipse import CEllipse
from HBox import CHBox
from Line import CLine
from Loop import CLoop
from Padding import CPadding
from Rectangle import CRectangle
from SimpleContainer import CSimpleContainer
from TextBox import CTextBox
from VBox import CVBox
from Shadow import CShadow
from Proportional import CProportional
from Align import CAlign
from Svg import CSvg
from Sizer import CSizer
from Icon import CIcon
from Switch import CCase, CSwitch
from Diamond import CDiamond

from ConnectionArrow import CConnectionArrow
from ConnectionLine import CConnectionLine

ALL = {'Condition': CCondition, 'Ellipse': CEllipse, 'HBox': CHBox, 'Line': CLine, 'Loop': CLoop,
       'Padding': CPadding, 'Rectangle': CRectangle, 'TextBox': CTextBox, 'VBox': CVBox,
       'Shadow': CShadow, 'Proportional': CProportional, 'Align': CAlign, 'Svg': CSvg,
       'Sizer': CSizer, 'Icon': CIcon, 'Case': CCase, 'Switch': CSwitch, 'Diamond': CDiamond}

ALL_CONNECTION = {'Condition': CCondition, 'Loop': CLoop, 'Shadow': CShadow, 'Case': CCase, 'Switch': CSwitch,
                  'ConnectionLine': CConnectionLine, 'ConnectionArrow': CConnectionArrow}
