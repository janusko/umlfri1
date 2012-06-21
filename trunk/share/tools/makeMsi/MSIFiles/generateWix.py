__author__= "Mattho"
import os.path
import sys,uuid
#argument 1 nazov suboru
#argument 2 cesta k priecinku

def getId():
  global compid
  compid+=1
  return str("UMID"+str(compid))
  
def getFilId():
  global filId
  filId+=1
  return str("FID"+str(filId))


def genfromtree( root,feat,name_dir=""):
    files = []
    dirs=[]
    names=os.listdir(root)
    for name in names:
        fullname = os.path.normpath(os.path.join(root, name))
        if os.path.isfile(fullname) and not os.path.isdir(fullname):
            files.append((name,fullname))
        elif os.path.isdir(fullname) and not os.path.islink(fullname):
            dirs.append((name,fullname))
       
    if name_dir!="":
        lin.append('<Directory Id="'+getFilId()+'" Name="'+name_dir+'">\n')
    if name_dir=="bin":
        lin.append("""
        <Component Id="ID1532" Guid="ad6600f4-3451-49d6-9a31-39dd2dcb2f60">
                <ProgId Id="ID6004" Description=".frip File" Icon="filetype_icon" IconIndex="0">
                  <Extension Id="frip" ContentType="aaaa">
                    <Verb Id="Open" Command="Open" TargetFile="ID_736c205c_ef71_411b_84b4_359e285d7c74" Argument="&quot;%1&quot;" />
                  </Extension>
                </ProgId>
                <ProgId Id="ID6005" Description="Fripx file" Icon="filetype_icon" IconIndex="0">
                  <Extension Id="fripx" ContentType="Fripx file">
                    <Verb Id="Open" Command="Open" TargetFile="ID_736c205c_ef71_411b_84b4_359e285d7c74" Argument="&quot;%1&quot;" />
                  </Extension>
                </ProgId>
                <ProgId Id="ID6006" Description="Frit file" Icon="filetype_icon" IconIndex="0">
                  <Extension Id="frit" ContentType=".frit">
                    <Verb Id="Open" Command="Open" TargetFile="ID_736c205c_ef71_411b_84b4_359e285d7c74" Argument="&quot;%1&quot;" />
                    <Verb Id="New" Command="New" TargetFile="ID_736c205c_ef71_411b_84b4_359e285d7c74" Argument="--new &quot;%1&quot;" />
                  </Extension>
                </ProgId>
                <ProgId Id="ID6007" Description="Fria file" Icon="filetype_icon" IconIndex="0">
                  <Extension Id="fria" ContentType="fria">
                    <Verb Id="Open" Command="Open" TargetFile="ID_736c205c_ef71_411b_84b4_359e285d7c74" Argument="&quot;%1&quot;" />
                  </Extension>
                </ProgId>
                <File Id="ID_736c205c_ef71_411b_84b4_359e285d7c74" Source="""+'"'+root+"""\UML FRI.exe" DiskId="1" Name="UML FRI.exe" />
              </Component>
              <Component Id="ID20633" Guid="18df63c4-b24a-4fda-aecc-50c38554d6fa">
                <RegistryValue Root="HKCU" Key="SOFTWARE\Faculty of Management Sience and Informatic University of Zilina\UML .FRI\Components\ID20633" Type="string" KeyPath="yes" Value="" />
                <Shortcut Id="ID20632" Target="[#ID_736c205c_ef71_411b_84b4_359e285d7c74]" Directory="ProgramMenuDir" Name="UML .FRI" />
              </Component>
              <Component Id="ID20635" Guid="14c26f5f-7b9a-4a31-b82f-88e3a49e0a44">
                <RegistryValue Root="HKCU" Key="SOFTWARE\Faculty of Management Sience and Informatic University of Zilina\UML .FRI\Components\ID20635" Type="string" KeyPath="yes" Value="" />
                <Shortcut Id="ID20634" Target="[#ID_736c205c_ef71_411b_84b4_359e285d7c74]" Directory="DesktopFolder" Name="UML .FRI" />
              </Component>

        """)

  
    for d in dirs:
        if name_dir!='addons':
            genfromtree(d[1],feat,d[0])
        else:
            if d[0]!='pythonStarter':
                fetr=[]
                features.append((d[0],fetr))
                genfromtree(d[1],fetr,d[0])
            else:
                genfromtree(d[1],feat,d[0])

    if len (files)>0:
     # lin.append("<CreateDirectory/>\n")
      componentID=getId()
      global mainFeature
      feat.append(componentID)
      lin.append('<Component Id="'+componentID+'"'+' Guid="'+str(uuid.uuid4())+'">\n')
      lin.append('<CreateFolder />\n')
      for f in files:
        if f[0]!= 'UML FRI.exe':
            if f[0]=='fileicon.ico':
                lin.append(str('<File Id= "filetype_icon" Source ="'+f[1]+'" Name ="'+f[0]+'"/> \n'))
            else:
                lin.append(str('<File Id= "'+getFilId()+'" Source ="'+f[1]+'" Name ="'+f[0]+'"/> \n'))
      lin.append("</Component>\n")
    lin.append("</Directory>\n")
      

