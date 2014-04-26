# Adapted from the source code of Scintilla Maxgui Gadget
import ctypes
from ctypes import c_int, c_ulong, c_char_p, c_wchar_p, c_ushort

OFN_OVERWRITEPROMPT     = 0x00000002
OFN_HIDEREADONLY        = 0x00000004
OFN_ALLOWMULTISELECT    = 0x00000200
OFN_PATHMUSTEXIST       = 0x00000800
OFN_FILEMUSTEXIST       = 0x00001000
OFN_EXPLORER            = 0x00080000

class OPENFILENAME(ctypes.Structure):
    _fields_ = (("lStructSize", c_int),
        ("hwndOwner", c_int),
        ("hInstance", c_int),
        ("lpstrFilter", c_wchar_p),
        ("lpstrCustomFilter", c_char_p),
        ("nMaxCustFilter", c_int),
        ("nFilterIndex", c_int),
        ("lpstrFile", c_wchar_p),
        ("nMaxFile", c_int),
        ("lpstrFileTitle", c_wchar_p),
        ("nMaxFileTitle", c_int),
        ("lpstrInitialDir", c_wchar_p),
        ("lpstrTitle", c_wchar_p),
        ("flags", c_int),
        ("nFileOffset", c_ushort),
        ("nFileExtension", c_ushort),
        ("lpstrDefExt", c_char_p),
        ("lCustData", c_int),
        ("lpfnHook", c_char_p),
        ("lpTemplateName", c_char_p),
        ("pvReserved", c_char_p),
        ("dwReserved", c_int),
        ("flagsEx", c_int))

    def __init__(self, win, title):
        ctypes.Structure.__init__(self)
        self.lStructSize = ctypes.sizeof(OPENFILENAME)
        self.nFilterIndex = 1
        self.nMaxFile = 1024
        self.hwndOwner = win
        self.lpstrTitle = title
        self.flags = OFN_HIDEREADONLY | OFN_EXPLORER

class COpenSaveDialog(object):
    def __init__(self, parent, type, title, filter):
        self.__title = title.decode('utf8')
        self.__type = type
        self.__filter = filter
        self.__parentDialog = parent
        self.__path = None
        self.__filterIndex = None
    
    def ShowModal(self):
        ofx = OPENFILENAME(self.__parentDialog.window.handle, self.__title)
        opath = "\0" * 1024
        ofx.lpstrFile = opath
        
        filterText = "\0".join(['%s\0%s'%(f[0], f[1]) for f in self.__filter])+"\0\0"
        ofx.lpstrFilter = filterText
        
        if self.__type == 'open':
            fnc = ctypes.windll.comdlg32.GetOpenFileNameW
            ofx.flags |= OFN_FILEMUSTEXIST
        else:
            fnc = ctypes.windll.comdlg32.GetSaveFileNameW
            ofx.flags |= OFN_PATHMUSTEXIST | OFN_OVERWRITEPROMPT

        if fnc(ctypes.byref(ofx)):
            self.__path = ofx.lpstrFile.replace("\0", "")
            self.__filterIndex = ofx.nFilterIndex
            return True
        else:
            return False
    
    def GetAbsolutePath(self):
        return self.__path
    
    def GetSelectedFilter(self):
        return self.__filter[self.__filterIndex - 1]
        
    def GetSelectedFilterIndex(self):        
        return self.__filterIndex - 1
