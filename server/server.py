from flask import Flask
import psycopg2
import time

app = Flask(__name__)

def connect_postgres_db():
    retries = 5
    while retries > 0:
        try:
            con = psycopg2.connect(
                host='db',
                database='postgres',
                user='postgres',
                password='postgres',
            )
            return con
        except psycopg2.OperationalError as e:
            print("Database not ready. Retrying in 3 seconds... ")
            retries -= 1
            time.sleep(3)
    raise Exception ("COuld not connect to the database after 5 retries")

@app.route("/")
def index():
    conn = connect_postgres_db()
    cur = conn.cursor()
    cur.execute('SELECT version();')
    db_version = cur.fetchone()
    cur.close()
    conn.close()
    return f'''
        <h1>Hello from Flask!</h1>
        <p>PostgreSQL version: {db_version[0]}</p>
    '''

@app.route("/status")
def status():
    return {
        "service": "Telecom Monitoring Lab",
        "status": "OK",
        "database": "connected"
    }

@app.route("/metrics")
def metrics():
    return {
        "cmts_name": "cbr8_casa_1",
        "active_modems": 14520,
        "cmts_latency_ms": 18,
        "alarm_count": 3,
        "service_status": "OK"
    }

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
