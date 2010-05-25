# -*- coding: utf-8 -*-

from heapq import heappop, heappush, heapify
from math import sqrt
from time import time
import copy

"""
The module for complete tidy of the diagram
"""

"""
The exceptions possiblly returned by this module.
They represent some graph theory conditions under which the computation cannot
#be performed
"""
class GraphError(Exception):
    """
    The general error of the graph visualization module
    """
    def __init__(self):
        self.value = ""
    def __str__(self):
        return repr(self.value)

class CyclicHierarchyError(GraphError):
    """
    Error signaling the cycle in the hierarchization relations
    """
    def __init__(self):
        self.value = "The hierarchization process encountered cycle!"


"""
The core mathematic class for graphs
This class DO NOT treat the multiple or reflexive connections!
"""

class CTidyMath(object):
    
    #constructor
    def __init__(self, positionList, sizeList, connections=None, hierarchyConnections =None, centerList=None, direction=None):
        """
        Constructor

        @param positionList: container/generator with DEFINED order of positions of elements
        @type  positionList: container/generator of tuples

        @param sizeList: container/generator with DEFINED order of sizes of elements
        @type  sizeList: container/generator of tuples

        @param connections: set of ALL UNORIENTED edges/connections; In the tuple needs to be indices of the incident vertices; at that appropriate indices need to be positions +sizes of the vertices; the lower index first.
        @type  connections: container/generator of tuples

        @param hierarchyConnections: set of ORIENTED edges making the hierarchy; In the tuple needs to be indices of the incident vertices
        @type  hierarchyConnections: container/generator of tuples

        @param centerList: container/generator with DEFINED order of centers of elements
        @type  centerList: container/generator of tuples
        """
        self.positionList =[] #here MUST be the iterable
        self.sizeList     =sizeList
        self.connections  =set(map(lambda x: tuple(x), connections)) if connections else set()
        self.hConnections  =[]
        self.setOfHierarchization =set()
        self.setOfOhers =set(range(len(self.sizeList)))
        self.idealDistances =None
        self.vertexNeighbours =None
        self.direction = direction
        if not centerList: #compute
            self.centerList   =[[i[0]+j[0]/2,i[1]+j[1]/2] for i,j in zip(positionList, sizeList)]
        else:
            self.centerList =centerList
            if not self.positionList:
                self.positionList =[]
                for i,j in zip(self.centerList, self.sizeList):
                    self.positionList.append( (i[0]-j[0]/2, i[1]-j[1]/2) )
        if positionList:
            self.positionList =positionList
        if hierarchyConnections:
            if self.direction in ['down', 'right']:
                self.hConnections  =set(map(lambda x: tuple(x[::-1]), hierarchyConnections))
                self.direction = 'up' if self.direction == 'down' else 'left'
            else:
                self.hConnections  =set(map(lambda x: tuple(x), hierarchyConnections))
            self.setOfHierarchization =set()
            for i in self.hConnections:
                self.setOfHierarchization.add(i[0])
                self.setOfHierarchization.add(i[1])
            self.setOfOhers =self.setOfOhers.difference(self.setOfHierarchization)
        #print "Debug init", self.positionList, self.sizeList, self.connections, self.hConnections, self.setOfHierarchization, self.setOfOhers
    
    #other public methods
    def GetSizes(self):
        """ 
        Returns the generator of the element sizes
        
        @return: generator of sizes of elements
        @rtype:  generator of tuples
        """
        for i in self.sizeList:
            yield i

    def GetPositions(self):
        """ 
        Returns the generator of the element positions
        
        @return: generator of positions of elements
        @rtype:  generator of tuples
        """
        for i in self.positionList:
            yield i

    def GetCenters(self):
        """ 
        Returns the generator of the element centers
        
        @return: generator of centers of elements
        @rtype:  generator of tuples
        """
        for i in self.centerList:
            yield i

    def GetMostLeftCoordinate(self):
        """ 
        Returns the actual most left coordinate of elements
        
        @return: actual most left coordinate of the elements
        @rtype:  int
        """
        return min([i[0] for i in self.positionList])

    def GetMostTopCoordinate(self):
        """ 
        Returns the actual most top coordinate of elements
        
        @return: actual most top coordinate of the elements
        @rtype:  int
        """
        return min([i[1] for i in self.positionList])
        
    def GetMostRightCoordinate(self):
        """ 
        Returns the actual most right coordinate of elements
        
        @return: actual most right coordinate of the elements
        @rtype:  int
        """
        return max([i[0]+j[0] for (i,j) in zip(self.positionList, self.sizeList)])
        
    def TranslateToTheCoordinate(self, mostLeftTop): #works OK
        """ 
        Translate all the elements so that the most left and top coordinate is "mostLeftTop"
        
        @param positionList: new most left-top coordinate of the system of elements
        @type  positionList: tuple
        
        @return: most right-top coordinate of the system of elements
        @rtype:  tuple of int
        """
        deltaH =mostLeftTop[0] -self.GetMostLeftCoordinate()
        deltaV =mostLeftTop[1] -self.GetMostTopCoordinate()
        for i in range(len(self.positionList)):
            tmp =self.positionList[i]
            self.positionList[i] =[tmp[0]+deltaH, tmp[1]+deltaV]
        for i in range(len(self.centerList)):
            tmp =self.centerList[i]
            self.centerList[i] =[tmp[0]+deltaH, tmp[1]+deltaV]
        return (mostLeftTop[0] +self.GetMostRightCoordinate() -self.GetMostLeftCoordinate(), mostLeftTop[1])

