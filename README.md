# SQL Analytics Lab

A local SQL practice environment using Docker to explore ingestion and
analytics patterns across multiple database engines.

------------------------------------------------------------------------

## Databases

### PostgreSQL

Schema-first staging database. - Explicit table definitions -
`COPY`-based bulk ingestion - Strong typing and structured ETL workflows

### DuckDB

Lightweight analytical engine. - Direct CSV ingestion - Schema-on-read
exploration - Fast local analytics development

### ClickHouse

Columnar OLAP engine. - High-performance aggregations - Large analytical
workloads - Query performance comparison

------------------------------------------------------------------------

## Dataset: CMS NPPES NPI Data

This project uses real-world data from the **CMS National Plan &
Provider Enumeration System (NPPES)**.

The monthly dissemination files contain:

-   Provider identifiers (NPI)
-   Provider names
-   Practice locations
-   Taxonomy codes
-   Other identifiers
-   Endpoint information

Source: https://download.cms.gov/nppes/

Monthly file pattern:
NPPES_Data_Dissemination\_`<Month>`{=html}\_`<Year>`{=html}.zip

Example:
https://download.cms.gov/nppes/NPPES_Data_Dissemination_January_2026.zip

------------------------------------------------------------------------

## Canonical Data Layout

After download and extraction, CSV files are organized into canonical
folders:

    data/NPI_Files/
    ├── npidata_pfile/
    ├── pl_pfile/
    ├── othername_pfile/
    └── endpoint_pfile/

Each folder contains only its relevant CSV type (excluding
\*\_fileheader.csv files).

This structure allows: - Clean separation of file types - Easier
ingestion into DuckDB - Controlled `COPY` loading into PostgreSQL
staging tables - Repeatable monthly updates

------------------------------------------------------------------------

## Project Structure

    .
    ├── docker-compose.yml
    ├── data/NPI_Files/
    ├── databases/
    │   ├── postgres/
    │   ├── clickhouse/
    │   └── duckdb/
    ├── scripts/etl/
    └── sql_queries/
        ├── create_tables/
        └── staging_views/

------------------------------------------------------------------------

## Getting Started

    cp .env.example .env
    docker compose up -d

Open DuckDB:

    docker compose run --rm duckdb

Download NPPES data:

    docker compose run --rm python_etl python download_nppes.py
