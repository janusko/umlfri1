from lib.consts import MAX_UNDO_STACK_SIZE

class CCommandProcessor(object):
    '''
    Command processor and history object
    '''
    def __init__(self, guiBus):
        self.__undoStack = []
        self.__redoStack = []
        self.__guiBus = guiBus
    
    def Execute(self, command):
        '''
        Executes the given command and stores it in the history
        '''
        command.Do()
        
        if not command.IsError():
            del self.__redoStack[:]
            
            self.__undoStack.insert(0, command)
            if MAX_UNDO_STACK_SIZE is not None and len(self.__undoStack) > MAX_UNDO_STACK_SIZE:
                del self.__undoStack[MAX_UNDO_STACK_SIZE:]
            
            guiUpd = command.GetGuiUpdates()
            if guiUpd:
                self.__guiBus.DoUpdates(guiUpd)
    
    def Undo(self, count = 1):
        '''
        Undo given count of the operations.
        
        '''
        toUndo = self.__undoStack[:count]
        del self.__undoStack[:count]
        
        guiUpd = []
        
        for cmd in toUndo:
            cmd.Undo()
            guiUpd.extend(cmd.GetGuiUpdates())
        
        self.__redoStack[:0] = toUndo
            
        if guiUpd:
            self.__guiBus.UndoUpdates(guiUpd)
    
    def Redo(self, count = 1):
        toRedo = self.__redoStack[:count]
        del self.__redoStack[:count]
        
        guiUpd = []
        
        for cmd in toRedo:
            cmd.Redo()
            guiUpd.extend(cmd.GetGuiUpdates())
        
        self.__undoStack[:0] = toRedo
            
        if guiUpd:
            self.__guiBus.Undo(guiUpd)
    
    def GetUndoStack(self, limitation = None):
        if limitation is None:
            toReturn = self.__undoStack[:limitation]
        else:
            toReturn = self.__undoStack
        
        return (str(cmd) for cmd in toReturn)
    
    def GetRedoStack(self, limitation = None):
        if limitation is None:
            toReturn = self.__redoStack[:limitation]
        else:
            toReturn = self.__redoStack
        
        return (str(cmd) for cmd in toReturn)
    
    def CanUndo(self):
        return bool(self.__undoStack)
    
    def CanRedo(self):
        return bool(self.__redoStack)
    
    def Clear(self):
        del self.__redoStack[:]
        del self.__undoStack[:]
