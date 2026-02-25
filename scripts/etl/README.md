# NPPES ETL – Monthly Download & Load

This project downloads the monthly NPPES (NPI registry) dataset from CMS, extracts it, and prepares it for staging in Postgres.

---

## What the Script Does

`scripts/etl/download_nppes.py`:

1. Automatically determines the correct monthly CMS ZIP:
   - If today is before the 15th → previous month
   - If today is the 15th or later → current month
2. Downloads the ZIP from:
   `https://download.cms.gov/nppes/NPPES_Data_Dissemination_<Month>_<Year>.zip`
3. Extracts the ZIP and organizes the raw CSVs into the canonical folders under `data/npi_files/`.

---

## Canonical Folder Structure (Expected)

After running the script, your data should look like this:

```
data/
└── npi_files/
    ├── npidata_pfile/
    │   └── npidata_pfile_*.csv
    ├── pl_pfile/
    │   └── pl_pfile_*.csv
    ├── othername_pfile/
    │   └── othername_pfile_*.csv
    └── endpoint_pfile/
        └── endpoint_pfile_*.csv
```

This structure is required so the staging load script can reliably find the newest files to load.

---

## Tables Loaded

The staging script loads data into:

- `nppes.stg_nppes_npidata`
- `nppes.stg_nppes_practice_location`
- `nppes.stg_nppes_othername`
- `nppes.stg_nppes_endpoint`

---

## Usage

Run from the project root:

```bash
python scripts/etl/download_nppes.py
```

Optional:

```bash
python scripts/etl/download_nppes.py --url "<custom CMS zip url>"
```

---

## Typical Workflow

1) Download + extract + lay out canonical folders:

```bash
python scripts/etl/download_nppes.py
```

2) Load into Postgres staging:

```bash
docker compose exec -T postgres psql -U analytics_user -d analytics < sql_queries/dml/pg_load_nppes_staging.sql
```
