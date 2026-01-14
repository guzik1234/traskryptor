; Instalator Traskryptor - WinPython Edition (prawdziwie portable)

#define MyAppName "Traskryptor"
#define MyAppVersion "2.0"
#define MyAppPublisher "Traskryptor"

[Setup]
AppId={{B9C8D7E6-F5A4-3B2C-1D0E-9F8A7B6C5D4E}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName=C:\Traskryptor
DisableDirPage=yes
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
OutputDir=.
OutputBaseFilename=Traskryptor_WinPython_Installer
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
DisableWelcomePage=no
SetupIconFile=
DiskSpanning=no
; Wymagane około 1.2 GB miejsca na dysku
ExtraDiskSpaceRequired=209715200

[Languages]
Name: "polish"; MessagesFile: "compiler:Languages\Polish.isl"

[Files]
Source: "Traskryptor_WinPython\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\Uruchom_Traskryptor.bat"; WorkingDir: "{app}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\Uruchom_Traskryptor.bat"; WorkingDir: "{app}"

[Run]
Filename: "{app}\Uruchom_Traskryptor.bat"; Description: "Uruchom {#MyAppName}"; Flags: nowait postinstall skipifsilent shellexec

[Messages]
polish.WelcomeLabel2=Instalator zainstaluje [name/ver] na tym komputerze.%n%nAplikacja zawiera wszystko co potrzebne:%n- WinPython 3.13.11 (prawdziwie portable)%n- PyTorch 2.9.1 (AI)%n- OpenAI Whisper (rozpoznawanie mowy)%n- Wszystkie biblioteki tłumaczeniowe%n%nNie musisz instalować nic dodatkowego!

