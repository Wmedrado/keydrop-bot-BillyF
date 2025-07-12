"""Remove local branches inactive for a given number of days."""

import datetime
import os
import subprocess


DAYS = int(os.environ.get("BRANCH_MAX_AGE_DAYS", 30))


def list_local_branches():
    out = subprocess.check_output(
        [
            "git",
            "for-each-ref",
            "--format=%(refname:short) %(committerdate:unix)",
            "refs/heads",
        ],
        text=True,
    )
    for line in out.splitlines():
        name, ts = line.split()
        yield name, datetime.datetime.fromtimestamp(int(ts))


def main() -> int:
    threshold = datetime.datetime.now() - datetime.timedelta(days=DAYS)
    for name, dt in list_local_branches():
        if name in ("main", "develop"):
            continue
        if dt < threshold:
            print(f"Deleting old branch {name}")
            subprocess.run(["git", "branch", "-D", name])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
