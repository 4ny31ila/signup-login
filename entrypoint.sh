#!/bin/sh

# Set the PYTHONPATH to include the project root
export PYTHONPATH=.

# Wait for the database to be ready
echo "Waiting for PostgreSQL..."
while ! pg_isready -h db -p 5432 -q -U "user"; do
  sleep 1
done
echo "PostgreSQL is ready"

# Run database migrations
echo "Initializing the database..."
python src/infrastructure/database/init_db.py

# Start the main application
echo "Starting the application with Gunicorn..."
gunicorn --bind 0.0.0.0:8080 wsgi:app
