from Utils import *

ROOT_PATH =      path(ROOT)
DOCS_PATH =      path(ROOT)
ETC_PATH =       path(ROOT, "etc")
CONFIG_PATH =    path(ETC_PATH, "config.xml")
TEMPLATES_PATH = path(ETC_PATH, "templates")

GUI_PATH =       path(ROOT, "gui")

IMAGES_PATH =    path(ROOT, "img")

ADDONS_PATH =    path(ROOT, "share", "addons")
LOCALES_PATH =   path(ROOT, "share", "locale")
SCHEMA_PATH =    path(ROOT, "share", "schema")

USERDIR_PATH =   path(USER, ".uml_fri")

SVN_REVISION =   svnrev(ROOT)
SVN_BRANCH =     svnbranch(ROOT)