#--left alignment
    def AlignLeft(self, setLeftCoordinate):
        """
        Align the elements left, so that they have the same most left coordinate
        
        @param positionList: new most left coordinate of elements
        @type  positionList: int
        """
        # set the x position to setLeftCoordinate
        for i in range(len(self.positionList)):
            self.positionList[i] = (setLeftCoordinate, self.positionList[i][1] )
        # But preserve the Y coordinate ("sel.GetPosition()[1]")
    
    def AlignMostLeft(self):
        """
        Align the elements most left, so that they have the same left coordinate as the previous most left one
        """
        setLeftCoordinate =min([pos[0] for pos in self.positionList])
        # now we have the most left location
        # set the x position of all selected elements to that most left one!
        for i in range(len(self.positionList)):
            self.positionList[i] = (setLeftCoordinate, self.positionList[i][1] )
        # But preserve the Y coordinate ("sel.GetPosition()[1]")
#--right alignment
    def AlignRight(self, setRightCoordinate):
        """
        Align the elements right, so that they have the same most right coordinate
        
        @param positionList: new most right coordinate of elements
        @type  positionList: int
        """
        # set the x position to setRightCoordinate
        for i in range(len(self.positionList)):
            self.positionList[i] = (setRightCoordinate -self.sizeList[i][0], self.positionList[i][1] )
        # But preserve the Y coordinate ("sel.GetPosition()[1]")
    
    def AlignMostRight(self):
        """
        Align the elements most right, so that they have the same right coordinate as the previous most right one
        """
        setRightCoordinate =max([pos[0]+size[0] for (pos, size) in zip(self.positionList, self.sizeList)])
        # now we have the most right location
        # set the x position of all selected elements to that most right one!
        for i in range(len(self.positionList)):
            self.positionList[i] = (setRightCoordinate -self.sizeList[i][0], self.positionList[i][1] )
        # But preserve the Y coordinate ("sel.GetPosition()[1]")
#--horizontal center alignment
    def AlignHCenter(self, setHCenterCoordinate):
        """
        Align the centers of elements horizontally, so that they have the same vertical center coordinate
        
        @param positionList: new vertical center coordinate of elements
        @type  positionList: int
        """
        # set the x position to setRightCoordinate
        for i in range(len(self.positionList)):
            self.positionList[i] = (setHCenterCoordinate -self.sizeList[i][0]/2,
self.positionList[i][1] )
        # But preserve the Y coordinate ("sel.GetPosition()[1]")

