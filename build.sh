#!/usr/bin/env bash
# Exit on error
set -o errexit

pip install -r requirements.txt

if [ -f "manage.py" ]; then
    python manage.py migrate
    python manage.py collectstatic --no-input
elif [ -f "Annapurna_liquor/shopadmin_clean/shopadmin/manage.py" ]; then
    python Annapurna_liquor/shopadmin_clean/shopadmin/manage.py migrate
    python Annapurna_liquor/shopadmin_clean/shopadmin/manage.py collectstatic --no-input
fi
