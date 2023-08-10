#!/bin/bash

until PGPASSWORD=password psql -h code-challenge_db -U code-challenge -d code-challenge_dev -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up"

until PGPASSWORD=postgres psql -h code-challenge_db_test -U postgres -d code-challenge_test -c '\q'; do
  >&2 echo "Postgres for test is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres for test is up"

alembic -c /usr/code-challenge/src/migrations/alembic.ini upgrade head
uvicorn --host 0.0.0.0 --port ${PORT} app.main:app --reload
