# -*- coding: utf-8 -*-

from heapq import heappop, heappush, heapify
from math import sqrt
from time import time

"""
The module for complete tidy of the diagram
"""

"""
The exceptions possiblly returned by this module.
They represent some graph theory conditions under which the computation cannot
#be performed
"""
class GraphError(Exception):
    def __init__(self):
        self.value = ""
    def __str__(self):
        return repr(self.value)

class CyclicHierarchyError(GraphError):
  def __init__(self):
          self.value = "The hierarchization process encountered cycle!"


"""
The core mathematic class for graphs
This class DO NOT treat the multiple or reflexive connections!
"""

class CTidyMath(object):
    #constructor
    def __init__(self, positionList, sizeList, connections=None, hierarchyConnections =None, centerList=None):
        """Constructor takes as the argument container of all the SELECTED
        elements or generator of that container"""
        self.positionList =[] #here MUST be the iterable
        self.sizeList     =sizeList
        self.connections  =set(map(lambda x: tuple(x), connections)) if connections else set()
        self.HConnections  =[]
        self.setOfHierarchization =set()
        self.setOfOhers =set(range(len(self.sizeList)))
        self.idealDistances =None
        self.vertexNeighbours =None
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
            self.HConnections  =set(map(lambda x: tuple(x), hierarchyConnections))
            self.setOfHierarchization =set()
            for i in self.HConnections:
                self.setOfHierarchization.add(i[0])
                self.setOfHierarchization.add(i[1])
            self.setOfOhers =self.setOfOhers.difference(self.setOfHierarchization)
        print "Debug init", self.positionList, self.sizeList, self.connections, self.HConnections, self.setOfHierarchization, self.setOfOhers
    
    #other public methods
    def getSize(self):
        for i in self.sizeList:
            yield i

    def getPositions(self):
        for i in self.positionList:
            yield i

    def getCenters(self):
        for i in self.centerList:
            yield i

    def getMostLeftCoordinate(self):
        return min([i[0] for i in self.positionList])

    def getMostTopCoordinate(self):
        return min([i[1] for i in self.positionList])
        
    def getMostRightCoordinate(self):
        return max([i[0]+j[0] for (i,j) in zip(self.positionList, self.sizeList)])
        
    def translateToTheCoordinate(self, mostLeftTop): #works OK
        deltaH =mostLeftTop[0] -self.getMostLeftCoordinate()
        deltaV =mostLeftTop[1] -self.getMostTopCoordinate()
        for i in range(len(self.positionList)):
            tmp =self.positionList[i]
            self.positionList[i] =[tmp[0]+deltaH, tmp[1]+deltaV]
        for i in range(len(self.centerList)):
            tmp =self.centerList[i]
            self.centerList[i] =[tmp[0]+deltaH, tmp[1]+deltaV]
        return (mostLeftTop[0] +self.getMostRightCoordinate() -self.getMostLeftCoordinate(), mostLeftTop[1])

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

