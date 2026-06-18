from time import sleep
import requests
import os
import time
from datetime import datetime, timezone
import requests
import psycopg2


DB_HOST = "127.0.0.1"
DB_PORT = 5432
DB_NAME = "postgres"
DB_USER =  "postgres"
DB_PASSWORD = "postgres"

MAX_RETRIES = 5
MAX_TIMEOUT = 3 

services = {
    "nginx": "http://localhost",
    "flask_status": "http://localhost/status",
    "flask_metrics": "http://localhost/metrics",
    "grafana": "http://localhost:3000",
    "uptime_kuma": "http://localhost:3001"
}

results = {}

def connect_db():
    retries=0
    while retries < MAX_RETRIES:
        try:
            con = psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                port=DB_PORT,
                user=DB_USER,
                password=DB_PASSWORD,
            )
            return con
        except psycopg2.OperationalError as e:
            print("Database not ready. Retrying in 3 seconds... ")
            retries += 1
            time.sleep(3)
    raise Exception ("Could not connect to the database after 5 retries")


def save_result(conn, result):
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO service_health_checks (
                checked_at,
                service_name,
                url,
                status,
                status_code,
                response_time_ms,
                error,
                number_of_retries
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            """,
            (
                result["checked_at"],
                result["service_name"],
                result["url"],
                result["status"],
                result["status_code"],
                result["response_time_ms"],
                result["error"],
                result["number_of_retries"]
            ),
        )
    conn.commit()


def main():

    conn = connect_db()

    for service_name, url in services.items():
        
        checked_at = datetime.now(timezone.utc)
        start_time = time.perf_counter()

        for attempt in range(1, MAX_RETRIES + 2):
            try:
                
                response = requests.get(url, timeout=MAX_TIMEOUT)
                response_time_ms = int((time.perf_counter() - start_time) * 1000)
                
                result = {
                    "checked_at": checked_at,
                    "service_name": service_name,
                    "url": url,
                    "status": "UP" if response.status_code == 200 else "WARNING",
                    "status_code": response.status_code,
                    "response_time_ms": response_time_ms,
                    "error": "None",
                    "number_of_retries": attempt,
                }
                save_result(conn, result)
                break

            except requests.exceptions.RequestException as e:
                if attempt <= MAX_RETRIES:
                    print(
                        f"status: Timeout for service: {service_name}. "
                        f"Attempt {attempt}/{MAX_RETRIES} failed. Retrying..."
                    )
                    sleep(1)
                    continue
                
                result = {
                    "checked_at": datetime.now(timezone.utc),
                    "service_name": service_name,
                    "url": url,
                    "status": "DOWN",
                    "status_code": "None",
                    "response_time_ms": "None",
                    "error": str(e),
                    "number_of_retries": MAX_RETRIES,
                }
                save_result(conn, result)

if __name__ == "__main__":
    main()