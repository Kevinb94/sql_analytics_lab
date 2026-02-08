docker compose exec -T clickhouse clickhouse-client --query "SELECT * FROM ch_bronze.ch_stg_nppes_npidata LIMIT 1"

docker compose exec -T clickhouse clickhouse-client --query "SELECT * FROM ch_bronze.ch_stg_nppes_othername LIMIT 1"

docker compose exec -T clickhouse clickhouse-client --query "SELECT * FROM ch_bronze.ch_stg_nppes_endpoint LIMIT 1"

docker compose exec -T clickhouse clickhouse-client --query "SELECT * FROM ch_bronze.ch_stg_nppes_pl LIMIT 1"
