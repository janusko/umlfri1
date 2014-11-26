# -*- mode: python -*-
import os
project_dir=os.environ.get("code_path")
out_dir='..\\bins'
pl_dir=project_dir+'\\share\\addons\\pythonStarter'
hiddenimports=['code','codeop','platform','gtk.keysyms']
a = Analysis([os.path.join(HOMEPATH,'support\\_mountzlib.py'), os.path.join(HOMEPATH,'support\\useUnicode.py'),pl_dir+'\\starter\\pl_runner.py'],[pl_dir+'\\library'], hiddenimports = hiddenimports)
pyz = PYZ(a.pure)
exe = EXE( pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name=os.path.join('..\\bins\\share\\addons\\pythonStarter\\starter','pl_runner.exe'),
          debug=False,
          strip=False,
          upx=True,
          console=False,
          icon=project_dir+'\\doc\\Logo\\icon.ico' )
