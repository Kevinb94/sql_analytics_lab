# Data Folder Guide

This folder stores local data files used by the project.  
For NPI registry data (providers and practice/location files), use the NPPES download script to populate `data/NPI_Files`.

Run from project root:

```bash
python scripts/etl/download_nppes.py
```

After download and extraction, you can load staging tables with:

```bash
docker compose exec -T postgres psql -U analytics_user -d analytics < sql_queries/dml/load_nppes_staging.sql
```

More details are in:

- `scripts/etl/README.md`
