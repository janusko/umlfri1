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

def frozen():
    import sys
    import imp
    
    return (hasattr(sys, "frozen") or hasattr(sys, "importers") or imp.is_frozen("__main__"))

def root():
    import sys
    
    if frozen():
        return path(syspath(sys.executable), '..', '..')
    else:
        return path(dir(__file__), '..', '..')

def user():
    import os.path
    
    return syspath(os.path.expanduser('~'))

def svnentry(path):
    import os.path
    
    try:
        with open(os.path.join(path, '.svn', 'entries')) as svn:
            result = []
            for idx, line in enumerate(svn):
                if idx in [3, 4, 10]:
                    result.append(line[:-1])
                if idx > 10:
                    break
            return int(result[0]), result[1], int(result[2])
    except:
        return None, None, None

def svnrev(path):
    return svnentry(path)[0]

def svnbranch(path):
    return svnentry(path)[1]

ROOT = root()
USER = user()

IS_FROZEN = frozen()

__all__ = ['ROOT', 'USER', 'IS_FROZEN', 'path', 'svnrev', 'svnbranch']