#--top alignment
    def AlignTop(self, setTopCoordinate):
        """
        Align the elements top, so that they have the same most top coordinate
        
        @param positionList: new most top coordinate of elements
        @type  positionList: int
        """
        # set the y position to setTopCoordinate
        for i in range(len(self.positionList)):
            self.positionList[i] = (self.positionList[i][0], setTopCoordinate)
        # But preserve the X coordinate ("sel.GetPosition()[0]")
    
    def AlignMostTop(self):
        """
        Align the elements most top, so that they have the same top coordinate as the previous most top one
        """
        setTopCoordinate =min([pos[1] for pos in self.positionList])
        # now we have the most top location
        # set the y position of all selected elements to that most top one!
        for i in range(len(self.positionList)):
            self.positionList[i] = (self.positionList[i][0], setTopCoordinate)
        # But preserve the X coordinate ("sel.GetPosition()[0]")
#--bottom alignment
    def AlignBottom(self, setBottomCoordinate):
        """
        Align the elements bottom, so that they have the same most bottom coordinate
        
        @param positionList: new most bottom coordinate of elements
        @type  positionList: int
        """
        # set the y position to setBottomCoordinate
        for i in range(len(self.positionList)):
            self.positionList[i] = (self.positionList[i][0], setBottomCoordinate -self.sizeList[i][1])
        # But preserve the X coordinate ("sel.GetPosition()[0]")
    
    def AlignMostBottom(self):
        """
        Align the elements most bottom, so that they have the same bottom coordinate as the previous most bottom one
        """
        setBottomCoordinate =max([pos[1]+size[1] for (pos, size) in zip(self.positionList, self.sizeList)])
        # now we have the most bottom location
        # set the y position of all selected elements to that most bottom one!
        for i in range(len(self.positionList)):
            self.positionList[i] = (self.positionList[i][0], setBottomCoordinate -self.sizeList[i][1])
        # But preserve the Y coordinate ("sel.GetPosition()[1]")
#--vertical center alignment
    def AlignVCenter(self, setVCenterCoordinate):
        """
        Align the centers of elements vertically, so that they have the same horizontal center coordinate
        
        @param positionList: new horizontal center coordinate of elements
        @type  positionList: int
        """
        # set the y position to setBottomCoordinate
        for i in range(len(self.positionList)):
            self.positionList[i] = (self.positionList[i][0], setVCenterCoordinate
-self.sizeList[i][1]/2)
        # But preserve the X coordinate ("sel.GetPosition()[0]")

