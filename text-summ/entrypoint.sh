#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z web-db 5432; do
  sleep 0.1
done

echo "PostgreSQL started"

# is an array-like construct of all positional parameters. to accept additional parameters
exec "$@"
