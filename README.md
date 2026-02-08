# SQL Analytics Practice (PostgreSQL + ClickHouse + Docker)

This project is for practicing SQL queries for analytics and writing performant queries using PostgreSQL and ClickHouse running in Docker.

## Project structure

- `docker-compose.yml`: Local stack with PostgreSQL + ClickHouse + Python environment.
- `.env`: Local environment values used by Docker Compose.
- `databases/postgres/`: Persistent PostgreSQL data directory.
- `databases/clickhouse/`: Persistent ClickHouse data directory.
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
CLICKHOUSE_HTTP_PORT=8123
CLICKHOUSE_NATIVE_PORT=9000
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

4. Connect with ClickHouse client (if installed):

   ```bash
   clickhouse-client --host localhost --port 9000 --query "SELECT version()"
   ```

5. Stop services:

   ```bash
   docker compose down
   ```

## Data

This repository uses real-world National Provider Identifier (NPI) data from the CMS NPPES monthly dissemination files.

- Source: CMS NPPES monthly ZIP files at `https://download.cms.gov/nppes/`
- Monthly file pattern: `NPPES_Data_Dissemination_<Month>_<Year>.zip`
- Example: `https://download.cms.gov/nppes/NPPES_Data_Dissemination_January_2026.zip`

Data is requested by running the Python download script in the `python_etl` container:

```bash
docker compose run --rm python_etl python download_nppes.py
```

The downloaded archives and extracted files are stored under `data/NPI_Files/` and then used for loading into staging/bronze tables.
