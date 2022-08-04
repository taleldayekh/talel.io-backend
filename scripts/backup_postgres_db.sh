#!/usr/bin/env sh

POSTGRES_CONTAINER_ID=$(docker ps -qf "name=.*postgres.*")
TIMESTAMP=$(Date +%y%m%d-%H%M%S)
DB_BACKUP_NAME="talelio-db-backup-${TIMESTAMP}.sql"
