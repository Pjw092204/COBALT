#!/bin/sh
# Production entry for Railway/Docker (Gunicorn WSGI — not Flask dev server)
set -e
PORT="${PORT:-5000}"
exec gunicorn main:app \
  --bind "0.0.0.0:${PORT}" \
  --workers 2 \
  --threads 2 \
  --timeout 120 \
  --access-logfile - \
  --error-logfile -
