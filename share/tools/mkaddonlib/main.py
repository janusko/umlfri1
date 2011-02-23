#!/usr/bin/python

import sys

from lib.model import Builder
from lib.generator import FileList
from optparse import OptionParser

options_parser = OptionParser(usage = "usage: %prog [options] index1 [index2 [...]]")
options_parser.add_option("-o", "--output", dest="outdir", default="output/",
                  help="write output to DIR", metavar="DIR")

(options, args) = options_parser.parse_args()

if not args:
    options_parser.print_help()
    sys.exit()

builder = Builder()

builder.parse()
builder.finish()

root = builder.getRootNamespace()

out = FileList(root)

for index in args:
    out.parse(index)

out.create(options.outdir)
