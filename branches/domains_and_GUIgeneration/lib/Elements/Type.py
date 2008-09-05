from lib.lib import ToBool
from lib.Exceptions.UserException import *

class CElementType(object):
    def __init__(self, id):
        self.icon = None
        self.id = id
        self.attributes = {}
        self.connections = {}
        self.appearance = None
        self.visAttrs = {}
        self.attributeList = []
        self.generatename = True
    
    def AppendAttribute(self, value, type, propid = None, options = [], itemtype=None):
        if propid is not None:
            self.visAttrs[propid] = value
        self.attributes[value] = (type, options)
        self.attributeList.append(value)
    
    def AppendConnection(self, value, withobject, allowrecursive):
        self.connections[value] = (withobject, allowrecursive)
    
    def GetAppearance(self):
        return self.appearance
                
    def GetConnections(self):
        for item in self.connections.iteritems():
            yield item
    
    def GetIcon(self):
        return self.icon
    
    def GetId(self):
        return self.id
    
    def GetResizable(self):
        return self.appearance.GetResizable()
    
    def GetDefValue(self, id):
        type, options = self.attributes[id]
        if len(options) > 0:
            temp = options[0]
        else:
            temp = None
        if type == 'int':
            if temp is None:
                return 0
            else:
                return int(temp)
        if type == 'enum':
            if temp is None:
                raise ElementAttributeError("ListNoOptions")
            else:
                return str(temp)
        elif type == 'float':
            if temp is None:
                return 0.0
            else:
                return float(temp)
        elif type == 'bool':
            if temp is None:
                return False
            else:
                return ToBool(temp)
        elif type == 'str':
            if temp is None:
                return ""
            else:
                return str(temp)
        elif type == 'note':
            if temp is None:
                return ""
            else:
                return str(temp)
        elif type == 'attrs':
            return []
        elif type == 'opers':
            return []
    
    def TypeCastAttribute(self, key, value):
        type, options = self.attributes[key]
        if type == 'int':
            return int(value)
        if type == 'enum':
            return str(value)
        elif type == 'float':
            return float(value)
        elif type == 'bool':
            return ToBool(value)
        elif type == 'str':
            return str(value)
        elif type == 'note':
            return str(value)
        elif type == 'attrs':
            ret = []
            for i in value:
                ret.append({'name': str(i['name']), 'type': str(i['type']), 'scope': str(i['scope']),
                            'stereotype': str(i['stereotype']), 'containment': str(i['containment']), 'initial': str(i['initial']),
                            'doc': str(i['doc']), 'derived': ToBool(i['derived']), 'static': ToBool(i['static']),
                            'property': ToBool(i['property']), 'const': ToBool(i['const'])
                })
            return ret
        elif type == 'opers':
            ret = []
            for i in value:
                ret.append({'name': str(i['name']), 'params': str(i['params']), 'abstract': ToBool(i['abstract']),
                            'static': ToBool(i['static']), 'const': ToBool(i['const']), 'returnarray': ToBool(i['returnarray']),
                            'pure': ToBool(i['pure']), 'synchronize': ToBool(i['synchronize']), 'isquery': ToBool(i['isquery']),
                            'scope': str(i['scope']), 'type': str(i['type']), 'stereotype': str(i['stereotype']),
                            'doc': str(i['doc'])
                })
            return ret
    
    def GetAttributes(self):
        for i in self.attributeList:
            yield i
            
    def GetAttribute(self, key):
        return self.attributes[key]
    
    def GetGenerateName(self):
        return self.generatename
        
    def SetGenerateName(self, generate):
        self.generatename = generate
        
    def Paint(self, canvas, element, delta = (0, 0)):
        dx, dy = delta
        x, y = element.GetPosition()
        pos = (x + dx,  y + dy)
        self.appearance.Paint(canvas, pos, element, element.GetSize(canvas))
    
    def SetAppearance(self, appearance):
        self.appearance = appearance
    
    def SetIcon(self, pixbuf):
        self.icon = pixbuf
    
    def SetId(self, id):
        self.id = id
    
    def HasVisualAttribute(self, id):
        return id in self.visAttrs.itervalues()
    
    def GetVisAttr(self, id):
        if id in self.visAttrs:
            return self.visAttrs[id]
        else:
            raise ElementAttributeError('VisAttrDontExists')
    
    def GetSize(self, canvas, element):
        return self.appearance.GetSize(canvas, element)
