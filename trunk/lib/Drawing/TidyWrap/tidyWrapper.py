# -*- coding: utf-8 -*-
from lib.Math2D import CTidyMath
from lib.Drawing.VisibleObject import CVisibleObject
"""The class to wrap methods for Element Alignment &Tidy
This class uses interface of CVisibleObject to abstract the core graph tiding
class from all of the program logic. This core graph tiding class (CTidyMath)
is PURE Python implementation of mathematical algorithms described in
documentation.
"""

class CTidyWrapper(object):

    #constructor
    def __init__(self, setOfSelectedElements, diagram, connections=None):
        """Constructor takes as the argument container of all the SELECTED
        elements or generator of that container"""
        self.elementTuple =tuple(setOfSelectedElements)
        self.connections  =connections
        self.diagram      =diagram
        #make internal 
        self.positionList =[elem.GetPosition()      for elem in self.elementTuple]
        self.sizeList     =[elem.GetSize(diagram)   for elem in self.elementTuple]
        if connections:
            self.centerList =[elem.GetCenter(diagram) for elem in self.elementTuple]
        else:
            self.centerList =None
        self.tidy =CTidyMath(self.positionList, self.sizeList, self.centerList, self.connections)

    def applyState(self):
        """Applies the new positions of elements"""
        self.positionList =self.tidy.getPositions()
        for (elem, pos) in zip(self.elementTuple, self.positionList):
            elem.SetPosition( pos )
        if self.connections: #if called operation changing connection bends
            connection =self.tidy.getConnectionBends()
            for con in self.connections:
                con.RemoveAllPoint(self, self.diagram)
            for (elem, pos) in zip(self.elementTuple, self.positionList):
                elem.SetPosition( pos )
            ### TODO add the tidy of connection bend points
                
    #other public methods
#--left alignment
    def alignLeft(self, clickedElem):
        if not isinstance(clickedElem, CVisibleObject):
            return #nothing to do
        # set the x position to setLeftCoordinate
        self.tidy.alignLeft( clickedElem.GetPosition()[0] )
        self.positionList =self.tidy.getPositions()
    
    def alignMostLeft(self):
        self.tidy.alignMostLeft( )
        self.positionList =self.tidy.getPositions()

#--right alignment
    def alignRight(self, clickedElem):
        if not isinstance(clickedElem, CVisibleObject):
            return #nothing to do
        # set the x position to setLeftCoordinate
        self.tidy.alignRight( clickedElem.GetPosition()[0] +clickedElem.GetSize(self.diagram)[0] )
        self.positionList =self.tidy.getPositions()
    
    def alignMostRight(self):
        self.tidy.alignMostRight( )
        self.positionList =self.tidy.getPositions()

#--horizontal center alignment
    def alignHCenter(self, clickedElem):
        if not isinstance(clickedElem, CVisibleObject):
            return #nothing to do
        # set the x position to setLeftCoordinate
        self.tidy.alignHCenter( clickedElem.GetPosition()[0]
+clickedElem.GetSize(self.diagram)[0]/2 )
        self.positionList =self.tidy.getPositions()

#--top alignment
    def alignTop(self, clickedElem):
        if not isinstance(clickedElem, CVisibleObject):
            return #nothing to do
        # set the y position to settopCoordinate
        self.tidy.alignTop( clickedElem.GetPosition()[1] )
        self.positionList =self.tidy.getPositions()
    
    def alignMostTop(self):
        self.tidy.alignMostTop( )
        self.positionList =self.tidy.getPositions()

#--bottom alignment
    def alignBottom(self, clickedElem):
        if not isinstance(clickedElem, CVisibleObject):
            return #nothing to do
        # set the y position to setTopCoordinate
        self.tidy.alignBottom( clickedElem.GetPosition()[1] +clickedElem.GetSize(self.diagram)[1] )
        self.positionList =self.tidy.getPositions()
    
    def alignMostBottom(self):
        self.tidy.alignMostBottom( )
        self.positionList =self.tidy.getPositions()

#--vertical center alignment
    def alignVCenter(self, clickedElem):
        if not isinstance(clickedElem, CVisibleObject):
            return #nothing to do
        # set the y position to setTopCoordinate
        self.tidy.alignVCenter( clickedElem.GetPosition()[1] +clickedElem.GetSize(self.diagram)[1]/2 )
        self.positionList =self.tidy.getPositions()


#--Tidy
#    def Tidy(self, clickedElem):
        ##if the class badly constructed (without connections)
        #if connections ==None:
            #return
        ##if no connections =nothing to do. TODO is it OK?
        #if connections ==[]:
            #return
        ## set the x position to setLeftCoordinate
        #self.tidy.Tidy()
        #self.positionList =self.tidy.getPositions()