#--Tidy------------------------------------------
    def Tidy(self):
        """
        Method to perform the complex tidy
        """
        # set the y position to setBottomCoordinate
        components =self.__DivideToComponents__()
        #now process the individual components +GIVE THEM THE MAX_TIME
        for i in components:
            i[1].__Hierarchization__()
            #now start the computation; the time divide by the number of vertices
            i[1].__StressMajorization__(time()+7.*len(self.centerList)/len(i[0]))
        #apply the computations on the continuous components
        self.__ApplyComponents__(components)

    def __DivideToComponents__(self): #works
        """
        This method divides the input graph into the separate components
        
        @return: components with thier back mappings 
        @rtype:  list of tuples (1st in tuple map; 2nd CTidyMath instance with one component)
        """
        allNodes =set(range(len(self.centerList )))
        allConnections =set(self.connections)
        allHierarchization =set(map(lambda x: tuple(x), self.hConnections))
        components =[]
        while len(allNodes):
            #workConnections =[]
            mapIndex        =[]
            comSizeList     =[]
            comCenterList   =[]
            comConnections  =set()
            comHConnections =set()
            initNode =allNodes.pop()
            stack =[ (initNode,0) ]
            mapIndex.append(initNode)
            comSizeList.append(self.sizeList[initNode])
            comCenterList.append(self.centerList[initNode])
            while stack:
                #take the node from stack and...
                processNode, orderNode =stack.pop(0)
                #...find him his neighbours
                for i in allConnections: #for all edges from the node
                    if processNode == i[0]:
                        if i[1] in allNodes:
                            stack.append( (i[1], len(mapIndex)) )
                            # 1. chceck if there's the edges and add them
                            edge =(orderNode, len(mapIndex))
                            comConnections.add( edge) #NEED to preserve the order
                            if tuple(i) in allHierarchization:
                                comHConnections.add(edge)
                                allHierarchization.discard(tuple(i))
                            if tuple(i)[::-1] in allHierarchization:
                                comHConnections.add(edge[::-1])
                                allHierarchization.discard( tuple(i)[::-1] )
                            # 2 . add the vertex +it's properties
                            mapIndex.append( i[1])
                            comSizeList.append( self.sizeList[ i[1]])
                            comCenterList.append(self.centerList[ i[1]])
                            #allConnections.discard(i) #optimization?         
                            allNodes.discard(i[1])
                            #if tuple(i) in allHierarchization:
                                #comHConnections.add(tuple(i))
                                #allHierarchization.discard(tuple(i))
                            #if tuple(i[::-1]) in allHierarchization:
                                #comHConnections.add(tuple(i[::-1]))
                                #allHierarchization.discard(tuple(i[::-1]))
                        else: #only add 
                            edge =(orderNode, mapIndex.index(i[1]))
                            comConnections.add( edge) #NEED to preserve the order
                            if tuple(i) in allHierarchization:
                                comHConnections.add(edge)
                                allHierarchization.discard(tuple(i))
                            if tuple(i)[::-1] in allHierarchization:
                                comHConnections.add(edge[::-1])
                                allHierarchization.discard( tuple(i)[::-1] )
                    elif processNode == i[1]:
                        if i[0] in allNodes:
                            stack.append( (i[0], len(mapIndex)) )
                            # 1. chceck if there's the edges and add them
                            edge =(len(mapIndex), orderNode)
                            comConnections.add( edge) #NEED to preserve the order
                            if tuple(i) in allHierarchization:
                                comHConnections.add( edge)
                                allHierarchization.discard(tuple(i))
                            if tuple(i[::-1]) in allHierarchization:
                                comHConnections.add( edge[::-1])
                                allHierarchization.discard(tuple(i[::-1]))
                            # 2 . add the vertex +it's properties
                            mapIndex.append( i[0])
                            comSizeList.append( self.sizeList[ i[0]])
                            comCenterList.append(self.centerList[ i[0]])
                            #allConnections.discard(i) #optimization?                       
                            allNodes.discard(i[0])
                        else: #only add
                            edge =(mapIndex.index(i[0]), orderNode)
                            comConnections.add( edge) #NEED to preserve the order
                            if tuple(i) in allHierarchization:
                                comHConnections.add( edge)
                                allHierarchization.discard(tuple(i))
                            if tuple(i[::-1]) in allHierarchization:
                                comHConnections.add( edge[::-1])
                                allHierarchization.discard(tuple(i[::-1]))
                                
                allConnections.difference_update(comConnections) #optimization of computation of others components
                allHierarchization.difference_update(comHConnections)
                
            #do not give positions of elements, but their centers
            #print "mapIndex, comSizeList, comConnections, comHConnections, comCenterList", mapIndex, comSizeList, comConnections, comHConnections, comCenterList
            components.append((mapIndex,
            CTidyMath(None, comSizeList, comConnections, comHConnections, comCenterList, self.direction) ))
        
        return components
        #TODO pridaj Time division 
        
        
    def __ApplyComponents__(self, listToApply):
        """
        This method applies the layout performed on the components back to original CTidyMath instance
        
        @param components with thier back mappings 
        @type  list of tuples (1st in tuple map; 2nd CTidyMath instance with one component)
        """
        mostLeftTop=(0,0)
        for i in listToApply:
            #take the separated elements side-by-side
            mostLeftTop =i[1].TranslateToTheCoordinate(mostLeftTop)
            mostLeftTop =( mostLeftTop[0]+40, 0)
            #apply the positions to the global layout
            for k,l in zip(i[0], i[1].GetPositions()):
                self.positionList[k] =l #set the internal variables of Tidy obj by this values
                # Position or centers???
                
        #print "a.getCenters()",   list(a.getCenters())
        #print "a.getPositions()", list(a.getPositions())
    
    def __Hierarchization__(self): #works
        """
        This method compute the vertical positions/floors of components for the
        nodes involved in hierarchization connections/edges
        
        @raise CyclicHierarchyError
        """
        if not self.hConnections:
            return #nothing to do
        
        #print self.positionList, self.sizeList, self.connections, self.hConnections, self.setOfHierarchization, self.setOfOhers,
        
        #compute the primal parents (parents without parents)
        levels =dict(map(lambda x: (x,0), self.setOfHierarchization))
        #print "levels", levels, "self.setOfHierarchization", self.setOfHierarchization
        for i in self.hConnections:
            levels[i[1]] =1
        #print "levels", levels
        queue =[] #the priority queue
        for i in self.setOfHierarchization:
            if not levels[i]:
                queue.append((0,i)) #we add here all the primal parents with their levels
        #print "queue", queue
        heapify(queue)
        if not queue:
            raise CyclicHierarchyError()
        while queue:
            priority, node =heappop(queue)
            for i in self.hConnections:
                if i[0] ==node:
                    heappush(queue, (priority-1, i[1]))
                    levels[i[1]] =min(priority-1, levels[i[1]])
            if priority < -len(self.setOfHierarchization):
                raise CyclicHierarchyError()
            #print "queue", queue
            #print "levels", levels
        #print "levels", levels
        #now assign the y coordinate according to the floor
        #WARNING! THE FLOOR IS **ALWAYS* NEGATIVE!
        pairs =levels.items()
        
        pairs.sort(lambda x,y: cmp(x[1], y[1]), reverse =(self.direction in ['up','left']))
        
        #print "pairs", pairs
        floorHeight =[0]*len(self.centerList)
        if self.direction in ['up','down']: #for vertical hierarchy
            for i in pairs:
                floorHeight[ - i[1]] =max(self.sizeList[i[0]][1], floorHeight[ - i[1]])
            #print "floorHeight", floorHeight
            floor =pairs[0][1]
            cumulativeFloorHeight =floorHeight[-floor]/2
            for i in pairs:
                if not i[1] ==floor:
                    if self.direction == 'up':
                        cumulativeFloorHeight +=(floorHeight[-floor] +floorHeight[-floor +1])/2 +40
                    else:
                        cumulativeFloorHeight +=(floorHeight[-floor] +floorHeight[-floor -1])/2 +40
                    floor = i[1]
                self.centerList[ i[0]][1] =cumulativeFloorHeight
        else: #for horizontal hierarchy
            for i in pairs:
                floorHeight[ - i[1]] =max(self.sizeList[i[0]][0], floorHeight[ - i[1]])
            #print "floorHeight", floorHeight
            floor =pairs[0][1]
            cumulativeFloorHeight =floorHeight[-floor]/2
            for i in pairs:
                if not i[1] ==floor:
                    if self.direction == 'left':
                        cumulativeFloorHeight +=(floorHeight[-floor] +floorHeight[-floor +1])/2 +40
                    else:
                        cumulativeFloorHeight +=(floorHeight[-floor] +floorHeight[-floor -1])/2 +40
                    floor = i[1]
                self.centerList[ i[0]][0] =cumulativeFloorHeight
        #additional precomputing of the posList.
        self.positionList =[]
        for i,j in zip(self.centerList, self.sizeList):
            self.positionList.append( (i[0]-j[0]/2, i[1]-j[1]/2) )
        return

    
    def ComputeVertexNeighbours(self): #works OK
        """
        Acquire the set of vertices incident to each one vertex
        """
        self.vertexNeighbours =[set() for i in range(len(self.centerList))]
        for i in self.connections:
            self.vertexNeighbours[i[0]].add(i[1])
            self.vertexNeighbours[i[1]].add(i[0])
    
    def ComputeIdealDistances(self): #works ????
        """
        Method to compute the ideal distances between each two vertices for starting of the Stress Majorization
        """
        if not self.vertexNeighbours:
            self.ComputeVertexNeighbours()
        elements =len(self.centerList)
        self.idealDistances =[ [100000 for i in range(elements)] for i in range(elements)]
        for i,j in enumerate(self.sizeList):
            for k,l in enumerate(self.sizeList):
                if (i,k) in self.connections:
                    self.idealDistances[i][k] =self.idealDistances[k][i] =  len(self.vertexNeighbours[i].symmetric_difference(self.vertexNeighbours[k]))                     *(sqrt(j[0]**2 +j[1]**2) +sqrt(l[0]**2 +l[1]**2))/2
        for i in range(elements):
            self.idealDistances[i][i] =0.
        #now use Floyd algorithm
        for i in range(elements):
            for j in range(elements):
                for k in range(elements):
                    if self.idealDistances[i][k] +self.idealDistances[k][j] <self.idealDistances[i][j]:
                        self.idealDistances[i][j] =self.idealDistances[i][k] +self.idealDistances[k][j]
        for i,j in enumerate(self.sizeList):
            for k,l in enumerate(self.sizeList):
                if (i,k) in self.connections:
                    self.idealDistances[i][k] =self.idealDistances[k][i] =  len(self.vertexNeighbours[i].symmetric_difference(self.vertexNeighbours[k]))                     *(sqrt(j[0]**2 +j[1]**2) +sqrt(l[0]**2 +l[1]**2))/2    
    
    def ComputeTotalEnergy(self): #works ????
        """
        Method to compute the total energy/stress in the system
        """
        if not self.idealDistances:
            self.ComputeIdealDistances()
        elements =len(self.sizeList)
        totalEnergy =0.
        for i,j in enumerate(self.centerList):
            for k,l in enumerate(self.centerList[i+1:]):
                idDist =self.idealDistances[i][k+i+1]
                realDist =sqrt((j[0]-l[0])**2 +(j[1]-l[1])**2)
                totalEnergy +=(realDist/idDist-1)**2
        return totalEnergy
    
    def __StressMajorization__(self, timeMax=None):
        """
        The main tidy method -it computes the new distribution of vertices
        through the Stress Majorization method http://www.research.att.com/areas/
        visualization/papers_videos/abstract.php?id=DBLP-conf-gd-GansnerKN04
        
        @param optional time limit; after this limit no iteration will be started
        @type  float
        """
        if len(self.centerList)<2:
            return #nothing to do
                
        #begin the comupting
        if not self.idealDistances:
            self.ComputeIdealDistances()
        
        totalEnergyOrig =self.ComputeTotalEnergy()
        totalEnergyAfter =totalEnergyOrig/1.00101
        #remove one random element --> to fix the whole structure by him.
        const =[]
        for i in range(len(self.idealDistances)):
            tmp =0.
            for j in range(len(self.idealDistances)):
                if not i == j:
                    tmp += self.idealDistances[i][j]**-2
            const.append(tmp)
        #print "__StressMajorization__", totalEnergyOrig/totalEnergyAfter

        while totalEnergyOrig/totalEnergyAfter >1.0000001:
            #now -compute one iteration of common vertices
            q=copy.deepcopy(self.centerList)
            for i in self.setOfOhers:
                posX=0.
                posY=0.
                for j,k in enumerate(self.centerList):
                    idDist =self.idealDistances[i][j]
                    if idDist<1:
                        continue
                    realDist = sqrt( (self.centerList[j][0] -self.centerList[i][0])**2
                                    +(self.centerList[j][1] -self.centerList[i][1])**2)
                    if realDist:
                        posX += (self.centerList[j][0]/idDist +(self.centerList[i][0] -self.centerList[j][0])/realDist)/idDist
                        posY += (self.centerList[j][1]/idDist +(self.centerList[i][1] -self.centerList[j][1])/realDist)/idDist
                    else:
                        posX +=self.centerList[j][0]/idDist**2
                        posY +=self.centerList[j][1]/idDist**2
                q[i] =(int(posX/const[i] ), int(posY/const[i]))
            #now -compute one iteration of hierarcized vertices
            if self.direction in ['up','down']:
                for i in self.setOfHierarchization:
                    posX=0.
                    for j,k in enumerate(self.centerList):
                        idDist =self.idealDistances[i][j]
                        if idDist<1:
                            continue
                        realDist = sqrt( (self.centerList[j][0] -self.centerList[i][0])**2
                                        +(self.centerList[j][1] -self.centerList[i][1])**2)
                        if realDist:
                            posX += (self.centerList[j][0]/idDist +(self.centerList[i][0] -self.centerList[j][0])/realDist)/idDist
                        else:
                            posX +=self.centerList[j][0]/idDist**2
                    q[i] =(int(posX/const[i]), self.centerList[i][1])
            else:
                for i in self.setOfHierarchization:
                    posY=0.
                    for j,k in enumerate(self.centerList):
                        idDist =self.idealDistances[i][j]
                        if idDist<1:
                            continue
                        realDist = sqrt( (self.centerList[j][0] -self.centerList[i][0])**2
                                        +(self.centerList[j][1] -self.centerList[i][1])**2)
                        if realDist:
                            posY += (self.centerList[j][1]/idDist +(self.centerList[i][1] -self.centerList[j][1])/realDist)/idDist
                        else:
                            posY +=self.centerList[j][1]/idDist**2
                    q[i] =(self.centerList[i][0], int(posY/const[i]))
            #swap q and self.centerList
            q, self.centerList =self.centerList, q
            #update the total energy variables
            totalEnergyOrig =totalEnergyAfter
            totalEnergyAfter =self.ComputeTotalEnergy()
            if timeMax and time() >timeMax:
                break
        #transform the results also into the position list
        self.positionList =[]
        for i,j in zip(self.centerList, self.sizeList):
            self.positionList.append( (i[0]-j[0]/2, i[1]-j[1]/2) )
        return

## the module self test section! on console
# ------------------------------------------
    def __test__(self):
        """
        Method helping testing the modules
        """
        for i in range(len(self.sizeList)):
            self.centerList[i] =self.sizeList[i]

if __name__ == '__main__': #if run from console
    a=CTidyMath([[20,10],[20,10],[20,10],[20,10]], [[30,20],[30,10],[20,10],[10,10]], [[0,1],[0,2],[2,3]], [[1,0],[2,0],[2,1],[3,2],[2,3]], None)
    #a.__Hierarchization__() #works!!
    #print list(a.getCenters())
    #print list(a.getPositions())
    print a.ComputeIdealDistances()
    #a.__StressMajorization__()
    #print a.vertexNeighbours
    print a.idealDistances
    print a.ComputeTotalEnergy()
    #a.__DivideToComponents__()
    #print list(a.getCenters())
    #print list(a.getPositions())
    # check the order of results with the header below and the test writeout
    ##def __init__(self, positionList, sizeList, connections=None, hierarchyConnections =None, centerList=None):
    ##print self.positionList, self.sizeList, self.connections, self.hConnections, self.setOfHierarchization, self.setOfOhers, self.connectionBends