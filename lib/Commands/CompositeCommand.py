from lib.Commands import CBaseCommand


class CCompositeCommand(CBaseCommand):
    '''Class used for grouping other commands
    
    New commands can be add using the add() method.
    Commands will be executed after calling the do() method. If no
    description is provided it will be constructed using the 
    grouped commands descriptions.
    '''      
    def __init__(self):
        CBaseCommand.__init__(self)
        self.stack = []

    def add(self, commandObject):
        '''
        Adds a new object to stack
        
        @param commandObject: instance to be added to stack
        @type type: L{CBaseCommand<lib.Commands.BaseCommand.CBaseCommand>} 
        '''        
        if isinstance(commandObject, CBaseCommand):
            self.stack.append(commandObject)
  
    def Do(self):
        '''
        Iterates over the stacked commands and executes their do() method
        '''        
        for command in self.stack:
            command.Do()
            if not command.isEnabled():                
                self.stack.remove(command)

    def Undo(self):
        '''
        Iterates over the stacked commands and executes their undo() method
        '''        
        for command in self.stack:
            command.Undo()

    def Redo(self):
        '''
        Iterates over the stacked commands and executes their redo() method
        '''        
        for command in self.stack:
            command.Redo()        

    def isEnabled(self):
        return len(self.stack) > 0

    def GetDescription(self):
        '''
        Gets current description
        ''' 
        if len(self.stack) == 1:
            return self.stack[0].getDescription()
        description = [_('Group Operation:')]

        for command in self.stack:
            
            if command.isEnabled():                
                # default way to create composite description is
                # to put every component description on a new line
                description.append(command.getDescription())
        
        return '\n\t'.join(description)
