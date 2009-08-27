import colors

class CColor(object):
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

class CFont(object):
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
