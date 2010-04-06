# -*- coding: utf-8 -*-

"""The class to wrap methods for Element Alignment"""

class CsetToAlign(set):

    #constructor
    def __init__(self, setOfSelectedElements, diagram=None):
        """Constructor takes as the argument container of all the SELECTED
        elements or generator of that container"""
        set.__init__(self, setOfSelectedElements)
        self.diagram =diagram
    
    #other public methods
#--left alignment
    def AlignLeft(self, setLeftCoordinate):
        # set the x position to setLeftCoordinate
        for sel in self:
            sel.SetPosition( (setLeftCoordinate, sel.GetPosition()[1] ) )
        # But preserve the Y coordinate ("sel.GetPosition()[1]")
    
    def AlignMostLeft(self):
        try:
            #take the MINIMAL ("min") X position ("GetPosition()[0]") =most left
            min_left =min( [ i.GetPosition()[0] for i in self] )
        except ValueError: #if NO element selected
            return
        # now we have the most left location
        # set the x position of all selected elements to that most left one!
        for sel in self:
            sel.SetPosition((min_left, sel.GetPosition()[1]))
        # But preserve the Y coordinate ("sel.GetPosition()[1]")
#--right alignment
    def AlignRight(self, setRightCoordinate):
        # set the x position to setRightCoordinate
        for sel in self:
            sel.SetPosition( (setRightCoordinate -sel.GetSize(self.diagram)[0], sel.GetPosition()[1] ) )
        # But preserve the Y coordinate ("sel.GetPosition()[1]")
    
    def AlignMostRight(self):
        try:
            #take the MAXIMAL ("max") X position ("GetPosition()[0] +i.GetSize(self.diagram)[0]") =most right
            max_right =max( [ i.GetPosition()[0] +i.GetSize(self.diagram)[0] for i in self] )
        except ValueError: #if NO element selected
            return
        # now we have the most right location
        # set the x position of all selected elements to that most right one!
        for sel in self:
            sel.SetPosition((max_right -sel.GetSize(self.diagram)[0], sel.GetPosition()[1]))
        # But preserve the Y coordinate ("sel.GetPosition()[1]")
#--top alignment
    def AlignTop(self, setTopCoordinate):
        # set the y position to setTopCoordinate
        for sel in self:
            sel.SetPosition( (sel.GetPosition()[0], setTopCoordinate ) )
        # But preserve the X coordinate ("sel.GetPosition()[0]")
    
    def AlignMostTop(self):
        try:
            #take the MINIMAL ("min") Y position ("GetPosition()[1]") =most top
            min_top =min( [ i.GetPosition()[1] for i in self] )
        except ValueError: #if NO element selected
            return
        # now we have the most top location
        # set the y position of all selected elements to that most top one!
        for sel in self:
            sel.SetPosition( (sel.GetPosition()[0], min_top ) )
        # But preserve the X coordinate ("sel.GetPosition()[0]")
#--bottom alignment
    def AlignBottom(self, setBottomCoordinate):
        # set the y position to setBottomCoordinate
        for sel in self:
            sel.SetPosition( (sel.GetPosition()[0], setBottomCoordinate -sel.GetSize(self.diagram)[1]) )
        # But preserve the X coordinate ("sel.GetPosition()[0]")
    
    def AlignMostBottom(self):
        try:
            #take the MINIMAL ("max") Y position ("GetPosition()[1] +i.GetSize(self.diagram)[1]") =most bottom
            max_bottom =max( [ i.GetPosition()[1] +i.GetSize(self.diagram)[1] for i in self] )
        except ValueError: #if NO element selected
            return
        # now we have the most bottom location
        # set the y position of all selected elements to that most bottom one!
        for sel in self:
            sel.SetPosition( (sel.GetPosition()[0], max_bottom -sel.GetSize(self.diagram)[1]) )
        # But preserve the Y coordinate ("sel.GetPosition()[1]")
