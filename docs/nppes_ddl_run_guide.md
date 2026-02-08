# Run NPPES Create Table SQL

Run these commands from project root:

`c:\Users\kevin\dev\data_engineering\sql_analytics`

## 1) Start PostgreSQL

```bash
docker compose up -d postgres
```

## 2) Run the DDL script

```bash
docker compose exec -T postgres psql -U analytics_user -d analytics < sql_queries/ddl/create_nppes_tables.sql
```

## 3) Verify tables were created

```bash
docker compose exec postgres psql -U analytics_user -d analytics -c "\dt nppes.*"
```

Expected tables:

- `nppes.stg_nppes_npidata`
- `nppes.stg_nppes_practice_location`
- `nppes.stg_nppes_othername`
- `nppes.stg_nppes_endpoint`

## Optional: open interactive psql

```bash
docker compose exec postgres psql -U analytics_user -d analytics
```
