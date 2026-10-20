#!/bin/bash
# this script is used to boot a Docker container

if [ -z "${RATELIMIT_STORAGE_URI:-}" ]; then
    echo "ERROR: RATELIMIT_STORAGE_URI is required" >&2
    exit 1
fi

while true; do
    flask db upgrade
    if [[ "$?" == "0" ]]; then
        break
    fi
    echo Deploy command failed, retrying in 5 secs...
    sleep 5
done
exec gunicorn -b 0.0.0.0:8000 --access-logfile - --error-logfile - microblog:app