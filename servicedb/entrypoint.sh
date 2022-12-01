#!/bin/sh

uvicorn app:app --reload --port 8001

exec "$@"
