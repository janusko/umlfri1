def check():
    """
    Check wether all dependencies are installed or not
    
    @raise AssertionError: if something missing
    """
    
    import sysplatform
    import etree
    import gtk2
    
    sysplatform.check()
    etree.check()
    gtk2.check()

def version():
    import sysplatform
    import etree
    import gtk2
    ret = []
    
    ret.extend(sysplatform.version())
    ret.extend(etree.version())
    ret.extend(gtk2.version())
    
    return ret
