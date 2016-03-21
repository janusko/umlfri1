def check():
    """
    Check wether all dependencies are installed or not
    
    @raise AssertionError: if something missing
    """
    try:
        import sysplatform
        import libxml
        import gtk2
        
        sysplatform.check()
        libxml.check()
        gtk2.check()
    except (AssertionError, ), e:
        import sys
        sys.exit(e)

def version():
    import sysplatform
    import libxml
    import gtk2
    ret = []
    
    ret.extend(sysplatform.version())
    ret.extend(libxml.version())
    ret.extend(gtk2.version())
    
    ret.append(('__debug__', str(__debug__)))
    
    return ret
