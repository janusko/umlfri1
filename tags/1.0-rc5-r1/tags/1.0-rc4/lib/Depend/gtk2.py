try:
    import pygtk
except ImportError:
    pygtk = None

try:
    import gtk
    import gtk.glade
    import gtk.gdk
    import gtk.keysyms
except ImportError:
    gtk = None

try:
    import gobject
except ImportError:
    gobject = None

try:
    import glib
except ImportError:
    glib = gobject

try:
    import pango
except ImportError:
    pango = None

try:
    import cairo
except ImportError:
    cairo = None

try:
    import pangocairo
except ImportError:
    pangocairo = None

def check():
    """
    Check wether pygtk library is installed, or not
    
    @raise AssertionError: if gtk support is missing
    """
    from base import checkDependencyMet
    
    checkDependencyMet(gobject is not None and gtk is not None, "PyGTK 2.x must be installed")
    checkDependencyMet(pango is not None, "PyGTK have no pango support")
    checkDependencyMet(cairo is not None and pangocairo is not None, "PyGTK have no cairo support")
    
    checkDependencyMet(gtk.gtk_version >= (2, 10), "GTK+ 2.10 or better is required")
    checkDependencyMet(gtk.pygtk_version >= (2, 10), "PyGTK 2.10 or better is required")
    
    checkDependencyMet(gtk.gtk_version < (2, 13) or (2, 14, 7) <= gtk.gtk_version,
        ("GTK+ %s has known bug and is not supported" % ('.'.join(str(i) for i in gtk.gtk_version),))
    )

def version():
    """
    Check pygtk libraries versions
    
    @return: versions of each library connected to PyGTK
    @rtype: list of (str, str)
    """
    return [
        (_("GTK+ version"), ".".join(str(i) for i in gtk.gtk_version)),
        (_("PyGTK version"), ".".join(str(i) for i in gtk.pygtk_version)),
    ]
