import Directory
import ZipStorage

classes = [
    Directory.CDirectory,
    ZipStorage.CZipStorage,
]

def open_storage(path):
    for cls in classes:
        obj = cls.create(path)
        if obj is not None:
            return obj
