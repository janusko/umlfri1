def getPath(type):
    path = []
    tmp = type
    while tmp.parent is not None:
        path.insert(0, tmp)
        tmp = tmp.parent
    
    path = [part.identifier.lowerCamelCase for part in path]
    
    return '.'.join(path) + '.html'
