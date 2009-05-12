# -*- coding: utf-8 -*-
from lib.Commands import CBaseCommand

#CCompositeCommand
class CCompositeCommand(CBaseCommand):
    
    def __init__(self):
        CBaseCommand.__init__(self, _('Group Operation:'))
        self.stack = []


    def add(self, commandObject):
        if isinstance(commandObject, CBaseCommand):
            self.stack.append(commandObject)
  
    def do(self):
        for command in self.stack:
            command.do()
            if command.isEnabled():                
                # default way to create composite description is
                # to put every component description on a new line
                self.description += '\n\t' + str(command)
            else:
                self.stack.remove(command)

        if len(self.stack) == 1:
            self.description = str(self.stack[0])


    def undo(self):
        for command in self.stack:
            command.undo()


    def redo(self):
        for command in self.stack:
            command.redo()        

    def isEnabled(self):
        return len(self.stack) > 0
        
        
    def setDesc(self, description):
        self.description = description


    def getStackMembers(self):
        for command in self.stack:
            yield command


    def __str__(self):
        return self.description

