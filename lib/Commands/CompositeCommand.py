from lib.Commands import CBaseCommand


class CCompositeCommand(CBaseCommand):
    '''Class used for grouping other commands
    
    New commands can be add using the add() method.
    Commands will be executed after calling the do() method. If no
    description is provided it will be constructed using the 
    grouped commands descriptions.
    '''      
    def __init__(self):
        CBaseCommand.__init__(self, _('Group Operation:'))
        self.stack = []


    def add(self, commandObject):
        '''
        Adds a new object to stack
        
        @param commandObject: instance to be added to stack
        @type type: L{CBaseCommand<lib.Commands.BaseCommand.CBaseCommand>} 
        '''        
        if isinstance(commandObject, CBaseCommand):
            self.stack.append(commandObject)
  
    def do(self):
        '''
        Iterates over the stacked commands and executes their do() method
        '''        
        for command in self.stack:
            command.do()
            if command.isEnabled():                
                # default way to create composite description is
                # to put every component description on a new line
                self.description += '\n\t' + command.getDescription()
            else:
                self.stack.remove(command)

        if len(self.stack) == 1:
            self.description = self.stack[0].getDescription()


    def undo(self):
        '''
        Iterates over the stacked commands and executes their undo() method
        '''        
        for command in self.stack:
            command.undo()


    def redo(self):
        '''
        Iterates over the stacked commands and executes their redo() method
        '''        
        for command in self.stack:
            command.redo()        

    def isEnabled(self):
        return len(self.stack) > 0
        
        
    def setDesc(self, description):
        '''
        Sets a custom description
        
        @param description: new description
        @type description: str                
        '''        
        self.description = description

    def getDescription(self):
        '''
        Gets current description
        '''         
        return self.description

