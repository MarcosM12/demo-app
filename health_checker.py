from time import sleep

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
    for attempt in range(1, total_retries + 2):
        try:
            response = requests.get(url, timeout=3)
            results[name] = {
                "status": "UP" if response.status_code == 200 else "WARNING",
                "status_code": response.status_code
            }
            break
        except requests.exceptions.RequestException as e:
            if attempt <= total_retries:
                print(
                    f"status: Timeout for service: {name}. "
                    f"Attempt {attempt}/{total_retries} failed. Retrying..."
                )
                sleep(1)
                continue
            
            results[name] = {
                "status": "DOWN",
                "error": str(e),
            }

print(json.dumps(results, indent=2))