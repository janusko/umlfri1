#!/bin/bash

find ../.. | grep -E "(glade|py)$" | grep -v setup.py | xgettext -f- -o uml_fri.pot
