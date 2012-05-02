import weakref

uid = 0

class Object(object):
    def __init__(self, obj):
        global uid
        uid = uid + 1
        
        self.__obj = obj
        self.__uid = uid
        self.__references = []
        self.__className = obj.__class__.__name__
        self.__reducing = False
        self.__reduced = False
    
    def renderObject(self, f, renderClasses, renderReduced):
        if not isinstance(self, renderClasses) or (not renderReduced and self.isReduced()):
            return
        
        print>>f, ('x%08X [ label = "%s", shape = box ]' % (self.__uid, self.__className))
    
    def renderReferences(self, f, renderClasses, renderReduced):
        if not isinstance(self, renderClasses) or (not renderReduced and self.isReduced()):
            return
        
        for ref in self.__references:
            if not isinstance(ref, renderClasses) or (not renderReduced and ref.isReduced()):
                continue
            
            if isinstance(ref, WeakRef):
                print>>f, ('x%08X -> x%08X [ style = dotted ]' % (self.__uid, ref.getTarget().getUid()))
            else:
                print>>f, ('x%08X -> x%08X' % (self.__uid, ref.getUid()))
    
    def reduce(self):
        if self.__reducing:
            return False
        
        self.__reducing = True
        self.__reduced = len([ref for ref in self.__references if not ref.reduce()]) == 0
        self.__reducing = False
        
        
        return self.__reduced
    
    def isReduced(self):
        return self.__reduced
    
    def getUid(self):
        return self.__uid
    
    def getClassName(self):
        return self.__className
    
    def addAttribute(self, name, value):
        self.__references.append(value)

class List(object):
    def __init__(self, l):
        global uid
        uid = uid + 1
        
        self.__uid = uid
        self.__references = []
        self.__className = l.__class__.__name__
        self.__reducing = False
        self.__reduced = False
    
    def renderObject(self, f, renderClasses, renderReduced):
        if not isinstance(self, renderClasses) or (not renderReduced and self.isReduced()):
            return
        
        print>>f, ('x%08X [ label = "%s", shape = diamond ]' % (self.__uid, self.__className))
    
    def renderReferences(self, f, renderClasses, renderReduced):
        if not isinstance(self, renderClasses) or (not renderReduced and self.isReduced()):
            return
        
        for ref in self.__references:
            if not isinstance(ref, renderClasses) or (not renderReduced and ref.isReduced()):
                continue
            
            if isinstance(ref, WeakRef):
                print>>f, ('x%08X -> x%08X [ style = dotted ]' % (self.__uid, ref.getTarget().getUid()))
            else:
                print>>f, ('x%08X -> x%08X' % (self.__uid, ref.getUid()))
    
    def reduce(self):
        if self.__reducing:
            return False
        
        self.__reducing = True
        self.__reduced = len([ref for ref in self.__references if not ref.reduce()]) == 0
        self.__reducing = False
        
        
        return self.__reduced
    
    def isReduced(self):
        return self.__reduced
    
    def getUid(self):
        return self.__uid
    
    def getClassName(self):
        return self.__className
    
    def addValue(self, value):
        self.__references.append(value)

class Primitive(object):
    def __init__(self, value):
        global uid
        uid = uid + 1
        
        self.__uid = uid
        self.__value = value
    
    def renderObject(self, f, renderClasses, renderReduced):
        if not isinstance(self, renderClasses) or (not renderReduced and self.isReduced()):
            return
        
        print>>f, ('x%08X [ label = "%s", shape = box ]' % (self.__uid, self.__className))
    
    def renderReferences(self, f, renderClasses, renderReduced):
        pass
    
    def reduce(self):
        return True
    
    def isReduced(self):
        return True
    
    def getUid(self):
        return self.__uid
    
    def getValue(self):
        return self.__className

class WeakRef(object):
    def __init__(self, target):
        global uid
        uid = uid + 1
        
        self.__uid = uid
        self.__target = target
    
    def renderObject(self, f, renderClasses, renderReduced):
        pass
    
    def renderReferences(self, f, renderClasses, renderReduced):
        pass
    
    def reduce(self):
        return True
    
    def isReduced(self):
        return True
    
    def getUid(self):
        return self.__uid
    
    def getTarget(self):
        return self.__target

class DependencyGraph(object):
    def __init__(self, obj):
        self.__obj = obj
        
        self.__parsedCache = {}
        self.reparse()
    
    def reparse(self):
        self.__allObjs = []
        self.__parsed = self.__parse(self.__obj)
        self.__parsedCache = {}
        
        self.__parsed.reduce()
    
    def __parse(self, obj):
        i = id(obj)
        if i in self.__parsedCache:
            return self.__parsedCache[i]
        
        if obj is None or isinstance(obj, (str, unicode, int, long, float)):
            ret = self.__parsedCache[i] = Primitive(obj)
        elif isinstance(obj, weakref.ref):
            tar = self.__parse(obj())
            if tar is None:
                return None
            ret = self.__parsedCache[i] = WeakRef(tar)
        elif isinstance(obj, (list, tuple)):
            ret = self.__parsedCache[i] = List(obj)
            for value in obj:
                value = self.__parse(value)
                if value is not None:
                    ret.addValue(value)
        elif isinstance(obj, (dict, weakref.WeakKeyDictionary, weakref.WeakValueDictionary)):
            ret = self.__parsedCache[i] = List(obj)
            for item, value in obj.iteritems():
                item = self.__parse(item)
                if item is not None:
                    ret.addValue(item)
                value = self.__parse(value)
                if value is not None:
                    ret.addValue(value)
        elif not callable(obj) and hasattr(obj, '__class__') and hasattr(obj, '__dict__'):
            ret = self.__parsedCache[i] = Object(obj)
            for attr, value in obj.__dict__.iteritems():
                value = self.__parse(value)
                if value is not None:
                    ret.addAttribute(attr, value)
        else:
            return None
        
        self.__allObjs.append(ret)
        
        return ret
    
    def render(self, f, renderPrimitive = False, renderWeakRef = True, renderReduced = False):
        classes = [Object, List]
        
        if renderPrimitive:
            classes.append(Primitive)
        if renderWeakRef:
            classes.append(WeakRef)
        
        classes = tuple(classes)
        
        if isinstance(f, (str, unicode)):
            f = open(f, 'w')
        
        print>>f, ('digraph Dependencies {')
        
        if renderReduced or not self.__parsed.isReduced():
            for obj in self.__allObjs:
                obj.renderObject(f, classes, renderReduced)
            for obj in self.__allObjs:
                obj.renderReferences(f, classes, renderReduced)
        
        print>>f, ('}')
