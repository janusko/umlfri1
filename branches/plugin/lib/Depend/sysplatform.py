import platform, os

def check():
    """
    Check wether platform is sufficient or not
    
    @raise AssertionError: if platform configuration is insufficient
    """
    
    if os.name == 'nt':
        assert tuple(int(i) for i in platform.python_version_tuple()) >= (2, 6), "You will need at least Python 2.6 to run UML .FRI on Windows"
    else:
        assert tuple(int(i) for i in platform.python_version_tuple()) >= (2, 5), "You will need at least Python 2.5 to run UML .FRI on %s system" % (os.name, )

def version():
    """
    Check platform informations
    
    @return: version of python and platform informations
    @rtype: list of (str, str)
    """
    return [
        ("Machine", platform.machine()),
        ("Architecture", platform.architecture()[0]),
        ("Platform", platform.platform()),
        ("Python version", ".".join(str(i) for i in platform.python_version_tuple())),
    ]
