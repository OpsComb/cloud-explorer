#!/bin/sh
set -e

python3 manage.py collectstatic

python3 manage.py migrate

# Start service
exec "$@"