compid=0;
filId=0;
names={'uml':'UML','bpmn':'BPMN Diagram','dfd':'Data Flow Diagram','flowchart':'Flowchart Diagram','pythonTerminal':'Python Terminal','roads':'Road Network Model'}
if len( sys.argv)<3:
    print "neboli zadane vsekty parametre pouziju sa standardne hodnoty"
    binary_files='bins'
    outputFile=os.environ.get("install_name")+'.wxs'
else:
    outputFile=sys.argv[1]
    binnary_files=sys.argv[2]
#===========================================================
#variables
#===========================================================
linesFile=[]
lin=[]
product_id=uuid.uuid4()
upgrade_id='2e1c6140-1c1a-47c5-ab73-18d4d1a7dab0';
#======================================================
#FEATURES
#main features - hlavny program, list komponentov
# features - pole featur [nazov,list komponentov)
#===================================================
mainFeature=[]
features=[]

lin.append('<?xml version="1.0" encoding="utf-8"?>\n'+
'<Wix xmlns="http://schemas.microsoft.com/wix/2006/wi">\n'+

 ' <Product Id="'+str(product_id)+'" Name="UML .FRI" Manufacturer="Faculty of Management Sience and Informatic University of Zilina" UpgradeCode="'+str(upgrade_id)+'" Language="1033" Codepage="1252" Version="1.0.0">\n'+
 '  <Package Description="UML .FRI" Manufacturer="Faculty of Management Sience and Informatic University of Zilina" SummaryCodepage="1252" Languages="1033" InstallerVersion="300" Keywords="Installer" Compressed="yes" />\n'+
 '   <Media Id="1" Cabinet="Setup_1.cab" EmbedCab="yes" DiskPrompt="CD-ROM #1" CompressionLevel="mszip" />\n'+
 '   <Property Id="DiskPrompt" Value="UML .FRI Installation [1]" />\n'+
 '  <Upgrade Id="'+str(upgrade_id)+'">\n'+
 '  <UpgradeVersion OnlyDetect="no" Property="WARSETUP_PREVIOUSVERSIONFOUND" IncludeMinimum="yes" Minimum="0.0.0" Maximum="1.0.0" IncludeMaximum="yes" />\n'+
   ' </Upgrade>\n'+
   ' <InstallExecuteSequence>\n'+
   '   <Custom Action="ID20426" After="CostFinalize" />\n'+
   '   <LaunchConditions Sequence="100">NOT Installed</LaunchConditions>\n'+
   '   <FindRelatedProducts Sequence="200" />\n'+
   '   <AppSearch Sequence="300" />\n'+
   '   <CCPSearch Sequence="400">NOT Installed</CCPSearch>\n'+
   '   <RMCCPSearch Sequence="600">NOT Installed AND CPP_TEST</RMCCPSearch>\n'+
   '   <ValidateProductID Sequence="700" />\n'+
   '   <CostInitialize Sequence="800" />\n'+
   '   <FileCost Sequence="900" />\n'+
   '   <IsolateComponents Sequence="990">RedirectedDllSupport</IsolateComponents>\n'+
   '   <CostFinalize Sequence="1000" />\n'+
   '   <SetODBCFolders Sequence="1100">NOT Installed</SetODBCFolders>\n'+
   '   <MigrateFeatureStates Sequence="1200" />\n'+
   '   <InstallValidate Sequence="1400" />\n'+
   '   <RemoveExistingProducts Sequence="1480">WARSETUP_PREVIOUSVERSIONFOUND</RemoveExistingProducts>\n'+
   '   <InstallInitialize Sequence="1500" />\n'+
   '   <ProcessComponents Sequence="1600" />\n'+
   '   <UnpublishComponents Sequence="1680" />\n'+
   '   <UnpublishFeatures Sequence="1800" />\n'+
   '   <StopServices Sequence="1900">VersionNT</StopServices>\n'+
   '   <DeleteServices Sequence="1980">VersionNT</DeleteServices>\n'+
   '   <UnregisterComPlus Sequence="2000" />\n'+
   '   <SelfUnregModules Sequence="2100" />\n'+
   '   <UnregisterTypeLibraries Sequence="2200" />\n'+
   '   <RemoveODBC Sequence="2300" />\n'+
   '   <UnregisterFonts Sequence="2400" />\n'+
   '   <RemoveRegistryValues Sequence="2600" />\n'+
   '   <UnregisterClassInfo Sequence="2700" />\n'+
   '   <UnregisterExtensionInfo Sequence="2800" />\n'+
   '   <UnregisterProgIdInfo Sequence="2900" />\n'+
   '   <UnregisterMIMEInfo Sequence="3000" />\n'+
   '   <RemoveIniValues Sequence="3100" />\n'+
   '   <RemoveShortcuts Sequence="3200" />\n'+
   '   <RemoveEnvironmentStrings Sequence="3300" />\n'+
   '   <RemoveDuplicateFiles Sequence="3400" />\n'+
   '   <RemoveFiles Sequence="3500" />\n'+
   '   <RemoveFolders Sequence="3600" />\n'+
   '   <CreateFolders Sequence="3700" />\n'+
    '  <MoveFiles Sequence="3800" />\n'+
    '  <InstallFiles Sequence="4000" />\n'+
    '  <DuplicateFiles Sequence="4100" />\n'+
    '  <PatchFiles Sequence="4200" />\n'+
    '  <BindImage Sequence="4300" />\n'+
    '  <CreateShortcuts Sequence="4500" />\n'+
    '  <RegisterClassInfo Sequence="4600" />\n'+
    '  <RegisterExtensionInfo Sequence="4700" />\n'+
    '  <RegisterProgIdInfo Sequence="4800" />\n'+
    '  <RegisterMIMEInfo Sequence="4900" />\n'+
    '  <WriteRegistryValues Sequence="5000" />\n'+
    '  <WriteIniValues Sequence="5100" />\n'+
    '  <WriteEnvironmentStrings Sequence="5200" />\n'+
    '  <RegisterFonts Sequence="5300" />\n'+
    '  <InstallODBC Sequence="5400" />\n'+
    '  <RegisterTypeLibraries Sequence="5500" />\n'+
    '  <SelfRegModules Sequence="5600" />\n'+
    '  <RegisterComPlus Sequence="5700" />\n'+
    '  <InstallServices Sequence="5800">VersionNT</InstallServices>\n'+
     ' <StartServices Sequence="5900">VersionNT</StartServices>\n'+
     ' <RegisterUser Sequence="6000" />\n'+
     ' <RegisterProduct Sequence="6100" />\n'+
     ' <PublishComponents Sequence="6200" />\n'+
     ' <PublishFeatures Sequence="6300" />\n'+
     ' <PublishProduct Sequence="6400" />\n'+
     ' <MsiPublishAssemblies Sequence="6500" />\n'+
     ' <MsiUnpublishAssemblies Sequence="6550" />\n'+
     ' <InstallFinalize Sequence="6600" />\n'+
     ' <Custom Action="ID20427" After="FileCost" />\n'+
   ' </InstallExecuteSequence>\n'+
   ' <CustomAction Id="ID20426" Property="WarSetup_PRODUCT" Value="*" HideTarget="no" />\n'+
   ' <InstallUISequence>\n'+
   '   <Custom Action="ID20426" After="CostFinalize" />\n'+
   '   <Custom Action="ID20427" After="FileCost" />\n'+
   ' </InstallUISequence>\n'+
   ' <AdvertiseExecuteSequence>\n'+
   '   <CostInitialize Sequence="800" />\n'+
   '   <CostFinalize Sequence="1000" />\n'+
    '  <InstallInitialize Sequence="1500" />\n'+
    '  <CreateShortcuts Sequence="4500" />\n'+
    '  <RegisterClassInfo Sequence="4600" />\n'+
    '  <RegisterExtensionInfo Sequence="4700" />\n'+
    '  <RegisterProgIdInfo Sequence="4800" />\n'+
    '  <RegisterMIMEInfo Sequence="4900" />\n'+
    '  <PublishComponents Sequence="6200" />\n'+
     ' <PublishFeatures Sequence="6300" />\n'+
     ' <PublishProduct Sequence="6400" />\n'+
    '  <MsiPublishAssemblies Sequence="6500" />\n'+
    '  <InstallFinalize Sequence="6600" />\n'+
    '</AdvertiseExecuteSequence>\n')

