#!/usr/bin/env bash
# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install -r requirements/production.txt

# Convert static asset files
python manage.py collectstatic --no-input

# Apply any outstanding database migrations
python manage.py migrate

# Create a default superuser
python3 manage.py create_superuser_script

# Load Initial Data
python manage.py runscript poblar_bd

# Translate
python manage.py makemessages -l es
python manage.py makemessages -l us
python manage.py compilemessages 