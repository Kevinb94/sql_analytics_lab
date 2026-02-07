# SQL Analytics Practice (PostgreSQL + Docker)

This project is for practicing SQL queries for analytics and writing performant queries using PostgreSQL running in Docker.

## Project structure

- `docker-compose.yml`: Local stack with PostgreSQL + Python environment.
- `.env`: Local environment values used by Docker Compose.
- `databases/postgres/`: Persistent PostgreSQL data directory.
- `docker/python/`: Python Docker image for data loading scripts.
- `sql_queries/ddl/`: SQL schema setup scripts.
- `sql_queries/dql/`: Query practice scripts.

## Prerequisites

- Docker Desktop (or Docker Engine + Docker Compose v2)
- Optional: VS Code + Dev Containers extension

## Environment variables

Copy `.env.example` to `.env` before starting services:

```bash
cp .env.example .env
```

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

The root `.env` file is used by Docker Compose:

```env
POSTGRES_DB=analytics
POSTGRES_USER=analytics_user
POSTGRES_PASSWORD=analytics_password
POSTGRES_PORT=5432
```

You can change values as needed.

## Run with Docker Compose

1. Start services:

   ```bash
   docker compose up -d
   ```

2. Check container health:

   ```bash
   docker compose ps
   ```

3. Connect with `psql` from your host (if installed):

   ```bash
   psql -h localhost -p 5432 -U analytics_user -d analytics
   ```

4. Stop services:

   ```bash
   docker compose down
   ```

## Python service for loading data

The `python_etl` service includes `pandas`, `psycopg` (PostgreSQL driver), and `SQLAlchemy`.

1. Open a shell in the Python container:

   ```bash
   docker compose exec python_etl bash
   ```

2. Run a script from your repo (example):

   ```bash
   docker compose exec python_etl python load_data.py
   ```
