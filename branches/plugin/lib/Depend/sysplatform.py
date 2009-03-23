import platform

def check():
    """
    Check wether platform is sufficient or not
    
    @raise AssertionError: if platform configuration is insufficient
    """
    
    assert tuple(platform.python_version_tuple()) >= (2, 5)

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
