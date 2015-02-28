import gtk

pixmaps = {}

def PixmapFromPath(storage, path):
    if (storage, path) in pixmaps:
        tmp = pixmaps[(storage, path)]
    else:
        if storage is None:
            tmp = gtk.gdk.pixbuf_new_from_file(unicode(path))
        else:
            pathx = storage.file(path)
            loader = gtk.gdk.PixbufLoader()
            while True:
                tmp = pathx.read(102400)
                if not tmp:
                    break
                loader.write(tmp)
            loader.close()
            tmp = loader.get_pixbuf()
        pixmaps[(storage, path)] = tmp
    return tmp