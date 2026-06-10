# Demo Lab App - Flask, PostgreSQL, nginx, Grafana and Uptime Kuma

This is a small infrastructure lab project built with Docker Compose.

## Architecture

Browser → nginx → Flask app → PostgreSQL

Additional services:
- Grafana (Dashboards to visualize PostegresSQL data)
- Uptime Kuma (Used to check uptime of services used on demo lab app)

## Technologies

- Docker
- Docker Compose
- Flask
- PostgreSQL
- nginx
- Grafana
- Uptime Kuma

## Run

```bash
docker compose up -d --build
