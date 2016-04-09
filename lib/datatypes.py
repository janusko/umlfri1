import colors
import re

from Base import CBaseObject

class CColor(CBaseObject):
    def __init__(self, color):
        if isinstance(color, CColor):
            self.__color = color.__color
        else:
            self.__color = colors.colors.get(color, color)
    
    def GetRed(self):
        return int(self.__color[1:3], 16)
    
    def GetGreen(self):
        return int(self.__color[3:5], 16)
    
    def GetBlue(self):
        return int(self.__color[5:7], 16)
    
    def Invert(self):
        return CColor(colors.invert(self.__color))
    
    def __str__(self):
        return self.__color

class CFont(CBaseObject):

    def __init__(self, font):
        if isinstance(font, CFont):
            self.__fontFamily = font.__fontFamily
            self.__fontSize = font.__fontSize
            self.__fontStyle = set(font.__fontStyle)
        else:
            tmp = font.split()
            self.__fontSize = int(tmp.pop(-1))
            self.__fontStyle = set()
            while tmp[-1].lower() in ('bold', 'italic', 'underline', 'strike'):
                self.__fontStyle.add(tmp.pop(-1).lower())
            self.__fontFamily = ' '.join(tmp)
    
    def GetSize(self):
        return self.__fontSize
    
    def GetStyle(self):
        return self.__fontStyle
    
    def GetFamily(self):
        return self.__fontFamily
    
    def ChangeStyle(self, style, doIt = True):
        if not doIt:
            return self
        
        tmp = CFont(self)
        tmp.__fontStyle.add(style)
        return tmp
    
    def ChangeSize(self, delta, doIt = True):
        if not doIt:
            return self
        
        tmp = CFont(self)
        tmp.__fontSize += delta
        return tmp
    
    def __str__(self):
        if self.__fontStyle:
            return ' '.join((self.__fontFamily, ' '.join(self.__fontStyle), str(self.__fontSize)))
        else:
            return ' '.join((self.__fontFamily, str(self.__fontSize)))


class MethodAttrTypes(object):
    ATTRIBUTES = {}
    METHODS = {
        CColor: {
        },
        CFont: {
            'GetSize': {
                'args': [],
                'rtype': int
            },
            'GetStyle': {
                'args': [],
                'rtype': set
            },
            'GetFamily': {
                'args': [],
                'rtype': (str, unicode)
            },
            'ChangeStyle': {
                'args': [str, bool],
                'rtype': CFont
            },
            'ChangeSize': {
                'args': [int, bool],
                'rtype': int
            }
        }
    }

    def GetMethod(self, type_, name):
        if type_ in self.METHODS:
            if name in self.METHODS[type_]:
                args = self.METHODS[type_][name]['args']
                rtype = self.METHODS[type_][name]['rtype']
                return args, rtype


class CVersion(object):
    __reVersion = re.compile(r'(?P<version>[0-9]+(\.[0-9]+)*)(?P<verchar>[a-z])?(-(?P<suffix>(alpha|beta|pre|rc|p))(?P<sufnum>[0-9]+))?(@(?P<rev>([0-9]+|\*)))?$')
    __full = ('full', )
    
    def __init__(self, value):
        parsed = self.__reVersion.search(value)
        
        if parsed is None:
            raise Exception("Invalid version number")
        else:
            ver = tuple(int(i) for i in parsed.group('version').split('.'))
            ver = (ver + (0, 0, 0))[:3]
            
            if parsed.group('verchar') is not None:
                ver += (parsed.group('verchar'), )
            
            self.__version = ver
            
            if parsed.group('suffix') is None:
                self.__suffix = None
            else:
                self.__suffix = (parsed.group('suffix'), int(parsed.group('sufnum')))
            
            if parsed.group('rev') is None:
                self.__revision = None
            else:
                self.__revision = int(parsed.group('rev'))
    
    def GetVersion(self):
        return self.__version
    
    def GetSuffix(self):
        return self.__suffix
    
    def GetRevision(self):
        return self.__revision
    
    def OfRevision(self, revision):
        ver = '.'.join(str(part) for part in self.__version)
        if self.__suffix:
            ver += '-%s%d'%self.__suffix
        if revision:
            ver += '@%d'%revision
        
        return self.__class__(ver)
    
    def __cmp__(self, other):
        if not isinstance(other, CVersion):
            return NotImplemented
        
        return cmp(
            (self.__version, self.__suffix or self.__full, self.__revision or 0),
            (other.__version, other.__suffix or self.__full, other.__revision or 0)
        )
    
    def __lt__(self, other):
        return self.__cmp__(other) < 0
    
    def __le__(self, other):
        return self.__cmp__(other) <= 0
    
    def __eq__(self, other):
        return self.__cmp__(other) == 0
    
    def __ne__(self, other):
        return self.__cmp__(other) != 0
    
    def __gt__(self, other):
        return self.__cmp__(other) > 0
    
    def __ge__(self, other):
        return self.__cmp__(other) >= 0
    
    def __str__(self):
        ver = '.'.join(str(part) for part in self.__version)
        if self.__suffix:
            ver += '-%s%d'%self.__suffix
        if self.__revision:
            ver += '@%d'%self.__revision
        
        return ver
    
    def __repr__(self):
        return '<%s %s>'%(self.__class__.__name__, self)
    
    def __add__(self, other):
        return str(self) + other
    
    def __radd__(self, other):
        return other + str(self)
