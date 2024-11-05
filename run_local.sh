#!/usr/bin/env bash
# Exit on error
set -o errexit

# Export the DEBUG variable
export DEBUG=true

# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install -r requirements/local.txt

# Apply any outstanding database migrations
python manage.py migrate

# run server
python manage.py runserver