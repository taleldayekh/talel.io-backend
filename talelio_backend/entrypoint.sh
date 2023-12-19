#!/usr/bin/env sh

cd ..
gunicorn talelio_backend.app:app -c ./talelio_backend/config/gunicorn.conf.py
