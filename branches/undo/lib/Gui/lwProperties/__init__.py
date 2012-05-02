# -*- coding: utf-8 -*-
from lib.Depend.gtk2 import gtk

if (2, 18) > gtk.gtk_version >= (2, 13):
    from lwPropertiesNew import ClwProperties
else:
    from lwPropertiesOld import ClwProperties