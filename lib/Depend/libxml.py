try:
    from lxml import etree
    from lxml.etree import XMLSyntaxError
    from lxml import html
    from lxml import builder
    HAVE_LXML = True
    LIBRARY=("lxml " + etree.__version__ + 
        " (libxml " + '.'.join(str(i) for i in etree.LIBXML_VERSION) + ")")
except ImportError:
    HAVE_LXML = False

def check():
    """
    Check wether any implementation of ElementTree library is installed, or not
    
    @raise AssertionError: if ElementTree is not installed
    """
    from base import checkDependencyMet
    
    checkDependencyMet(HAVE_LXML, "Python LXML library is required")
    
def version():
    """
    Check pygtk libraries versions
    
    @return: versions of each library connected to PyGTK
    @rtype: list of (str, str)
    """
    return [
        (_("etree version"), LIBRARY),
    ]