lin.append("""<CustomAction Id="ID20427" Property="TARGETDIR" Value="[APPLICATIONFOLDER]" HideTarget="no" />
    <Directory Id="TARGETDIR" Name="SourceDir">
      <Directory Id="ProgramMenuFolder" Name="Programs">""")
lin.append('    <Component Id="ID20430" Guid="*">'+
'          <RegistryValue Root="HKCU" Key="SOFTWARE\Faculty of Management Sience and Informatic University of Zilina\UML .FRI\Components\ID20430" Type="string" KeyPath="yes" Value="" />')
lin.append('          <RemoveFolder Id="ID20431" On="uninstall" />\n'+
'        </Component>\n'+
'        <Directory Id="ProgramMenuDir" Name="UML .FRI">\n'+
'          <Component Id="ID20432" Guid="*">\n'+
'            <RegistryValue Root="HKCU" Key="SOFTWARE\Faculty of Management Sience and Informatic University of Zilina\UML .FRI\Components\ID20432" Type="string" KeyPath="yes" Value="" />\n'+
'            <RemoveFolder Id="ID20433" On="uninstall" />\n'+
'          </Component>\n'+
'          <Component Id="UninstallShortcutComponent" Guid="*">\n'+
'            <RegistryValue Root="HKCU" Key="SOFTWARE\Faculty of Management Sience and Informatic University of Zilina\UML .FRI\Uninstall" Type="string" KeyPath="yes" Value="" />\n'+
'            <Shortcut Id="UninstallProduct" Name="Uninstall UML .FRI" Target="[System64Folder]msiexec.exe" Arguments="/X{'+str(product_id)+'}" Directory="ProgramMenuDir" Description="Uninstall UML .FRI" />\n'+
'            <RemoveFolder Id="RemoveShortcutFolder" On="uninstall" />\n'+
'          </Component>\n'+
'        </Directory>\n'+
'        <Directory Id="StartupFolder" Name="StartupFolder Directory">\n'+
'          <Component Id="ID20434" Guid="*">\n'+
'            <RegistryValue Root="HKCU" Key="SOFTWARE\Faculty of Management Sience and Informatic University of Zilina\UML .FRI\Components\ID20434" Type="string" KeyPath="yes" Value="" />\n'+
'            <RemoveFolder Id="ID20435" On="uninstall" />\n'+
'          </Component>\n'+
'        </Directory>\n'+
'      </Directory>\n'+
'      <Directory Id="AppDataFolder" Name="AppData">\n'+
'        <Component Id="ID20436" Guid="*">\n'+
'          <RegistryValue Root="HKCU" Key="SOFTWARE\Faculty of Management Sience and Informatic University of Zilina\UML .FRI\Components\ID20436" Type="string" KeyPath="yes" Value="" />\n'+
'          <RemoveFolder Id="ID20437" On="uninstall" />\n'+
'        </Component>\n'+
'        <Directory Id="Microsoft" Name="Microsoft">\n'+
'          <Component Id="ID20438" Guid="*">\n'+
'            <RegistryValue Root="HKCU" Key="SOFTWARE\Faculty of Management Sience and Informatic University of Zilina\UML .FRI\Components\ID20438" Type="string" KeyPath="yes" Value="" />\n'+
'            <RemoveFolder Id="ID20439" On="uninstall" />\n'+
'          </Component>\n'+
'          <Directory Id="AppMsInternetExplorer" Name="Internet Explorer">\n'+
'            <Component Id="ID20440" Guid="*">\n'+
'              <RegistryValue Root="HKCU" Key="SOFTWARE\Faculty of Management Sience and Informatic University of Zilina\UML .FRI\Components\ID20440" Type="string" KeyPath="yes" Value="" />\n'+
'              <RemoveFolder Id="ID20441" On="uninstall" />\n'+
'            </Component>\n'+
'            <Directory Id="QuickLaunchFolder" Name="Quick Launch">\n'+
'              <Component Id="ID20442" Guid="*">\n'+
'                <RegistryValue Root="HKCU" Key="SOFTWARE\Faculty of Management Sience and Informatic University of Zilina\UML .FRI\Components\ID20442" Type="string" KeyPath="yes" Value="" />\n'+
'                <RemoveFolder Id="ID20443" On="uninstall" />\n'+
'              </Component>\n'+
'            </Directory>\n'+
'          </Directory>\n'+
'        </Directory>\n'+
'      </Directory>\n'+
'      <Directory Id="DesktopFolder" Name="Desktop">\n'+
'        <Component Id="ID20428" Guid="*">\n'+
'          <RegistryValue Root="HKCU" Key="SOFTWARE\Faculty of Management Sience and Informatic University of Zilina\UML .FRI\Components\ID20428" Type="string" KeyPath="yes" Value="" />\n'+
'          <RemoveFolder Id="ID20429" On="uninstall" />\n'+
'        </Component>\n'+
'      </Directory>\n')
lin.append("""<Directory Id="ProgramFilesFolder" Name="Program Files Folder">
          <Directory Id="APPLICATIONFOLDER" Name="UML .FRI">""")
