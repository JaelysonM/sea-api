#!/bin/bash
python3 -m alembic -c src/seaapi/adapters/db/alembic.ini upgrade head

exec "$@" 