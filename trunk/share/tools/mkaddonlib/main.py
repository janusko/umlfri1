from lib.model import Builder

builder = Builder()

builder.parse()
builder.finish()

root = builder.getRootNamespace()

builder.printStructure()
