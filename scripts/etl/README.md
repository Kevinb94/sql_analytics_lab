# NPPES ETL Download Script

This folder contains `download_nppes.py`, which downloads the NPPES monthly ZIP from CMS for the National Provider Identifier (NPI) registry (providers and their practice/location data), extracts it, and lays out files in the structure expected by the staging DML script.

## What `download_nppes.py` does

1. Builds the default CMS URL for the monthly NPPES ZIP:
   - If today is the 15th or later, it targets the current month.
   - If today is before the 15th, it targets the previous month.
   - URL pattern: `https://download.cms.gov/nppes/NPPES_Data_Dissemination_<Month>_<Year>.zip`
2. Downloads the ZIP in 1 MB chunks and prints progress.
3. Saves the ZIP under `data/NPI_Files/` by default.
4. Extracts the ZIP into:
   - `data/NPI_Files/NPPES_Data_Dissemination_<Month>_<Year>/`

## Why this prepares data for DML

`sql_queries/dml/load_nppes_staging.sql` scans `/data/NPI_Files` for the newest folder matching:

- `NPPES_Data_Dissemination_*`

Then it auto-selects the expected CSV files inside that folder:

- `npidata_pfile_*.csv`
- `pl_pfile_*.csv`
- `othername_pfile_*.csv`
- `endpoint_pfile_*.csv`

Because `download_nppes.py` preserves the CMS folder and filenames during extraction, the DML can locate and `COPY` those files into:

- `nppes.stg_nppes_npidata`
- `nppes.stg_nppes_practice_location`
- `nppes.stg_nppes_othername`
- `nppes.stg_nppes_endpoint`

## Usage

Run from project root:

```bash
python scripts/etl/download_nppes.py
```

Optional arguments:

```bash
python scripts/etl/download_nppes.py --url "https://download.cms.gov/nppes/NPPES_Data_Dissemination_January_2026.zip"
python scripts/etl/download_nppes.py --output-dir data/NPI_Files
```

## Typical flow

1. Download + extract monthly NPPES files:

```bash
python scripts/etl/download_nppes.py
```

2. Load extracted CSVs into staging tables:

```bash
docker compose exec -T postgres psql -U analytics_user -d analytics < sql_queries/dml/load_nppes_staging.sql
```
