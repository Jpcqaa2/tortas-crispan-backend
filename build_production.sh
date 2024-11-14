#!/usr/bin/env bash
# Exit on error
set -o errexit

# Export the DJANGO_DEBUG variable
export DJANGO_DEBUG=false

# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install -r requirements/production.txt

# Convert static asset files
python manage.py collectstatic --no-input

# Apply any outstanding database migrations
python manage.py migrate

# Translate
python manage.py makemessages -l es
python manage.py makemessages -l us
python manage.py compilemessages 