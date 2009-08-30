from lib.Commands import CBaseCommand
from lib.Drawing import  CElement, CConnection


class CElementChangeCmd(CBaseCommand):
    
    def __init__(self, element, key, value, description = None): 
        CBaseCommand.__init__(self, description)
        self.element = element
        self.key = key
        self.value = value
       

    def do (self):
        
        self.old_value = self.element.GetObject().GetValue(self.key)
                
        if str(self.old_value) == self.value:
            self.enabled = False
        else:
            self.element.GetObject().SetValue(self.key, self.value)
            #if self.description == None:
                #if isinstance(self.element, CElement):
                    #name = self.element.GetObject().GetName()
                #elif isinstance(self.element, CConnection):
                    #name = self.element.GetObject().GetType().GetId() + _(' connection')
                #else:
                    #name = self.element.GetObject().GetType().GetId()
    
                #if self.old_value == '':
                    #self.description = _('Setting %s %s to "%s"') %(name, self.key.replace('[',' ').replace('].',' '), self.value)
                #elif self.value == '':
                    #self.description = _('Clearing %s %s') %(name, self.key.replace('[',' ').replace('].',' '))                    
                #else:
                    #self.description = _('Changing %s %s from "%s" to "%s"') %(name, self.key.replace('[',' ').replace('].',' '), self.old_value, self.value)
                        
                        
    def undo(self):
        self.element.GetObject().SetValue(self.key, self.old_value)
        
    def redo(self):
        self.element.GetObject().SetValue(self.key, self.value)
        
        
    def getDescription(self):
        if self.description != None:
            return self.description
        else:
            if isinstance(self.element, CElement):
                name = self.element.GetObject().GetName()
            elif isinstance(self.element, CConnection):
                name = self.element.GetObject().GetType().GetId() + _(' connection')
            else:
                name = self.element.GetObject().GetType().GetId()            
                
            if self.old_value == '':
                return _('Setting %s %s to "%s"') %(name, self.key.replace('[',' ').replace('].',' '), self.value)
            elif self.value == '':
                return _('Clearing %s %s') %(name, self.key.replace('[',' ').replace('].',' '))                    
            else:
                return _('Changing %s %s from "%s" to "%s"') %(name, self.key.replace('[',' ').replace('].',' '), self.old_value, self.value)
                                
 
 