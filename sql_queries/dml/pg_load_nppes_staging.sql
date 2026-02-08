\set ON_ERROR_STOP on

-- Data load script (DML/ETL), not DDL.
-- Uses server-side COPY from files mounted into the postgres container at /data.

TRUNCATE TABLE
  nppes.stg_nppes_npidata,
  nppes.stg_nppes_practice_location,
  nppes.stg_nppes_othername,
  nppes.stg_nppes_endpoint;

DO $$
DECLARE
  base_dir text := '/data/NPI_Files';
  nppes_dir text;
  npidata_file text;
  pl_file text;
  othername_file text;
  endpoint_file text;
BEGIN
  SELECT base_dir || '/' || d
  INTO nppes_dir
  FROM pg_ls_dir(base_dir) AS d
  WHERE d LIKE 'NPPES_Data_Dissemination_%'
  ORDER BY (pg_stat_file(base_dir || '/' || d)).modification DESC
  LIMIT 1;

  IF nppes_dir IS NULL THEN
    RAISE EXCEPTION 'No NPPES_Data_Dissemination_* folder found under %', base_dir;
  END IF;

  SELECT nppes_dir || '/' || f
  INTO npidata_file
  FROM pg_ls_dir(nppes_dir) AS f
  WHERE f LIKE 'npidata_pfile_%.csv'
    AND f NOT LIKE '%_fileheader.csv'
  ORDER BY f DESC
  LIMIT 1;

  SELECT nppes_dir || '/' || f
  INTO pl_file
  FROM pg_ls_dir(nppes_dir) AS f
  WHERE f LIKE 'pl_pfile_%.csv'
    AND f NOT LIKE '%_fileheader.csv'
  ORDER BY f DESC
  LIMIT 1;

  SELECT nppes_dir || '/' || f
  INTO othername_file
  FROM pg_ls_dir(nppes_dir) AS f
  WHERE f LIKE 'othername_pfile_%.csv'
    AND f NOT LIKE '%_fileheader.csv'
  ORDER BY f DESC
  LIMIT 1;

  SELECT nppes_dir || '/' || f
  INTO endpoint_file
  FROM pg_ls_dir(nppes_dir) AS f
  WHERE f LIKE 'endpoint_pfile_%.csv'
    AND f NOT LIKE '%_fileheader.csv'
  ORDER BY f DESC
  LIMIT 1;

  IF npidata_file IS NULL OR pl_file IS NULL OR othername_file IS NULL OR endpoint_file IS NULL THEN
    RAISE EXCEPTION 'Missing one or more expected NPPES CSV files in %', nppes_dir;
  END IF;

  RAISE NOTICE 'Using NPPES folder: %', nppes_dir;
  RAISE NOTICE 'npidata file: %', npidata_file;
  RAISE NOTICE 'pl file: %', pl_file;
  RAISE NOTICE 'othername file: %', othername_file;
  RAISE NOTICE 'endpoint file: %', endpoint_file;

  EXECUTE format(
    'COPY nppes.stg_nppes_npidata FROM %L WITH (FORMAT csv, HEADER true, NULL '''', ENCODING ''UTF8'')',
    npidata_file
  );
  EXECUTE format(
    'COPY nppes.stg_nppes_practice_location FROM %L WITH (FORMAT csv, HEADER true, NULL '''', ENCODING ''UTF8'')',
    pl_file
  );
  EXECUTE format(
    'COPY nppes.stg_nppes_othername FROM %L WITH (FORMAT csv, HEADER true, NULL '''', ENCODING ''UTF8'')',
    othername_file
  );
  EXECUTE format(
    'COPY nppes.stg_nppes_endpoint FROM %L WITH (FORMAT csv, HEADER true, NULL '''', ENCODING ''UTF8'')',
    endpoint_file
  );
END $$;

ANALYZE nppes.stg_nppes_npidata;
ANALYZE nppes.stg_nppes_practice_location;
ANALYZE nppes.stg_nppes_othername;
ANALYZE nppes.stg_nppes_endpoint;
