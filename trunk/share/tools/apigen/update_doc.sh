#!/bin/bash

if [ "$1" == "--help" ] || [ "$1" == "-h" ]; then
    echo "Usage:"
    echo "  $0 [application_path]"
    echo
    echo "If application path is not given, ../../.. is assumed"
    exit
fi

if ! which epydoc > /dev/null 2>&1; then
    echo "Epydoc package must be installed, to complete this operation"
fi

APP_PATH=${1:-../../..}

cd "${APP_PATH}"
epydoc --config "share/tools/apigen/epydoc.ini"
