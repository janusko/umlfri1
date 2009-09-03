
class CBaseCommand:
    '''Super class for all undoable operations
    
    All the children classes have to implement (override) these methods so the CommandProcessor will be able 
    to undo/redo them. The actions needed to do() and undo()/redo() depend on the specific kind of
    operation, but these methods can't have any arguments. All the necessary data should be 
    fed throught __ini__
    '''    
    def __init__(self):
        self.enabled = True 
        
    def Do(self):
        '''steps needed to initially execute the command
        should _not_ have any arguments, nor return values
        '''
        raise NotImplementedError
             
    def Undo(self):
        '''steps needed to undo the command
        should _not_ have any arguments, nor return values
        '''
        raise NotImplementedError
    
    def Redo(self):
        '''steps needed to redo the command, in some cases could be the same as the do() method
        should _not_ have any arguments, nor return values
        '''
        self.Do()
    
    def IsEnabled(self):
        '''Returns True if the command is valid, otherwise returns False
        Instance should be marked as not enabled, if during the commands do() method
        it's found out, that this user action is illegal - wont be done so logically
        shouldn't be part of the history
        
        @note: if an instance is marked as not enabled, it wont be added to undo stack
        '''
        return self.enabled

    def GetDescription(self):
        '''Returns a string containing the description of the command.
        Mandatory - used to show the user what kind of action command does 
        '''
        raise NotImplementedError
