from VisibleObject import IVisibleObject
from lib.Plugin.Communication.ComSpec import *
from lib.Plugin.Interface.decorators import *
from lib.Drawing.ConLabelInfo import CConLabelInfo

class IConLabelInfo(IVisibleObject):
    __cls__ = CConLabelInfo
    
