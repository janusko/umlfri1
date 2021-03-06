from UMLException import UMLException

class DevException(UMLException):
    """
    Super class for all developer exceptions. Make an exception a child of DevException
    if you want traceback.
    """
    pass 


class FactoryError(DevException):
    pass

class ConfigError(DevException):
    pass

class DomainFactoryError(FactoryError):
    pass
    
class DomainTypeError(DevException):
    pass

class DomainObjectError(DevException):
    pass

class DomainParserError(DevException):
    pass

class PluginCommunicationError(DevException):
    pass

class ParamValueError(PluginCommunicationError):
    pass

class ParamMissingError(PluginCommunicationError):
    pass

class ErrorDuringExecution(PluginCommunicationError):
    pass

class UnknowMethodError(PluginCommunicationError):
    pass

class UnknownClassNameError(PluginCommunicationError):
    pass
    
class TransactionError(PluginCommunicationError):
    pass
    
class TransactionModeUnspecifiedError(TransactionError):
    pass

class InvalidTransactionMode(TransactionError):
    pass

class TransactionPendingError(TransactionError):
    pass
    
class OutOfTransactionError(TransactionError):
    pass

class MetamodelValidationError(DevException):
    pass

class UIDException(DevException):
    pass
