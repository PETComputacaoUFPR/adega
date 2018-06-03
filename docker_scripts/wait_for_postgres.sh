#!/bin/bash
# wait-for-postgres.sh

set -e

host="$1"

cmd="$@"

until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up"
#~ >&2 echo "Postgres is up - executing command"
#~ exec $cmd
