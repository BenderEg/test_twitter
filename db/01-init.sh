#!/bin/bash
set -e
psql -U "$POSTGRES__USER" -d "$POSTGRES__DB" <<-EOSQL
  CREATE SCHEMA IF NOT EXISTS "$POSTGRES__SCHEMA";
  ALTER ROLE "$POSTGRES__USER" SET search_path TO content,public;
  COMMIT;
EOSQL