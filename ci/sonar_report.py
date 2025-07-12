import base64
import json
import os
import urllib.request

project_key = os.getenv("SONAR_PROJECT_KEY", "keydrop-bot")
organization = os.getenv("SONAR_ORGANIZATION", "your-org")
sonar_token = os.getenv("SONAR_TOKEN")

metrics = "duplicated_lines_density,code_smells,cognitive_complexity"

measure_url = (
    "https://sonarcloud.io/api/measures/component?component="
    f"{project_key}&metricKeys={metrics}"
)
status_url = (
    "https://sonarcloud.io/api/qualitygates/project_status?projectKey="
    f"{project_key}"
)

headers = {}
if sonar_token:
    token = base64.b64encode(f"{sonar_token}:".encode()).decode()
    headers["Authorization"] = f"Basic {token}"

req = urllib.request.Request(measure_url, headers=headers)
with urllib.request.urlopen(req) as resp:
    data = json.load(resp)

measures = {m["metric"]: m["value"] for m in data.get("component", {}).get("measures", [])}

req = urllib.request.Request(status_url, headers=headers)
with urllib.request.urlopen(req) as resp:
    status_data = json.load(resp)

status = status_data.get("projectStatus", {}).get("status")

print("SonarCloud Quality Gate:", status)
for metric, value in measures.items():
    print(f"{metric}: {value}")
