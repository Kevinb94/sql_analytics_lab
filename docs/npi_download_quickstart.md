# NPI Download Script Quickstart

Run commands from project root:

`c:\Users\kevin\dev\data_engineering\sql_analytics`

## 1) Run default monthly download

```bash
docker compose run --rm python_etl python download_nppes.py
```

This uses the script's month-selection rule:
- if day >= 15: current month
- if day < 15: previous month

## 2) Optional: override URL manually

```bash
docker compose run --rm python_etl python download_nppes.py --url "https://download.cms.gov/nppes/NPPES_Data_Dissemination_January_2026.zip"
```

## 3) Output location

Downloaded files are written to:

`data/NPI_Files/`