#===========================================================
#
#===========================================================
print "Generating WixFile"
print binary_files
path=binary_files
genfromtree(path,mainFeature)
lin.append("""</Directory>
            </Directory>
<Property Id="ApplicationFolderName" Value="UML .FRI" />
    <Property Id="WixAppFolder" Value="WixPerUserFolder" />
    <WixVariable Id="WixUILicenseRtf" Value="GNU General Public License (GPL) 2.0.rtf" />
    <WixVariable Id="WixUIBannerBmp" Value="MSIFiles\installat2.jpg" />
    <WixVariable Id="WixUIDialogBmp" Value="MSIFILES\installat.jpg" />
     <Feature Id="ID801655EA0B8A1C366E7183A0B0E69EF0" Title="UML .FRI" Level="1" Description="The complete package" AllowAdvertise="no" Absent="disallow" InstallDefault="local" ConfigurableDirectory="APPLICATIONFOLDER">
     <ComponentRef Id="ID1532" />
     <ComponentRef Id="ID20633" />
     <ComponentRef Id="ID20635" />
     <ComponentRef Id="UninstallShortcutComponent" />
        <ComponentRef Id="ID20428" />
      <ComponentRef Id="ID20430" />
      <ComponentRef Id="ID20432" />
      <ComponentRef Id="ID20434" />
      <ComponentRef Id="ID20436" />
      <ComponentRef Id="ID20438" />
      <ComponentRef Id="ID20440" />
      <ComponentRef Id="ID20442" />
    """)
