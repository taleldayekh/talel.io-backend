#!/usr/bin/env sh

cd talelio_backend
alembic upgrade head

# Move the PostgreSQL backup script for the backup cron
# job to the scripts directory used as a Docker volume.
cd ..
# mv backup_postgres_db.sh scripts/

gunicorn talelio_backend.app:app -c ./talelio_backend/config/gunicorn.conf.py
