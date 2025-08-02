#!/bin/bash

# Move to script directory
cd "$(dirname "$0")"

# Load env vars (optional)
export $(grep -v '^#' .env | xargs)

# Print for debug
echo "DATABASE_URL is: $DATABASE_URL"

# Run Django commands
python manage.py migrate
python manage.py collectstatic --noinput

# Start server
PORT=${PORT:-8000}
gunicorn Web_Base.wsgi:application --bind 0.0.0.0:$PORT
