import subprocess

subprocess.run(["bandit", "-r", "."], check=True)