for i in mainFeature:
    lin.append('<ComponentRef Id="'+str(i)+'" />\n')
lin.append('</Feature>\n <Feature Id="PROGRAM" Title="Addons" Level="1" AllowAdvertise="no" Description="The Main Executable" InstallDefault="local">')

for fet in features:
    level=1000
    if fet[0]=='uml':
        level=1
    else:
        level=1000

    lin.append('<Feature Id="'+getId()+'" Title=" '+names[fet[0]]+'"  AllowAdvertise="no" Level="'+str(level)+'" Description="Enter Description Here">')
    for f in fet[1]:
        
        lin.append('<ComponentRef Id="'+str(f)+'" />\n')
    lin.append("</Feature>")
lin.append("""</Feature> <UI>
      <UIRef Id="WixUI_Mondo" />
      <Publish Dialog="ExitDialog" Control="Finish" Event="DoAction" Value="LaunchApplication">WIXUI_EXITDIALOGOPTIONALCHECKBOX = 1 and NOT Installed</Publish>
      <UIRef Id="WixUI_ErrorProgressText" />
    </UI>
    <Property Id="WIXUI_EXITDIALOGOPTIONALCHECKBOXTEXT" Value="Launch UML .FRI" />
    <Property Id="WixShellExecTarget" Value="[#ID_736c205c_ef71_411b_84b4_359e285d7c74]" />
    <CustomAction Id="LaunchApplication" BinaryKey="WixCA" DllEntry="WixShellExec" Impersonate="yes" />
    <Property Id="ALLUSERS" Value="2" />
  </Product>
</Wix>""")
FILE = open(outputFile,"w")
FILE.writelines(lin)
for i in features:
    print i[0]






