#!/bin/sh

# Wait for the database to be ready
echo "Waiting for PostgreSQL..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "PostgreSQL started"

# Run database migrations
echo "Initializing the database..."
python src/infrastructure/database/init_db.py

# Start the main application
echo "Starting the application with Gunicorn..."
gunicorn --bind 0.0.0.0:8080 wsgi:app
