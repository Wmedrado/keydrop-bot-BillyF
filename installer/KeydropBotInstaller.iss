[Setup]
AppName=Keydrop Bot Professional
AppVersion=1.0.0
DefaultDirName={pf}\Keydrop Bot Professional
DefaultGroupName=Keydrop Bot Professional
UninstallDisplayIcon={app}\KeydropBot_Professional.exe
OutputBaseFilename=KeydropBotInstaller
SetupIconFile=bot-icone.ico
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\KeydropBot_Professional.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "config.json"; DestDir: "{app}"; Flags: ignoreversion
Source: "bot-icone.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Keydrop Bot Professional"; Filename: "{app}\KeydropBot_Professional.exe"; IconFilename: "{app}\bot-icone.ico"
Name: "{commondesktop}\Keydrop Bot Professional"; Filename: "{app}\KeydropBot_Professional.exe"; Tasks: desktopicon; IconFilename: "{app}\bot-icone.ico"

[Tasks]
Name: desktopicon; Description: "Criar \u00edcone na \u00c1rea de Trabalho"; Flags: unchecked
Name: startafter; Description: "Iniciar ap\u00f3s a instala\u00e7\u00e3o"; Flags: unchecked

[Run]
Filename: "{app}\KeydropBot_Professional.exe"; Description: "Iniciar Keydrop Bot"; Flags: nowait postinstall skipifsilent; Tasks: startafter
