# -*- coding: utf-8 -*-
from lib.Math2D import CTidyMath, GraphError, CyclicHierarchyError
from lib.Drawing.VisibleObject import CVisibleObject
from math import sqrt

class CTidyWrapper(object):
    """The class to wrap methods for Element Alignment &Tidy
    This class uses interface of CVisibleObject +CDiagram +CDiagcramType to abstract
    the core graph tiding class from all of the UML.FRI logic. This core graph
    tidy class (CTidyMath) is PURE Python implementation of mathematical algorithms
    described in documentation.
    """
    
    #def __init__(self, positionList, sizeList, connections=None, hierarchyConnections =None, centerList=None)

    #constructor
    def __init__(self, setOfSelectedElements, diagram, connections=None):
        """Constructor takes as the argument container of all the SELECTED
        elements or generator of that container,
        
        @param container/generator of elements to be aligned
        @type  generator of tuples
        
        @param components with thier back mappings 
        @type  list of tuples (1st in tuple map; 2nd CTidyMath instance with one component)
        
        @param components with thier back mappings 
        @type  list of tuples (1st in tuple map; 2nd CTidyMath instance with one component)
        
        """
        self.elementList =list(setOfSelectedElements)
        self.diagram      =diagram
        #make internal 
        self.positionList =[elem.GetPosition()      for elem in self.elementList]
        self.sizeList     =[elem.GetSize(diagram)   for elem in self.elementList]
        self.hierarchization =None
        self.connections     =None #the container of all the nonreflex. single connections
        self.connectionsObj  =None #the list of all real connections
        self.direction       =None
        if connections: #works??
            #need to separate reflexive or multiple connections
            self.connections  =set()
            self.hierarchization =set()
            self.connectionsObj  =list(connections)
            
            hierarchizationType =diagram.GetType().GetHierarchization()
            self.direction      =diagram.GetType().GetDirection()
            
            for i in self.connectionsObj:
                try:
                    s=self.elementList.index( i.GetSource())
                    d=self.elementList.index( i.GetDestination())
                    if   s<d:
                        self.connections.add((s,d))
                    elif s>d:
                        self.connections.add((d,s))
                    if hierarchizationType and i.GetObject().GetType().GetId() ==hierarchizationType:
                        self.hierarchization.add( (s,d) )
                except:
                    pass
        #debug
        #print self.positionList, self.sizeList, self.connections, self.hierarchization    
        self.tidy =CTidyMath(self.positionList, self.sizeList, self.connections, self.hierarchization, direction =self.direction)


#def __init__(self, positionList, sizeList, connections=None, hierarchyConnections =None, centerList=None)
    
    def applyState(self): #works OK
        """Applies the new positions of elements"""
        self.positionList =self.tidy.getPositions()
        for (elem, pos) in zip(self.elementList, self.positionList):
            elem.SetPosition( pos )
        if self.connectionsObj: #if called operation changing connection bends
            conNo =[[0 for i in range(len(self.elementList))] for i in range(len(self.elementList))]
            for con in self.connectionsObj:
                try:
                    #set the lines to be straight
                    con.RemoveAllPoints(self, self.diagram)
                    #Add the treatment of the multiple +refl. connections
                    sCen =con.GetSource().GetCenter(self.diagram)
                    dCen =con.GetDestination().GetCenter(self.diagram)
                    sSiz =con.GetSource().GetSize(self.diagram)
                    dSiz =con.GetDestination().GetSize(self.diagram)
                    sInd =self.elementList.index( con.GetSource() )
                    dInd =self.elementList.index( con.GetDestination() )
                    
                    if sInd == dInd: #reflexive connection -->done in connection implementation
                        continue
                    #now treat the non-reflexive conn.; treat the multiConn.
                    deltaX =dCen[0] -sCen[0]
                    deltaY =dCen[1] -sCen[1]
                    deltaLen =int(sqrt(deltaX**2 +deltaY**2))
                    
                    con.AddPoint( (sCen[0] +deltaX/2 -10*conNo[dInd][sInd]*deltaY/deltaLen,
                                   sCen[1] +deltaY/2 +10*conNo[dInd][sInd]*deltaX/deltaLen) )
                    
                    conNo[dInd][sInd] +=1
                    conNo[sInd][dInd] =conNo[dInd][sInd]
                except:
                    pass
    
    #other public methods
