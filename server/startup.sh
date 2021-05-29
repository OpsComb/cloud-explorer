#!/bin/bash

NAME="cloud_explorer"                                             # Name of the application (*)
DJANGODIR=/usr/local/src/cloud_explorer                           # Django project directory (*)
USER=root                                                         # the user to run as (*)
NUM_WORKERS=4
TIMEOUT=300
DJANGO_SETTINGS_MODULE=cloud_explorer.settings                    # which settings file should Django use (*)
DJANGO_ASGI_MODULE=cloud_explorer.asgi                            # WSGI module name (*)

echo "Starting $NAME as `whoami`"

export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec gunicorn ${DJANGO_WSGI_MODULE}:application \
  -k uvicorn.workers.UvicornWorker \
  --name $NAME \
  --workers $NUM_WORKERS \
  --timeout $TIMEOUT \
  --user $USER \
  --bind 0.0.0.0:8000 \
  --worker-connections 1001
