#!/bin/sh
set -e

psql -v ON_ERROR_STOP=1 \
  --username "$POSTGRES_USER" \
  --dbname "$POSTGRES_DB" \
  -v app_pw="$APP_DB_PASSWORD" \
  -v ro_pw="$CONSULTA_DB_PASSWORD" \
  -v adm_pw="$ADMIN_DB_PASSWORD" \
  -f /scripts/permisos.sql
