from VisibleObject import IVisibleObject
from lib.Addons.Plugin.Communication.ComSpec import *
from lib.Addons.Plugin.Interface.decorators import *
from lib.Drawing.ConLabelInfo import CConLabelInfo

class IConnectionLabel(IVisibleObject):
    __cls__ = CConLabelInfo
    
