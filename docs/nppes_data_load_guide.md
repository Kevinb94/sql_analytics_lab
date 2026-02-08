# Run NPPES Staging Load SQL

Run these commands from project root:

`c:\Users\kevin\dev\data_engineering\sql_analytics`

## 1) Make sure Postgres is running

```bash
docker compose up -d postgres
```

## 2) Run the staging load script

```bash
docker compose exec -T postgres psql -U analytics_user -d analytics < sql_queries/dml/load_nppes_staging.sql
```

What this script does:
- truncates staging tables
- finds the latest `NPPES_Data_Dissemination_*` folder under `/data/NPI_Files`
- auto-detects the monthly CSV file names
- runs `COPY` into all staging tables
- runs `ANALYZE`

## 3) Validate row counts

```bash
docker compose exec postgres psql -U analytics_user -d analytics -c "
SELECT 'stg_nppes_npidata' AS table_name, count(*) FROM nppes.stg_nppes_npidata
UNION ALL
SELECT 'stg_nppes_practice_location', count(*) FROM nppes.stg_nppes_practice_location
UNION ALL
SELECT 'stg_nppes_othername', count(*) FROM nppes.stg_nppes_othername
UNION ALL
SELECT 'stg_nppes_endpoint', count(*) FROM nppes.stg_nppes_endpoint;
"
```


docker compose exec postgres psql -U analytics_user -d analytics -c "SELECT 'stg_nppes_othername', count(*) FROM nppes.stg_nppes_othername"

docker compose exec postgres psql -U analytics_user -d analytics -c "SELECT 'stg_nppes_npidata' AS table_name, count(*) FROM nppes.stg_nppes_npidata"