# -*- coding: utf-8 -*-
from lib.Commands import CBaseCommand
from lib.Exceptions.DevException import HistoryError
import lib.consts


# CCommandProcessor
class CCommandProcessor:
    
    def __init__(self):
        self.undoStack = []
        self.redoStack = []


    def __getStackDesc(self, redo = False, limitation = 0):
        '''
        Gets a description list from eather the redo or undo stack
        
        @param redo: True if redo descriptions are wanted, undo otherwise (by default)
        @type redo: bool
        
        @return: list containing all the stack descriptions
        @rtype: list
        '''
        descriptionList = []
        
        if not redo:
            for undo in self.undoStack:
                descriptionList.append(str(undo))
        else:
            for redo in self.redoStack:
                descriptionList.append(str(redo))
            
        if limitation:
            return descriptionList[-limitation:]
        
        return descriptionList
 
 
    def add(self, commandObject):
        '''
        Adds a new object to applications history undo stack
        
        @param o: instance to be added to undo stack  or group !
        @type type: L{CBaseCommand<lib.Commands.BaseCommand.CBaseCommand>} 
        '''
        
        if isinstance(commandObject, CBaseCommand):
            commandObject.do()                              # execute the command
            if commandObject.isEnabled():                   # if all went good...
                self.redoStack = []                         # emty the redo stack - linear restrictive undo
                self.undoStack.append(commandObject)        # and add the command to undo undo stack 
            
            # if the stack is bigger then the max allowed size, crop the oldest commands
            if len(self.undoStack) > lib.consts.STACK_MAX_SIZE:
                   self.undoStack = self.undoStack[-lib.consts.STACK_MAX_SIZE:]
          
        else: 
            raise HistoryError(_('Invalid History object. Must be a child of lib.Commands.CBaseCommand'))



    def undo(self):
        if self.canUndo():
            undoStackItem = self.undoStack.pop()
            undoStackItem.undo()
            self.redoStack.append(undoStackItem)
            

    def redo(self):
         if self.canRedo():
            redoStackItem = self.redoStack.pop()
            redoStackItem.redo()       
            self.undoStack.append(redoStackItem)


    def getUndoDesc(self, limitation = 0):
        return self.__getStackDesc(False, limitation)


    def getRedoDesc(self, limitation = 0):
        return self.__getStackDesc(True, limitation)


    def canUndo(self):
        return len(self.undoStack) > 0


    def canRedo(self):
        return len(self.redoStack) > 0


    def clear(self):
        self.undoStack = []
        self.redoStack = []
 
 

            