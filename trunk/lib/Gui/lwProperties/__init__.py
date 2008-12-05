import gtk

if gtk.gtk_version >= (2, 13):
    from lwPropertiesNew import ClwProperties
else:
    from lwPropertiesOld import ClwProperties