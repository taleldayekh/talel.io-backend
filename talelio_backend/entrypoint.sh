#!/usr/bin/env sh

cd talelio_backend
alembic upgrade head
cd ..

gunicorn talelio_backend.app:app -c ./talelio_backend/config/gunicorn.conf.py
