# -*- mode: python -*-
# gtk - prist na cestu zo setup.py
# locales skopirovat -
# prist na themes

def search_for_gtk():
    import os
    import re
    reWinVar = re.compile('%(?P<env>[a-zA-Z][a-zA-Z0-9]*)%?')
    def expandwinvars(path):
        while True:
            path, n = reWinVar.subn(lambda grp: os.environ[grp.group("env")], path)
            if n == 0:
                return path
    for path in expandwinvars(os.environ['PATH']).split(';')[::-1]:
        if os.path.isfile(os.path.join(path, 'libglib-2.0-0.dll')):
            return os.path.normpath(os.path.join(path, '..'))
#from ..\paths.py import project_dir
gtk_dir = search_for_gtk()
project_dir=os.environ.get("code_path")
a = Analysis([os.path.join(HOMEPATH,'support\\_mountzlib.py'), os.path.join(HOMEPATH,'support\\useUnicode.py'), project_dir+'\\main.py'])

pyz = PYZ(a.pure)
exe = EXE( pyz,
          a.scripts,
          exclude_binaries=1,
          name=os.path.join('build\\pyi.win32\\bin', 'UML FRI.exe'),
          debug=False,
          strip=False,
          upx=True,
          console=False,
          icon=project_dir+'\\doc\Logo\icon.ico' )
coll = COLLECT( exe,
                a.binaries,
                Tree(project_dir+'\\share','../share',excludes=['.svn','publicApi','tools','libraryTemplate','*.pyc','*.pot','*.pom']),
                Tree(project_dir+'\\gui','../gui',excludes=['.svn']),
                Tree(project_dir+'\\etc','../etc',excludes=['.svn']),
                Tree(project_dir+'\\img','../img',excludes=['.svn']),
                Tree(gtk_dir + '\\share\\locale\\sk\\LC_MESSAGES','../share/locale/sk/LC_MESSAGES'),
                Tree(gtk_dir + '\\lib\\gtk-2.0\\2.10.0\\engines','../lib/gtk-2.0/2.10.0/engines'),
                [('../etc/gtkrc', gtk_dir + '\\share\\themes\\MS-Windows\\gtk-2.0\\gtkrc', 'DATA'),('..\README',project_dir+'\\README','DATA'),('..\LICENSE',project_dir+'\\LICENSE','DATA'),('..\\ABOUT',project_dir+'\\ABOUT','DATA')],
                a.zipfiles,
                a.datas,
                strip=False,
                upx=True,
                name=os.path.join('../bins', 'bin'))