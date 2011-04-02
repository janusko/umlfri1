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

class CVersion(str):
    __reVersion = re.compile(r'(?P<version>[0-9]+(\.[0-9]+)*)(?P<verchar>[a-z])?(-(?P<suffix>(alpha|beta|pre|rc|p))(?P<sufnum>[0-9]+))?(@(?P<rev>([0-9]+|\*)))?$')
    
    def __init__(self, value):
        str.__init__(self, value)
        
        parsed = self.__reVersion.search(value)
        
        if parsed is None:
            raise Exception("Invalid version number")
        else:
            self.__version = tuple(int(i) for i in parsed.group('version').split('.'))
            if parsed.group('verchar') is not None:
                self.__version += (parsed.group('verchar'), )
            
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
    
    def __cmp__(self, other):
        if not isinstance(other, CVersion):
            return NotImplemented
        
        return cmp((self.__version, self.__suffix, self.__revision), (other.__version, other.__suffix, other.__revision))
