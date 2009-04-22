# -*- coding: utf-8 -*-
from lib.History import CHistoryOperation
from lib.Exceptions.DevException import HistoryError
import lib.consts
from HistoryGroup import CHistoryGroup



class CApplicationHistory:
    
    def __init__(self):
        self.undoStack = []
        self.redoStack = []
        self.group = CHistoryGroup()
        self.groupIsOpen = False


    def __getStackDesc(self, redo = False, limitation = 0):
        descriptionList = []
        
        if not redo:
            for undo in self.undoStack:
                descriptionList.append(str(undo))
        else:
            for redo in self.redoStack:
                descriptionList.append(str(redo))
            
        if limitation:
            return descriptionList[:limitation]
        
        return descriptionList
 
 
    def add(self, o):
        if isinstance(o, CHistoryOperation):
            if o.isEnabled():
                self.redoStack = []    
                if self.groupIsOpen:
                    self.group.add(o)
                else:   
                    self.undoStack.append(o) 
          
            if len(self.undoStack) > lib.consts.STACK_MAX_SIZE:
                   self.undoStack = self.undoStack[-lib.consts.STACK_MAX_SIZE:]
          
        else: 
            raise HistoryError(_('Invalid History object. Must be a child of lib.Undo.AbstractUndo'))



    def undo(self):
        
        if len(self.undoStack) > 0:
            undoStackItem = self.undoStack.pop()
    
            if isinstance(undoStackItem, CHistoryGroup):
                for undoGroup in undoStackItem.getStack():
                    undoGroup.undo()
            else:
                undoStackItem.undo()
                
            self.redoStack.append(undoStackItem)
            

    def redo(self):
        
         if len(self.redoStack) > 0:
            redoStackItem = self.redoStack.pop()
            
            if isinstance(redoStackItem, CHistoryGroup):
                for redoGroup in redoStackItem.getStack():
                    redoGroup.redo()
            else:
                redoStackItem.redo()       
    
            self.undoStack.append(redoStackItem)


    def startGroup(self):
        if not self.groupIsOpen:
            self.groupIsOpen = True
            self.group = CHistoryGroup()
        else: 
            raise HistoryError(_('History group is already open.'))


    def isGroupOpen(self):
        return self.groupIsOpen


    def endGroup(self):
        
        if self.groupIsOpen:
            self.groupIsOpen = False
            
            # if the group has only 1 member, insert only the group member
            if len(self.group.getStack()) == 1:
                self.undoStack.append(self.group.getStack()[0])
            else:
                self.undoStack.append(self.group)
        else: 
            raise HistoryError(_('There is no open History group. Nothing to close...'))
        

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
 
 

            