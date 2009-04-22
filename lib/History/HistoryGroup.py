# -*- coding: utf-8 -*-


class CHistoryGroup:
    
    def __init__(self):
        self.description = _('Group Operation:')
        self.stack = []
        
    def setDesc(self, description):
        self.description = description

    def add(self, o):
        self.stack.append(o)
        self.description += '\n\t' + str(o)
        
    def getStack(self):
        return self.stack

    def __str__(self):
        return self.description

