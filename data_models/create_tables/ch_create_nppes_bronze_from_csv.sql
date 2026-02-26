-- Create raw Bronze tables in ClickHouse by inferring CSV headers
-- and forcing all inferred columns to String for ELT-style downstream transforms.
--
-- Prereq:
-- Create sample files (header + 1 data row) in /var/lib/clickhouse/user_files/ch_nppes
-- because ClickHouse file() can only read from user_files by default and
-- needs at least one data row to infer table structure.

CREATE DATABASE IF NOT EXISTS ch_bronze;

SET input_format_csv_use_best_effort_in_schema_inference = 0;

CREATE TABLE IF NOT EXISTS ch_bronze.ch_stg_nppes_npidata
ENGINE = MergeTree
ORDER BY tuple()
AS
SELECT *
FROM file(
  'ch_nppes/npidata_sample.csv',
  CSVWithNames
);

CREATE TABLE IF NOT EXISTS ch_bronze.ch_stg_nppes_othername
ENGINE = MergeTree
ORDER BY tuple()
AS
SELECT *
FROM file(
  'ch_nppes/othername_sample.csv',
  CSVWithNames
);

CREATE TABLE IF NOT EXISTS ch_bronze.ch_stg_nppes_endpoint
ENGINE = MergeTree
ORDER BY tuple()
AS
SELECT *
FROM file(
  'ch_nppes/endpoint_sample.csv',
  CSVWithNames
);

CREATE TABLE IF NOT EXISTS ch_bronze.ch_stg_nppes_pl
ENGINE = MergeTree
ORDER BY tuple()
AS
SELECT *
FROM file(
  'ch_nppes/pl_sample.csv',
  CSVWithNames
);
