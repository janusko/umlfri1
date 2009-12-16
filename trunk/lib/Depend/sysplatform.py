import platform

def check():
    """
    Check wether platform is sufficient or not
    
    @raise AssertionError: if platform configuration is insufficient
    """
    req = [2, 5]
    ver = []
    
    for s in platform.python_version_tuple():
        i = len(s)
        while i:
            try:
                n = int(s[:i])
                break
            except ValueError:
                i -= 1
        if i:
            if i < len(s):
                n -= .5
            ver.append(n)
        else:
            break
    
    if ver < req:
        raise AssertionError("You will need at least Python 2.5 to run UML .FRI")

def version():
    """
    Check platform informations
    
    @return: version of python and platform informations
    @rtype: list of (str, str)
    """
    return [
        (_("Machine"), platform.machine()),
        (_("Architecture"), platform.architecture()[0]),
        (_("Platform"), platform.platform()),
        (_("Python version"), ".".join(str(i) for i in platform.python_version_tuple())),
    ]
