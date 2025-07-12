import json
from pathlib import Path
from typing import Dict
import logging

logger = logging.getLogger(__name__)

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
            "image": {"success": 0, "fail": 0},
            "coordinates": {"success": 0, "fail": 0}
        })
        self.state["method_stats"].setdefault("learned", {"success": 0, "fail": 0})
        self.state["method_stats"].setdefault("text", {"success": 0, "fail": 0})
        self.state.setdefault("learned_selector", None)
        self.state.setdefault("tab_best_method", {})
        self.state.setdefault("tab_learned_selector", {})
        self.state.setdefault("tab_coordinates", {})

    def save(self):
        try:
            with self.state_file.open("w", encoding="utf-8") as f:
                json.dump(self.state, f, indent=2, ensure_ascii=False)
        except Exception:
            logger.exception("Erro ao salvar estado do aprendizado")

    def record_result(self, method: str, success: bool, tab_id: int = None):
        stats: Dict[str, int] = self.state["method_stats"].setdefault(method, {"success": 0, "fail": 0})
        key = "success" if success else "fail"
        stats[key] += 1
        if success and tab_id is not None:
            self.state.setdefault("tab_best_method", {})[str(tab_id)] = method
        self.save()

    def set_selector(self, selector: str, tab_id: int = None):
        if tab_id is None:
            self.state["learned_selector"] = selector
        else:
            self.state.setdefault("tab_learned_selector", {})[str(tab_id)] = selector
        self.save()

    def get_selector(self, tab_id: int = None):
        if tab_id is not None:
            return self.state.get("tab_learned_selector", {}).get(str(tab_id))
        return self.state.get("learned_selector")

    def best_method(self, tab_id: int = None) -> str:
        if tab_id is not None:
            method = self.state.get("tab_best_method", {}).get(str(tab_id))
            if method:
                return method
        stats = {k: v for k, v in self.state["method_stats"].items() if k != "learned"}
        return max(stats.keys(), key=lambda m: stats[m]["success"]) if stats else "css"

    def set_coordinates(self, tab_id: int, x: float, y: float):
        self.state.setdefault("tab_coordinates", {})[str(tab_id)] = [x, y]
        self.save()

    def get_coordinates(self, tab_id: int):
        return self.state.get("tab_coordinates", {}).get(str(tab_id))
