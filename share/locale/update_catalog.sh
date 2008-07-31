#!/bin/bash

PACKAGE_NAME='UML .FRI'
PACKAGE_VERSION="$(grep __version__ ../../main.py | cut -d"'" -f2)"

find ../.. | grep -E "(glade|py)$" | grep -v setup.py | xgettext -f- -o uml_fri.pot -s --no-location --package-name="$PACKAGE_NAME" --package-version="$PACKAGE_VERSION"
