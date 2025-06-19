#!/bin/bash
python3 -m alembic -c src/siasdapi/adapters/db/alembic.ini upgrade head

exec "$@" 