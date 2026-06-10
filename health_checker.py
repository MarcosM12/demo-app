import requests
import json

services = {
    "nginx": "http://localhost",
    "flask_status": "http://localhost/status",
    "flask_metrics": "http://localhost/metrics",
    "grafana": "http://localhost:3000",
    "uptime_kuma": "http://localhost:3001"
}

results = {}
total_retries = 5

for name, url in services.items():
    for retry in total_retries:
        try:
            response = requests.get(url, timeout=5)
            results[name] = {
                "status": "UP" if response.status_code == 200 else "WARNING",
                "status_code": response.status_code
            }
        except requests.exceptions.RequestException as e:
            if retry <= 5:
                continue

            results[name] = {
                "status": "DOWN",
                "error": str(e)
            }

print(json.dumps(results, indent=2))