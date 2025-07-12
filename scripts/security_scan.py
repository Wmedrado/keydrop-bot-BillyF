import subprocess

subprocess.run([
    "bandit",
    "-r",
    ".",
    "--severity-level",
    "medium",
], check=True)
