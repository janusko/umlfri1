#!/bin/bash

if [ "$1" == "--help" ] || [ "$1" == "-h" ]; then
    echo "Usage:"
    echo "  $0 [application_path]"
    echo
    echo "If application path is not given, ../../.. is assumed"
    exit
fi

APP_PATH=${1:-../../..}
PACKAGE_NAME='UML .FRI'
PACKAGE_VERSION="$(grep '__version__ *=' $APP_PATH/main.py | cut -d"'" -f2)"

find $APP_PATH | grep -E "(glade|py)$" | grep -v setup.py | xgettext -f- -o $APP_PATH/share/locale/uml_fri.pot -s --no-location --package-name="$PACKAGE_NAME" --package-version="$PACKAGE_VERSION"
