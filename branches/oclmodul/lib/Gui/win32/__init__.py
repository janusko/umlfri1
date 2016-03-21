import sys

if sys.platform in ('win32', 'cygwin'):
    from OpenSaveDialog import COpenSaveDialog
else:
    COpenSaveDialog = None

del sys
