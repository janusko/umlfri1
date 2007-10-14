
import os
import os.path
from CodeContainer import CCodeContainer

class CDirectory(CCodeContainer):
    
    def __init__(self, name, value = ""):
        CCodeContainer.__init__(self)
        self.name = name
        self.value = value
    
    def GetName(self):
        return self.name
        
    def Generate(self, element, path, file = None):
        name, = self.GetVariables(element, 'name')
        new_path = os.path.join(path,name)
        if not os.path.exists(new_path):
            os.mkdir(new_path)
        ret = [True, ""]
        for i in self.childs:
            self.JoinReturnValue(ret, i.Generate(element, new_path, file))
        
        return ret
        
        
    def GetRules(self):
        yield self.GetSymbol(), ['dir:'+self.value] + [child.GetSymbol() for child in self.childs if child.Parse()] + ['eod']
        for rule in self.GetChildRules():
            yield rule
        
    def GetTokens(self):
        yield 'dir:'+self.value, self.value, 'dir'