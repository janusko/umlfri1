from os.path import join, dirname, abspath, expanduser, isdir
import sys
import imp

if (hasattr(sys, "frozen") or hasattr(sys, "importers") or imp.is_frozen("__main__")):
    ROOT_PATH = abspath(join(dirname(sys.executable), '..'))
else:
    ROOT_PATH = abspath(join(dirname(__file__), '..'))

ROOT_PATH = ROOT_PATH.decode(sys.getfilesystemencoding())

ETC_PATH = join(ROOT_PATH, 'etc')

MAIN_CONFIG_PATH = join(ETC_PATH, 'config.xml')
USERGUI_PATH ='/Paths/UserDir/usergui.xml'

SPLASH_TIMEOUT = 0

VERSIONS_PATH = 'versions'
DIAGRAMS_PATH = 'diagrams'
ELEMENTS_PATH = 'elements'
CONNECTIONS_PATH = 'connections'
ICONS_PATH = 'icons'
DOMAINS_PATH = 'domains'
METAMODEL_PATH = 'metamodel.xml'
ADDON_PATH = 'addon.xml'

ARROW_IMAGE = 'arrow.png'

DEFAULT_TEMPLATE_ICON = 'default_icon.png'
SPLASH_IMAGE = 'splash.png'
STARTPAGE_IMAGE = 'startpage.png'
GRAB_CURSOR = 'grab.png'
GRABBING_CURSOR = 'grabbing.png'
# extensions
PROJECT_EXTENSION = '.frip'
PROJECT_TPL_EXTENSION = '.frit'
PROJECT_CLEARXML_EXTENSION ='.fripx'

METAMODEL_NAMESPACE = '{http://umlfri.kst.fri.uniza.sk/xmlschema/metamodel.xsd}'
UMLPROJECT_NAMESPACE = '{http://umlfri.kst.fri.uniza.sk/xmlschema/umlproject.xsd}'
RECENTFILES_NAMESPACE = '{http://umlfri.kst.fri.uniza.sk/xmlschema/recentfiles.xsd}'
CONFIG_NAMESPACE = '{http://umlfri.kst.fri.uniza.sk/xmlschema/config.xsd}'
METAMODEL_LIST_NAMESPACE = '{http://umlfri.kst.fri.uniza.sk/xmlschema/metamodelList.xsd}'
ADDON_NAMESPACE = "{http://umlfri.org/xmlschema/addon.xsd}"
ADDON_LIST_NAMESPACE = "{http://umlfri.org/xmlschema/addonList.xsd}"
USERGUI_NAMESPACE='http://umlfri.kst.fri.uniza.sk/xmlschema/usergui.xsd'

# UML .FRI server - web page, mail address and address for error logs
WEB = 'http://umlfri.org/'
MAIL = 'projekt@umlfri.org'
ERROR_LOG_ADDRESS = 'http://umlfri.org/errors/log.php'  

DEBUG = True                    # turn DEBUG to true for some more information, e.g. user exceptions will be shown with traceback
ERROR_TO_CONSOLE = False        # only if DEBUG is true, instead of showing the exception in a window it will be printed to console
 
LABELS_CLICKABLE = True         # used to ignore labels at drawing area

# options for zoom 
SCALE_MAX = 5.0
SCALE_MIN = 0.6
SCALE_INCREASE = 0.2
BUFFER_SIZE=(2000.0,1500.0)         # buffer size at the start

DEFAULT_IDENTITY='@id'

# history consts
STACK_SIZE_TO_SHOW = 20             # number of undo/redo steps shown in the undo/redo menu 
STACK_MAX_SIZE = 300               # maximum size of the undo/redo stack kept by the application history
