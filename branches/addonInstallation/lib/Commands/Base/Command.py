class CommandNotDone(Exception):
    pass

class CCommand(object):
    '''
    Super class for all undoable operations
    '''
    
    def __init__(self):
        self.__done = False
        self.__undone = False
        self.__error = False
    
    def _Do(self):
        '''
        Steps needed to execute the command for the first time
        '''
        raise NotImplementedError
    
    def _Undo(self):
        '''
        Steps needed to undo the command
        '''
        raise NotImplementedError
    
    def _Redo(self):
        '''
        Steps needed to redo the command
        '''
        self._Do()
    
    def _CopyStatusTo(self, other):
        other.__done = self.__done
        other.__undone = self.__undone
        other.__error = self.__error
    
    def Do(self):
        '''
        Execute operation for the first time
        '''
        
        if self.__done:
            raise Exception("Cannot do operation that was already done")
        
        try:
            self._Do()
        except CommandNotDone:
            self.__error = True
        except:
            self.__error = True
            raise
        else:
            self.__done = True
    
    def Undo(self):
        '''
        Undo the command
        '''
        
        if self.__error:
            raise Exception("Command is in the error state")
        
        if not self.__done:
            raise Exception("Cannot undo command that was not executed")
        
        if self.__undone:
            raise Exception("Cannot undo undone operation")
        
        self._Undo()
        self.__undone = True
    
    def Redo(self):
        '''
        Redo the command
        '''
        
        if self.__error:
            raise Exception("Command is in the error state")
        
        if not self.__done:
            raise Exception("Cannot redo command that was not executed")
        
        if not self.__undone:
            raise Exception("Cannot redo operation that was not undone")
        
        self._Redo()
        self.__undone = False
    
    def Fold(self, other):
        return None
    
    def IsError(self):
        '''
        Informs about the state of the command
        
        @return: True if operation was ended with the error
        @rtype: bool
        '''
        return self.__error
    
    def IsDone(self):
        '''
        Informs about the state of the command
        
        @return: True if operation was done yet
        @rtype: bool
        '''
        return self.__done
    
    def GetGuiUpdates(self):
        return []
    
    def GetGuiActions(self):
        return []
