class platform:
    import sys as __sys

    @classmethod
    def isA(cls, platform):
        if platform == "windows":
            return cls.__sys.platform in ('win32', 'cygwin')
        else:
            return cls.__sys.platform == platform
            
def getPythonVersion():
    import platform

    ver = []
    for s in platform.python_version_tuple():
        if isinstance(s, (int, float)):
            ver.append(s)
        else:
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
    return ver


def check():
    """
    Check wether platform is sufficient or not
    
    @raise AssertionError: if platform configuration is insufficient
    """
    from base import checkDependencyMet
    
    req = [2, 5]
    
    ver = getPythonVersion()
    
    checkDependencyMet(ver >= req, "You will need at least Python 2.5 to run UML .FRI")

def version():
    """
    Check platform informations
    
    @return: version of python and platform informations
    @rtype: list of (str, str)
    """
    import platform
    
    return [
        (_("Machine"), platform.machine()),
        (_("Architecture"), platform.architecture()[0]),
        (_("Platform"), platform.platform()),
        (_("Python version"), ".".join(str(i) for i in platform.python_version_tuple())),
    ]
