# ClickHouse Table Verification Queries

Use these commands from the project root (`sql_analytics`) to verify ClickHouse status and table creation.

## 1) Verify ClickHouse container is running

```powershell
docker compose ps clickhouse
```

## 2) Verify databases exist

```powershell
docker compose exec -T clickhouse clickhouse-client --query "SHOW DATABASES"
```

## 3) Verify tables in `ch_bronze`

```powershell
docker compose exec -T clickhouse clickhouse-client --query "SHOW TABLES FROM ch_bronze"
```

Alternative (explicit system table query):

```powershell
docker compose exec -T clickhouse clickhouse-client --query "SELECT name FROM system.tables WHERE database='ch_bronze' ORDER BY name"
```

## 4) Check row count for created table

```powershell
docker compose exec -T clickhouse clickhouse-client --query "SELECT count() AS row_count FROM ch_bronze.ch_stg_nppes_npidata"
```
