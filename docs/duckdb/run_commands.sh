docker run --rm duckdb
.read /workspace/sql_queries/ddl/duckdb_create_npi_pfile.sql
DESCRIBE npidata_pfile;