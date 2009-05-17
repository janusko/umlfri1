#!/usr/bin/python

from lib.Plugin.Client.Interface import CInterface
from lib.Exceptions import *
import random

inf = float('inf')

class Node(object):
        
    def __init__(self, ref):
        self.ref = ref
        self.prev = []
        self.next = []
        self.decprev = 0
        self.idx = -1
        self.time = [[-inf, -inf], [inf, inf]]
    
    def AddPrev(self, con, node):
        self.prev.append((con, node))
    
    def AddNext(self, con, node):
        self.next.append((con, node))
    
    def DecPrev(self):
        self.decprev += 1
    
    def SumPrev(self):
        return len(self.prev) - self.decprev
    
    def SetIdx(self, idx):
        self.idx = idx
    
    def NextHops(self):
        for con, node in self.next:
            yield node
    
    def SendNext(self):
        for c, n in self.next:
            n.RecvPrev(self.time[0][1])
    
    def RecvNext(self, time):
        if self.time[1][1] > time and time > -inf:
            self.time[1][1] = time
            self.time[1][0] = time - self.Duration()
    
    def SendPrev(self):
        for c, n in self.prev:
            n.RecvNext(self.time[1][0])
    
    def RecvPrev(self, time):
        if self.time[0][0] < time:
            self.time[0][0] = time
            self.time[0][1] = time + self.Duration()
        if self.time[0][0] > self.time[1][0]:
            self.time[1][0] = self.time[0][0]
            self.time[1][1] = self.time[0][1]
        
    

class Condition(Node):
    
    def __init__(self, ref):
        Node.__init__(self, ref)
        self.name = ref.GetObject().GetValue('condition')
        self.neg = ref.GetObject().GetValue('negate') == 'True'
    
    def SetConditions(self, cond):
        self.val = cond[self.name] ^ self.neg
    
    def Duration(self):
        if self.val:
            return 0
        else:
            return -inf
    
    def IsCritical(self):
        return self.time[0][1] == self.time[1][1] > -inf and self.val
    
class Activity(Node):
    
    def __init__(self, ref):
        Node.__init__(self, ref)
        self.duration = float(ref.GetObject().GetValue('duration'))
    
    def Duration(self):
        return self.duration
    
    def IsCritical(self):
        return self.time[0][1] == self.time[1][1] > -inf
    
    

class CCriticalPathFinder(object):
    
    def __init__(self, interface):
        
        self.interface = interface
        try:
            self.interface.AddMenu('MenuItem', 'mnuMenubar', 'graphtools', None, text = 'Graph Tools')
            self.interface.AddMenu('submenu', 'mnuMenubar/graphtools', None, None)
        except PluginInvalidParameter:
            pass
        self.interface.AddMenu('MenuItem', 'mnuMenubar/graphtools', ''.join(chr(random.randint(97,125))for i in xrange(6)), self.activity, text = 'Find critical path')
    
    def activity(self, path):
        try:
            metamodel = self.interface.DetailMetamodel()
            if (metamodel['uri'] != 'http://umlfri.kst.fri.uniza.sk/metamodel/graph.frim' 
            or metamodel['version'] != '0.0.1'):
                self.interface.DisplayWarning('Not supported metamodel')
                return
            
            diagram = self.interface.GetProject().GetCurrentDiagram()
            if diagram.GetType() != 'Critical Path diagram':
                self.interface.DisplayWarning('Critical path not supported on current diagram')
                return
            
            conditionlist = {}
            activities = {}
            conditions = {}
            for e in diagram.GetElements():
                o = e.GetObject()
                t = o.GetType()
                if t == 'activity':
                    activities[e.GetId()] = Activity(e)
                
                elif t == 'condition':
                    activities[e.GetId()] = conditions[e.GetId()] = Condition(e)
                
                elif t == 'conditionList':
                    conditionlist.update(dict([
                        (str(item['name']), item['value'] == 'True')
                        for item in eval(o.GetValue('conditions'))
                    ]))
            
            for c in conditions.itervalues():
                c.SetConditions(conditionlist)
            
            
            for c in diagram.GetConnections():
                s, d = c.GetSource(), c.GetDestination()
                activities[s.GetId()].AddNext(c, activities[d.GetId()])
                activities[d.GetId()].AddPrev(c, activities[s.GetId()])
            
            
            #monotonne usporiadanie
            idx = 0
            beginners = [a for a in activities.itervalues() if a.SumPrev() == 0]
            
            while beginners:
                first = beginners.pop(0)
                first.SetIdx(idx)
                idx += 1
                for hop in first.NextHops():
                    hop.DecPrev()
                    if hop.SumPrev() == 0:
                        beginners.append(hop)
            
            for a in activities.itervalues():
                a.ref.GetObject().SetValue('index', str(a.idx))
                
            if idx < len(activities):
                self.interface.DisplayWarning('Cycle in graph')
                return
            
            #hladanie casov
            sort = sorted(activities.values(), lambda x,y: cmp(x.idx, y.idx))
            
            
            for n in activities.itervalues():
                if len(n.prev) == 0:
                    n.time[0] = [0, n.Duration()]
            for n in sort:
                n.SendNext()
            
            for n in activities.itervalues():
                if len(n.next) == 0:
                    n.time[1] = [n.time[0][0], n.time[0][1]]
            for n in reversed(sort):
                n.SendPrev()
                
            for a in activities.itervalues():
                o = a.ref.GetObject()
                if o.GetType() == 'activity':
                    o.SetValue('minstart', str(a.time[0][0]))
                    o.SetValue('minend', str(a.time[0][1]))
                    o.SetValue('maxstart', str(a.time[1][0]))
                    o.SetValue('maxend', str(a.time[1][1]))
                else:
                    o.SetValue('value', a.val)
                o.SetValue('critical', a.IsCritical())
                for c, n in a.next:
                    c.GetObject().SetValue('critical', a.IsCritical() and n.IsCritical() and a.time[0][1] == n.time[0][0])
            
            self.a = activities
            self.s = sort
            
        except PluginProjectNotLoaded:
            self.interface.DisplayWarning('Project is not loaded')
        except (KeyError, ), e:
            self.interface.DisplayWarning('Unknown condition called "%s"'%e.args)
        #~ except:
            #~ self.interface.DisplayWarning('Unkown error in plugin')
        
        
        

if __name__ == '__main__':
    import sys
    interface = CInterface(int(sys.argv[1]))
    c = CCriticalPathFinder(interface)
    while 1:
        time.sleep(1.)
