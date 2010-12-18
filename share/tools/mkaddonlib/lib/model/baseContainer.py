from base import Base

class BaseContainer(Base):
    def __init__(self, name, parent, children = [], sorted = True):
        Base.__init__(self, name, parent)
        
        self.__sorted = sorted
        
        self.__children = dict((child.getName(), child) for child in children)
        self.__orderedChildren = list(children)
        if self.__sorted:
            self.__orderedChildren.sort(key = lambda x: x.name)
    
    @property
    def children(self):
        for child in self.__orderedChildren:
            yield child
    
    def getChild(self, name):
        return self.__children[name]
    
    def _link(self, builder):
        Base._link(self, builder)
        
        for child in self.children:
            child._link(builder)
    
    def _addChild(self, child):
        self.__children[child.name] = child
        self.__orderedChildren.append(child)
        if self.__sorted:
            self.__orderedChildren.sort(key = lambda x: x.name)
