if __debug__:
    SPLASH_TIMEOUT = 0
else:
    SPLASH_TIMEOUT = 5000

# extensions
ADDON_EXTENSION = '.fria'
PROJECT_EXTENSION = '.frip'
PROJECT_TPL_EXTENSION = '.frit'
PROJECT_CLEARXML_EXTENSION ='.fripx'

METAMODEL_NAMESPACE = '{http://umlfri.kst.fri.uniza.sk/xmlschema/metamodel.xsd}'
UMLPROJECT_NAMESPACE = '{http://umlfri.kst.fri.uniza.sk/xmlschema/umlproject.xsd}'
RECENTFILES_NAMESPACE = '{http://umlfri.kst.fri.uniza.sk/xmlschema/recentfiles.xsd}'
CONFIG_NAMESPACE = '{http://umlfri.kst.fri.uniza.sk/xmlschema/config.xsd}'
USERCONFIG_NAMESPACE = '{http://umlfri.kst.fri.uniza.sk/xmlschema/userconfig.xsd}'
METAMODEL_LIST_NAMESPACE = '{http://umlfri.kst.fri.uniza.sk/xmlschema/metamodelList.xsd}'
ADDON_NAMESPACE = "{http://umlfri.org/xmlschema/addon.xsd}"
ADDON_LIST_NAMESPACE = "{http://umlfri.org/xmlschema/addonList.xsd}"
USERGUI_NAMESPACE='http://umlfri.kst.fri.uniza.sk/xmlschema/usergui.xsd'

# UML .FRI server - web page, mail address and address for error logs
WEB = 'http://umlfri.org/'
MAIL = 'projekt@umlfri.org'
ERROR_LOG_ADDRESS = 'http://umlfri.org/errors/log.php'  
 
LABELS_CLICKABLE = True         # used to ignore labels at drawing area

# options for zoom 
SCALE_MAX = 5.0
SCALE_MIN = 0.6
SCALE_INCREASE = 0.2
BUFFER_SIZE=(2000,1500)         # buffer size at the start
BUFFER_MAX_SIZE=(6400,6400)     # the graphic buffer will be extended to max this values

DEFAULT_IDENTITY='@id'

PLUGIN_SOCKET = 0
PLUGIN_DISPLAY_COMMUNICATION = False