#--Tidy------------------------------------------
    def Tidy(self):
        # set the y position to setBottomCoordinate
        components =self.divideToComponents()
        #now process the individual components +GIVE THEM THE MAX_TIME
        for i in components:
            i[1].hierarchization()
            #now start the computation; the time divide by the number of vertices
            i[1].stressMajorization(7.*len(self.centerList)/len(i[0]))
        #apply the computations on the continuous components
        self.applyComponents(components)

    def divideToComponents(self): #works
        """
        This method divides the input graph into the separate components
        """
        allNodes =set(range(len(self.centerList )))
        allConnections =set(self.connections)
        allHierarchization =set(map(lambda x: tuple(x), self.HConnections))
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
            print "mapIndex, comSizeList, comConnections, comHConnections, comCenterList", mapIndex, comSizeList, comConnections, comHConnections, comCenterList
            components.append((mapIndex,
            CTidyMath(None, comSizeList, comConnections, comHConnections, comCenterList) ))
        
        return components
        #TODO pridaj Time division 
        
        
    def applyComponents(self, listToApply):
        mostLeftTop=(0,0)
        for i in listToApply:
            #take the separated elements side-by-side
            mostLeftTop =i[1].translateToTheCoordinate(mostLeftTop)
            mostLeftTop =( mostLeftTop[0]+40, 0)
            #apply the positions to the global layout
            for k,l in zip(i[0], i[1].getPositions()):
                self.positionList[k] =l #set the internal variables of Tidy obj by this values
                # Position or centers???
                
        #print "a.getCenters()",   list(a.getCenters())
        #print "a.getPositions()", list(a.getPositions())
    
    def hierarchization(self): #works
        """
        This method compute the vertical positions/floors of components for the
        nodes involved in hierarchization connections/edges
        
        @raise CyclicHierarchyError
        """
        #print "Pozdravy z hierarch "
        if not self.HConnections:
            #print "nothing in hierarchization"
            return #nothing to do
        
        #print self.positionList, self.sizeList, self.connections, self.HConnections, self.setOfHierarchization, self.setOfOhers,
        
        #compute the primal parents (parents without parents)
        levels =dict(map(lambda x: (x,0), self.setOfHierarchization))
        #print "levels", levels, "self.setOfHierarchization", self.setOfHierarchization
        for i in self.HConnections:
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
            for i in self.HConnections:
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
        pairs.sort(lambda x,y: cmp(x[1], y[1]), reverse =True)
        #print "pairs", pairs
        floorHeight =[0]*len(self.centerList)
        for i in pairs:
            floorHeight[ - i[1]] =max(self.sizeList[i[0]][1], floorHeight[ - i[1]])
        #print "floorHeight", floorHeight
        cumulativeFloorHeight =floorHeight[0]/2
        floor =0
        for i in pairs:
            if not - i[1] ==floor:
                cumulativeFloorHeight +=(floorHeight[floor] +floorHeight[floor +1])/2 +40
                floor +=1
            self.centerList[ i[0]][1] =cumulativeFloorHeight
        #additional precomputing of the posList.
        self.positionList =[]
        for i,j in zip(self.centerList, self.sizeList):
            self.positionList.append( (i[0]-j[0]/2, i[1]-j[1]/2) )
        return

    
    def computeVertexNeighbours(self): #works OK
        self.vertexNeighbours =[set() for i in range(len(self.centerList))]
        for i in self.connections:
            self.vertexNeighbours[i[0]].add(i[1])
            self.vertexNeighbours[i[1]].add(i[0])
    
    def computeIdealDistances(self): #works ????
        if not self.vertexNeighbours:
            self.computeVertexNeighbours()
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
            
    
    def computeTotalEnergy(self): #works ????
        if not self.idealDistances:
            self.computeIdealDistances()
        elements =len(self.sizeList)
        totalEnergy =0.
        for i,j in enumerate(self.centerList):
            for k,l in enumerate(self.centerList[i+1:]):
                idDist =self.idealDistances[i][k+i+1]
                realDist =sqrt((j[0]-l[0])**2 +(j[1]-l[1])**2)
                totalEnergy +=(realDist/idDist-1)**2
        return totalEnergy
    
    def stressMajorization(self, timeMax=None):
        """
        The main tidy method -it computes the new distribution of vertices
        through the Stress Majorization method http://www.research.att.com/areas/
        visualization/papers_videos/abstract.php?id=DBLP-conf-gd-GansnerKN04
        """
        if len(self.centerList)<2:
            return #nothing to do
        
        #begin the comupting
        if not self.idealDistances:
            self.computeIdealDistances()
        
        totalEnergyOrig =self.computeTotalEnergy()
        totalEnergyAfter =totalEnergyOrig/1.0004
        #if some verteces to hierarchize, DO "hierarchization"
        #if self.setOfHierarchization:
            #self.hierarchization()
        #take the nearest vertex to (0,0) coordinate to be fixed
        #elem =self.centerList[0]
        #distanceFrom00 = float(elem[0])**2 +float(elem[1])**2
        #index =0
        #for i,j in enumerate(self.centerList):
            #tmpDist =float(j[0])**2 +float(j[1])**2
            #if tmpDist <distanceFrom00:
                #index, distanceFrom00 = i, tmpDist
        try:
            fixxed =-self.setOfHierarchization.pop() #fix the "fixxed" element
        except:
            fixxed =self.setOfOhers.pop()
        #remove one random element --> to fix the whole structure by him.
        const =0.
        for i in range(len(self.idealDistances)):
            for j in range( i+1, len(self.idealDistances)):
                const += self.idealDistances[i][j]**-2
        while totalEnergyOrig/totalEnergyAfter >1.0003: #perform
            print totalEnergyOrig/totalEnergyAfter, "pomer zlepsenia"
            #now -compute one iteration of common vertices
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
                self.centerList[i] =(int(posX/const), int(posY/const))
            #now -compute one iteration of hierarcized vertices
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
                self.centerList[i] =(int(posX/const), self.centerList[i][1])
            #update the total energy variables
            totalEnergyOrig =totalEnergyAfter
            totalEnergyAfter =self.computeTotalEnergy()
            #print totalEnergyOrig, "Energia pred iteraciou", totalEnergyAfter, "Energia po iteracii" #debug
            if time() >timeMax:
                break
        if fixxed>0:
            self.setOfOhers.add(fixxed) #give back the fixxed element
        else:
            self.setOfHierarchization.add(fixxed)
        #transform the results also into the position list
        self.positionList =[]
        for i,j in zip(self.centerList, self.sizeList):
            self.positionList.append( (i[0]-j[0]/2, i[1]-j[1]/2) )
        return

## the module self test section! on console

    def test(self):
        for i in range(len(self.sizeList)):
            self.centerList[i] =self.sizeList[i]




if __name__ == '__main__':
    a=CTidyMath([[20,10],[20,10],[20,10],[20,10]], [[30,20],[30,10],[20,10],[10,10]], [[0,1],[0,2],[2,3]], [[1,0],[2,0],[2,1],[3,2],[2,3]], None)
    #a.hierarchization() #works!!
    #print list(a.getCenters())
    #print list(a.getPositions())
    print a.computeTotalEnergy()
    a.stressMajorization()
    #print a.vertexNeighbours
    print a.idealDistances
    print a.computeTotalEnergy()
    #a.divideToComponents()
    #print list(a.getCenters())
    #print list(a.getPositions())
    # check the order of results with the header below and the test writeout
    ##def __init__(self, positionList, sizeList, connections=None, hierarchyConnections =None, centerList=None):
    ##print self.positionList, self.sizeList, self.connections, self.HConnections, self.setOfHierarchization, self.setOfOhers, self.connectionBends