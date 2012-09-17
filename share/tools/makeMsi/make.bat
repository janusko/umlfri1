SET code_path=..\..\..\
SET install_name=UMLFRI_1.0_Win32_setup
SET pyinstaller_path=pyinstaller

python %pyinstaller_path%\pyinstaller.py specs\umlfri.spec
python %pyinstaller_path%\pyinstaller.py specs\pl_runner.spec

python MSIFiles\generateWix.py 
candle %install_name%.wxs -ext WixUIExtension.dll -ext WixUtilExtension.dll
light %install_name%.wixobj -ext WixUIExtension.dll -ext WixUtilExtension.dll -cultures:en-US -b MSIFiles\Licenses 
