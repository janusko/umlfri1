class PluginError(Exception): pass
    
class PluginUnknownCommand(PluginError): pass
class PluginUnsupportedVersion(PluginError): pass
class PluginInvalidCommandType(PluginError): pass
class PluginMissingParameter(PluginError): pass
class PluginInvalidParameter(PluginError): pass
class PluginInvalidObject(PluginError): pass
class PluginUnknownMethod(PluginError): pass
class PluginInvalidMethodParameters(PluginError): pass
class PluginProjectNotLoaded(PluginError): pass
class PluginUnknownConstructor(PluginError): pass
    
class PluginInMainloop(PluginError): pass
    
class PluginAccessDenied(PluginError): pass

