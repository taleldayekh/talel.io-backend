#!/usr/bin/env sh

gunicorn talelio_backend.app:app -c ./talelio_backend/config/gunicorn.conf.py
