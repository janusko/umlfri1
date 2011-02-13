from lib.model import Builder
from lib.generator import FileList
from optparse import OptionParser

builder = Builder()

builder.parse()
builder.finish()

root = builder.getRootNamespace()

#builder.printStructure()


