from datetime import datetime
from pathlib import Path
import shutil

BACKUP_DIR = Path("backups")
BACKUP_DIR.mkdir(exist_ok=True)


def backup_arquivo(caminho: Path) -> Path:
    """Create timestamped backup of the file."""
    if caminho.exists():
        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M")
        dest = BACKUP_DIR / f"{caminho.stem}_{timestamp}{caminho.suffix}"
        shutil.copy2(caminho, dest)
        return dest
    return caminho


def restaurar_arquivo(caminho: Path) -> Path | None:
    """Restore file from latest backup if missing."""
    if caminho.exists():
        return caminho
    pattern = f"{caminho.stem}_*{caminho.suffix}"
    backups = sorted(BACKUP_DIR.glob(pattern), reverse=True)
    if backups:
        shutil.copy2(backups[0], caminho)
        return backups[0]
    return None

