import argparse
import subprocess
import uuid
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DIST_DIR = BASE_DIR / "dist"
INSTALLER_DIR = BASE_DIR / "installer"


NSIS_TEMPLATE = r"""
OutFile "{outfile}"
InstallDir "$PROGRAMFILES\\Keydrop Bot"
RequestExecutionLevel user
Icon "bot-icone.ico"
Section "Main"
  SetOutPath "$INSTDIR"
  File "{exe_path}"
  File "config.json"
  CreateShortCut "$DESKTOP\\Keydrop Bot.lnk" "$INSTDIR\\{exe_name}"
SectionEnd
"""

WXS_TEMPLATE = r"""
<?xml version=\"1.0\"?>
<Wix xmlns=\"http://schemas.microsoft.com/wix/2006/wi\">
  <Product Id=\"*\" Name=\"Keydrop Bot\" Version=\"{version}\" Manufacturer=\"Keydrop\" UpgradeCode=\"{upgrade}\">
    <Package InstallerVersion=\"200\" Compressed=\"yes\" InstallScope=\"perMachine\" />
    <Media Id=\"1\" Cabinet=\"cab1.cab\" EmbedCab=\"yes\"/>
    <Directory Id=\"TARGETDIR\" Name=\"SourceDir\">
      <Directory Id=\"ProgramFilesFolder\">
        <Directory Id=\"INSTALLDIR\" Name=\"Keydrop Bot\">
          <Component Id=\"MainExecutable\" Guid=\"{comp}\">
            <File Source=\"{exe_path}\" KeyPath=\"yes\" />
          </Component>
        </Directory>
      </Directory>
    </Directory>
    <Feature Id=\"Default\" Level=\"1\">
      <ComponentRef Id=\"MainExecutable\" />
    </Feature>
  </Product>
</Wix>
"""


def run(cmd):
    subprocess.check_call(cmd)


def build_installer(exe: Path, arch: str, version: str):
    DIST_DIR.mkdir(exist_ok=True)
    nsis_script = NSIS_TEMPLATE.format(
        outfile=DIST_DIR / f"KeydropBot_Installer_{arch}.exe",
        exe_path=exe,
        exe_name=exe.name,
    )
    nsis_file = INSTALLER_DIR / f"temp_{arch}.nsi"
    nsis_file.write_text(nsis_script, encoding="utf-8")
    run(["makensis", str(nsis_file)])

    wxs_script = WXS_TEMPLATE.format(
        version=version,
        upgrade=str(uuid.uuid4()),
        comp=str(uuid.uuid4()),
        exe_path=exe,
    )
    wxs_file = INSTALLER_DIR / f"temp_{arch}.wxs"
    wxs_file.write_text(wxs_script, encoding="utf-8")
    run(
        [
            "wixl",
            "-o",
            str(DIST_DIR / f"KeydropBot_Installer_{arch}.msi"),
            str(wxs_file),
        ]
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--exe", required=True)
    parser.add_argument("--arch", required=True)
    parser.add_argument("--version", default="1.0.0")
    args = parser.parse_args()

    build_installer(Path(args.exe), args.arch, args.version)


if __name__ == "__main__":
    main()
