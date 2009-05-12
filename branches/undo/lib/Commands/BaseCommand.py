# -*- coding: utf-8 -*-

class CBaseCommand:
    '''Super class for all undoable operations
    
    All the children classes have to implement (overload) these methods so the AplicationHistory will be able 
    to undone/redone them. The actions needed to do() and undo()/redo() depend on the specific kind of
    operation, but these methods can't have any arguments. All the necessary data should be 
    fed throught the __ini__ constructor
    '''    
    def __init__(self, description = None):
        self.description = description
        self.enabled = True 
        
    def do(self):
        '''steps needed to initially execute the command, is done only one time
        for each command, when the action occurs
        should _not_ have any arguments, nor return values
        '''
        pass
     
    def undo(self):
        '''steps needed to undo the command
        should _not_ have any arguments, nor return values
        '''
        pass
    
    def redo(self):
        '''steps needed to redo the command, in some cases could be the same as the do() method
        should _not_ have any arguments, nor return values
        '''
        self.do()
    
    def isEnabled(self):
        '''Returns True if the history action (undo or redo) is valid, otherwise return False
        Instance should be marked as not enabled, if during the commands operations it found out, that this user action is
        illegal - wont be done so logically shouldn't be part of the history
        
        @note: if an instance is marked as not enabled, it wont be added to undo stack
        '''
        return self.enabled
    

    def __str__(self):
        '''Returns a string containing the description of the command.
        Mandatory - shows the user undo/redoable steps
        '''
        if self.description == None:
            return _("History Operation")
        else:
            return self.description