# ClickHouse Container Quickstart

Run these commands from the project root:

`c:\Users\kevin\dev\data_engineering\sql_analytics`

## 1) Start ClickHouse

```bash
docker compose up -d clickhouse
```

## 2) Check container status

```bash
docker compose ps
```

Look for the `clickhouse` service with a healthy/running status.

## 3) Check ClickHouse logs (optional)

```bash
docker compose logs -f clickhouse
```

## 4) Open clickhouse-client inside the container

```bash
docker compose exec clickhouse clickhouse-client
```

## 5) Run quick validation queries

```sql
SELECT version();
SELECT currentDatabase(), currentUser();
SELECT 1;
```

## 6) Exit clickhouse-client

```sql
exit
```

## 7) Stop ClickHouse

```bash
docker compose stop clickhouse
```
