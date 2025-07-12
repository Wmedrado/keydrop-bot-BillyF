from datetime import datetime
from pathlib import Path
import json
import shutil

BACKUP_DIR = Path("backups")


def backup_file(file_path: str):
    path = Path(file_path)
    if path.exists():
        BACKUP_DIR.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M")
        backup = BACKUP_DIR / f"{path.stem}_{timestamp}{path.suffix}"
        try:
            shutil.copy2(path, backup)
        except Exception:
            pass
        return backup
    return None


def safe_save_json(file_path: str, data):
    backup_file(file_path)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
