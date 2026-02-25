CREATE OR REPLACE TABLE npidata_pfile AS
SELECT *
FROM read_csv_auto(
  '/workspace/data/npi_files/npidata_pfile/*.csv',
  HEADER=true,
  filename=true,
  ALL_VARCHAR=true
)
WHERE filename NOT LIKE '%_fileheader.csv';