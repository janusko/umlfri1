import gtk

if (2,15) > gtk.gtk_version >= (2, 13):
    from lwPropertiesNew import ClwProperties
else:
    from lwPropertiesOld import ClwProperties