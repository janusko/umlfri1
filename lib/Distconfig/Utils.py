def syspath(path):
    import sys
    
    return path.decode(sys.getfilesystemencoding())

def path(*args):
    import os.path
    
    if args[0] == '~':
        args = (syspath(os.path.expanduser('~')), ) + args[1:]
    return os.path.abspath(os.path.join(*args))

def dir(path):
    import os.path
    
    return syspath(os.path.abspath(os.path.dirname(path)))

def root():
    import sys
    import imp
    
    if (hasattr(sys, "frozen") or hasattr(sys, "importers") or imp.is_frozen("__main__")):
        return path(syspath(sys.executable), '..')
    else:
        return path(dir(__file__), '..', '..')

def user():
    import os.path
    
    return syspath(os.path.expanduser('~'))

ROOT = root()
USER = user()

__all__ = ['ROOT', 'USER', 'path']
