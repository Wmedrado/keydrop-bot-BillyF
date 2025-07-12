import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

THRESHOLDS = {
    "execution_time": 0.10,  # 10% slower is regression
    "success_rate": 0.05,    # 5% drop is regression
}


def parse_metrics_diff(path: Path) -> Dict[str, Tuple[float, float]]:
    """Parse metrics from build_metrics_diff.md if present."""
    metrics: Dict[str, Tuple[float, float]] = {}
    if not path.exists():
        return metrics
    pattern = re.compile(
        r"([A-Za-z_ ]+):?\s*(\d+(?:\.\d+)?)\s*->\s*(\d+(?:\.\d+)?)"
    )
    for line in path.read_text(encoding="utf-8").splitlines():
        m = pattern.search(line)
        if m:
            key = m.group(1).strip().lower().replace(" ", "_")
            old = float(m.group(2))
            new = float(m.group(3))
            metrics[key] = (old, new)
    return metrics


def analyze_logs(path: Path) -> List[str]:
    """Search log for suspicious patterns."""
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8").lower()
    issues: List[str] = []
    if "sleep(" in text or "delay" in text:
        issues.append("possible artificial delay added")
    if "fallback" in text:
        issues.append("fallback method detected")
    return issues


def evaluate(metrics: Dict[str, Tuple[float, float]]) -> Tuple[str, List[str]]:
    issues: List[str] = []
    improvement = False
    for key, (old, new) in metrics.items():
        if key == "execution_time":
            if new > old * (1 + THRESHOLDS["execution_time"]):
                issues.append(f"execution_time increased from {old} to {new}")
            elif new < old:
                improvement = True
        elif key == "success_rate":
            if new < old * (1 - THRESHOLDS["success_rate"]):
                issues.append(f"success_rate decreased from {old} to {new}")
            elif new > old:
                improvement = True
        elif key in {"retries", "exceptions", "ram_usage"}:
            if new > old:
                issues.append(f"{key} increased from {old} to {new}")
            elif new < old:
                improvement = True
    if issues:
        classification = "Regressao Critica"
    elif improvement:
        classification = "Melhoria"
    else:
        classification = "Neutro"
    return classification, issues


def run_check(repo_root: Path) -> str:
    metrics = parse_metrics_diff(repo_root / "build_metrics_diff.md")
    classification, issues = evaluate(metrics)
    issues.extend(analyze_logs(repo_root / "logs" / "bot_engine.log"))

    report_path = repo_root / "ci" / "regression_intelligence_report.md"
    lines = ["# Regression Intelligence Report", ""]
    if issues:
        lines.append("## Issues Detected")
        for item in issues:
            lines.append(f"- {item}")
    else:
        lines.append("No issues detected.")
    lines.append("")
    lines.append(f"**Classification:** {classification}")
    report_path.write_text("\n".join(lines), encoding="utf-8")
    return classification


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    classification = run_check(repo_root)
    if classification == "Regressao Critica":
        print("Regression detected: review required")
        return 1
    print(f"Regression check result: {classification}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
