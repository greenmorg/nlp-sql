#!/bin/sh
echo "Starting database setup..."
./wait-for-it.sh db:5432 --timeout=60 --strict -- python src/db/setup.py
status=$?
if [ $status -ne 0 ]; then
  echo "Database setup failed with status $status"
  exit $status
fi

echo "Starting FastAPI server..."
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
status=$?
if [ $status -ne 0 ]; then
  echo "FastAPI server failed with status $status"
  exit $status
fi