#--left alignment
    def alignLeft(self, clickedElem):
        """
        Call left alignment method from CTidyMath
        The left coordinate of the 'clickedElem' will be set as the left for all
        the selected elements
        
        @param element to be aligned after
        @type  CVisibleObject
        """
        if not isinstance(clickedElem, CVisibleObject):
            return #nothing to do
        # set the x position to setLeftCoordinate
        self.tidy.alignLeft( clickedElem.GetPosition()[0] )
        
    
    def alignMostLeft(self):
        """
        Call most left alignment method from CTidyMath
        The left coordinate of the the selected elements will be set by the most
        left one
        """
        self.tidy.alignMostLeft( )
        

#--right alignment
    def alignRight(self, clickedElem):
        """
        Call right alignment method from CTidyMath
        The right coordinate of the 'clickedElem' will be set as the right for all
        the selected elements
        
        @param element to be aligned after
        @type  CVisibleObject
        """
        if not isinstance(clickedElem, CVisibleObject):
            return #nothing to do
        # set the x position to setLeftCoordinate
        self.tidy.alignRight( clickedElem.GetPosition()[0] +clickedElem.GetSize(self.diagram)[0] )
        
    
    def alignMostRight(self):
        """
        Call most right alignment method from CTidyMath
        The right coordinate of the the selected elements will be set by the most
        right one
        """
        self.tidy.alignMostRight( )
        

#--horizontal center alignment
    def alignHCenter(self, clickedElem):
        """
        Call horizontal center alignment method from CTidyMath
        The horizontal center coordinate of the 'clickedElem' will be set as the
        horizontal center for all the selected elements
        
        @param element to be aligned after
        @type  CVisibleObject
        """
        if not isinstance(clickedElem, CVisibleObject):
            return #nothing to do
        # set the x position to setLeftCoordinate
        self.tidy.alignHCenter( clickedElem.GetPosition()[0]
+clickedElem.GetSize(self.diagram)[0]/2 )
        

#--top alignment
    def alignTop(self, clickedElem):
        """
        Call top alignment method from CTidyMath
        The top coordinate of the 'clickedElem' will be set as the top for all
        the selected elements
        
        @param element to be aligned after
        @type  CVisibleObject
        """
        if not isinstance(clickedElem, CVisibleObject):
            return #nothing to do
        # set the y position to settopCoordinate
        self.tidy.alignTop( clickedElem.GetPosition()[1] )
        
    def alignMostTop(self):
        """
        Call most top alignment method from CTidyMath
        The top coordinate of the the selected elements will be set by the most
        top one
        """
        self.tidy.alignMostTop( )
        

#--bottom alignment
    def alignBottom(self, clickedElem):
        """
        Call bottom alignment method from CTidyMath
        The bottom coordinate of the 'clickedElem' will be set as the bottom for all
        the selected elements
        
        @param element to be aligned after
        @type  CVisibleObject
        """
        if not isinstance(clickedElem, CVisibleObject):
            return #nothing to do
        # set the y position to setTopCoordinate
        self.tidy.alignBottom( clickedElem.GetPosition()[1] +clickedElem.GetSize(self.diagram)[1] )
        
    
    def alignMostBottom(self):
        """
        Call most bottom alignment method from CTidyMath
        The bottom coordinate of the the selected elements will be set by the most
        bottom one
        """
        self.tidy.alignMostBottom( )
        

#--vertical center alignment
    def alignVCenter(self, clickedElem):
        """
        Call vertical center alignment method from CTidyMath
        The vertical center coordinate of the 'clickedElem' will be set as the
        vertical center for all the selected elements
        
        @param element to be aligned after
        @type  CVisibleObject
        """
        if not isinstance(clickedElem, CVisibleObject):
            return #nothing to do
        # set the y position to setTopCoordinate
        self.tidy.alignVCenter( clickedElem.GetPosition()[1] +clickedElem.GetSize(self.diagram)[1]/2 )
        

#--Tidy
  #This is Tidy calling function.
    def Tidy(self):
        """
        This method calls the Tidy function in CTidyMath. It separetes the pure
        mathematical parts. It does me
        """
        # set the x position to setLeftCoordinate
        try:
            self.tidy.Tidy()
        except GraphError:
            #print "Vyskytla sa cyklicka dedicnost" #debug
            pass











