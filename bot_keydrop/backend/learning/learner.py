import json
from pathlib import Path
from typing import Dict

class ParticipationLearner:
    """Keep statistics of participation methods and learned selectors."""

    def __init__(self, state_file: str = None):
        self.state_file = Path(state_file or Path(__file__).parent / "learner_state.json")
        if self.state_file.exists():
            try:
                self.state = json.load(self.state_file.open())
            except Exception:
                self.state = {}
        else:
            self.state = {}
        self.state.setdefault("method_stats", {
            "css": {"success": 0, "fail": 0},
            "js": {"success": 0, "fail": 0},
            "image": {"success": 0, "fail": 0}
        })
        self.state["method_stats"].setdefault("learned", {"success": 0, "fail": 0})
        self.state.setdefault("learned_selector", None)

    def save(self):
        with self.state_file.open("w", encoding="utf-8") as f:
            json.dump(self.state, f, indent=2, ensure_ascii=False)

    def record_result(self, method: str, success: bool):
        stats: Dict[str, int] = self.state["method_stats"].setdefault(method, {"success": 0, "fail": 0})
        key = "success" if success else "fail"
        stats[key] += 1
        self.save()

    def set_selector(self, selector: str):
        self.state["learned_selector"] = selector
        self.save()

    def get_selector(self):
        return self.state.get("learned_selector")

    def best_method(self) -> str:
        stats = {k: v for k, v in self.state["method_stats"].items() if k != "learned"}
        return max(stats.keys(), key=lambda m: stats[m]["success"]) if stats else "css"
