import json
from bot_keydrop.backend.system_monitor.monitor import create_environment_snapshot

def test_environment_snapshot(tmp_path):
    cfg = {"version": "test"}
    snap_path = tmp_path / "snap.json"
    result = create_environment_snapshot(cfg, path=str(snap_path))
    assert result == snap_path
    data = json.loads(snap_path.read_text())
    assert data["config"]["version"] == "test"

