# PostgreSQL Container Quickstart

Run these commands from the project root:

`c:\Users\kevin\dev\data_engineering\sql_analytics`

## 1) Start PostgreSQL

```bash
docker compose up -d postgres
```

## 2) Check container status

```bash
docker compose ps
```

Look for the `postgres` service with a healthy/running status.

## 3) Check Postgres logs (optional)

```bash
docker compose logs -f postgres
```

## 4) Open psql inside the container

```bash
docker compose exec postgres psql -U analytics_user -d analytics
```

## 5) Run quick validation queries

```sql
SELECT version();
SELECT current_database(), current_user;
```

## 6) Exit psql

```sql
\q
```

## 7) Stop PostgreSQL

```bash
docker compose stop postgres
```
