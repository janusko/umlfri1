# -*- coding: utf-8 -*-

"""
The module of for complete tidy of the diagram
"""
class CTidyMath(object):
    #constructor
    def __init__(self, positionList, sizeList, centerList, connections=None):
        """Constructor takes as the argument container of all the SELECTED
        elements or generator of that container"""
        self.positionList =positionList
        self.sizeList     =sizeList
        self.centerList   =centerList
        self.connections  =connections
    
    #other public methods
    def getPositions(self):
        for i in self.positionList:
            yield i

#    def getConnectionBends():

#--left alignment
    def alignLeft(self, setLeftCoordinate):
        # set the x position to setLeftCoordinate
        for i in range(len(self.positionList)):
            self.positionList[i] = (setLeftCoordinate, self.positionList[i][1] )
        # But preserve the Y coordinate ("sel.GetPosition()[1]")
    
    def alignMostLeft(self):
        setLeftCoordinate =min([pos[0] for pos in self.positionList])
        # now we have the most left location
        # set the x position of all selected elements to that most left one!
        for i in range(len(self.positionList)):
            self.positionList[i] = (setLeftCoordinate, self.positionList[i][1] )
        # But preserve the Y coordinate ("sel.GetPosition()[1]")
#--right alignment
    def alignRight(self, setRightCoordinate):
        # set the x position to setRightCoordinate
        for i in range(len(self.positionList)):
            self.positionList[i] = (setRightCoordinate -self.sizeList[i][0], self.positionList[i][1] )
        # But preserve the Y coordinate ("sel.GetPosition()[1]")
    
    def alignMostRight(self):
        setRightCoordinate =max([pos[0]+size[0] for (pos, size) in zip(self.positionList, self.sizeList)])
        # now we have the most right location
        # set the x position of all selected elements to that most right one!
        for i in range(len(self.positionList)):
            self.positionList[i] = (setRightCoordinate -self.sizeList[i][0], self.positionList[i][1] )
        # But preserve the Y coordinate ("sel.GetPosition()[1]")
#--horizontal center alignment
    def alignHCenter(self, setHCenterCoordinate):
        # set the x position to setRightCoordinate
        for i in range(len(self.positionList)):
            self.positionList[i] = (setHCenterCoordinate -self.sizeList[i][0]/2,
self.positionList[i][1] )
        # But preserve the Y coordinate ("sel.GetPosition()[1]")

#--top alignment
    def alignTop(self, setTopCoordinate):
        # set the y position to setTopCoordinate
        for i in range(len(self.positionList)):
            self.positionList[i] = (self.positionList[i][0], setTopCoordinate)
        # But preserve the X coordinate ("sel.GetPosition()[0]")
    
    def alignMostTop(self):
        setTopCoordinate =min([pos[1] for pos in self.positionList])
        # now we have the most top location
        # set the y position of all selected elements to that most top one!
        for i in range(len(self.positionList)):
            self.positionList[i] = (self.positionList[i][0], setTopCoordinate)
        # But preserve the X coordinate ("sel.GetPosition()[0]")
#--bottom alignment
    def alignBottom(self, setBottomCoordinate):
        # set the y position to setBottomCoordinate
        for i in range(len(self.positionList)):
            self.positionList[i] = (self.positionList[i][0], setBottomCoordinate -self.sizeList[i][1])
        # But preserve the X coordinate ("sel.GetPosition()[0]")
    
    def alignMostBottom(self):
        setBottomCoordinate =max([pos[1]+size[1] for (pos, size) in zip(self.positionList, self.sizeList)])
        # now we have the most bottom location
        # set the y position of all selected elements to that most bottom one!
        for i in range(len(self.positionList)):
            self.positionList[i] = (self.positionList[i][0], setBottomCoordinate -self.sizeList[i][1])
        # But preserve the Y coordinate ("sel.GetPosition()[1]")
#--vertical center alignment
    def alignVCenter(self, setVCenterCoordinate):
        # set the y position to setBottomCoordinate
        for i in range(len(self.positionList)):
            self.positionList[i] = (self.positionList[i][0], setVCenterCoordinate
-self.sizeList[i][1]/2)
        # But preserve the X coordinate ("sel.GetPosition()[0]")

#--Tidy
#    def Tidy(self):
        # set the y position to setBottomCoordinate
