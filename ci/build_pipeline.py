import argparse
import subprocess
import shutil
import sys
import os
import json
import time
from pathlib import Path


def run(cmd, cwd=None):
    """Run command and stream output."""
    print(f"[RUN] {' '.join(cmd)}")
    proc = subprocess.run(cmd, cwd=cwd, text=True)
    return proc.returncode


def parse_coverage(xml_path: Path) -> float:
    if not xml_path.exists():
        return 0.0
    import xml.etree.ElementTree as ET
    tree = ET.parse(xml_path)
    root = tree.getroot()
    rate = float(root.get('line-rate', 0)) * 100
    return round(rate, 2)


def main():
    parser = argparse.ArgumentParser(description="Run build pipeline")
    parser.add_argument('--snapshot', action='store_true', help='create snapshot build')
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    build_dir = repo_root / 'build'
    build_dir.mkdir(exist_ok=True)

    if args.snapshot:
        snap_dir = build_dir / f'snapshot_{int(time.time())}'
        if snap_dir.exists():
            shutil.rmtree(snap_dir)
        shutil.copytree(repo_root, snap_dir, ignore=shutil.ignore_patterns('.git', 'build'))
        work_dir = snap_dir
    else:
        work_dir = repo_root

    # Linting
    run(['flake8', 'bot_keydrop', 'tests', 'launcher.py'], cwd=work_dir)
    run(['pylint', 'bot_keydrop', 'launcher.py'], cwd=work_dir)

    # Tests with coverage
    cov_file = work_dir / 'coverage.xml'
    start = time.time()
    run(['pytest', '--cov=bot_keydrop', '--cov-report', 'xml', '--html', str(build_dir / 'tests_report.html'), 'tests'], cwd=work_dir)
    duration = time.time() - start
    coverage = parse_coverage(cov_file)

    # Git info
    commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True, cwd=repo_root).strip()
    author = subprocess.check_output(['git', 'log', '-1', '--pretty=format:%an <%ae>'], text=True, cwd=repo_root).strip()

    info = {
        'commit': commit,
        'author': author,
        'coverage': coverage,
        'test_duration': round(duration, 2),
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
    }
    with open(build_dir / 'build_info.txt', 'w') as f:
        json.dump(info, f, indent=2)

    print("Build info written", info)


if __name__ == '__main__':
    main()
