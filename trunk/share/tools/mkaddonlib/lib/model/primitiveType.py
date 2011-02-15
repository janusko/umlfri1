class PrimitiveType(object):
    def __init__(self, name, isNumeric = False, isLogic = False, isString = False, isObject = False, default = None, convertor = None):
        self.__name = name
        self.__isNumeric = isNumeric
        self.__isLogic = isLogic
        self.__isString = isString
        self.__isObject = isObject
        self.__default = default
        self.__convertor = convertor
    
    @property
    def name(self):
        return self.__name
    
    @property
    def fqn(self):
        return '::' + self.__name
    
    @property
    def isNumeric(self):
        return self.__isNumberic
    
    @property
    def isLogic(self):
        return self.__isLogic
    
    @property
    def isString(self):
        return self.__isString
    
    @property
    def isObject(self):
        return self.__isObject
    
    @property
    def default(self):
        return self.__default
    
    @property
    def canConvert(self):
        return self.__convertor is not None
    
    def convert(self, value):
        return self.__convertor(value)

primitiveTypes = {
    'boolean':      PrimitiveType('boolean', isLogic = True, convertor = bool, default = False),
    'inputstream':  PrimitiveType('inputstream', isObject = True),
    'int32':        PrimitiveType('int32', isNumeric = True, convertor = int, default = 0),
    'variant':      PrimitiveType('variant'),
    'string':       PrimitiveType('string', isString = True, convertor = str, default = ""),
    'xy':           PrimitiveType('xy', isObject = True),
    'xywh':         PrimitiveType('xywh', isObject = True),
    'wh':           PrimitiveType('wh', isObject = True),
    'keyvalue':     PrimitiveType('keyvalue', isObject = True),
}
