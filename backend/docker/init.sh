#!/bin/sh

# Function to check if there are any pending migrations
function check_migrations {
    python manage.py makemigrations --check --noinput
    return $?
}

# Function to apply migrations and retry until it succeeds or no changes detected
function apply_migrations {
    python manage.py makemigrations --noinput
    python manage.py migrate --noinput
    while [ $? -ne 0 ]; do
        echo "Retrying migrations..."
        sleep 5
        python manage.py migrate --noinput
    done
}

# Apply migrations
check_migrations
if [ $? -eq 0 ]; then
    echo "No pending migrations found."
else
    echo "Applying migrations..."
    apply_migrations
    ####### GENERATE DUMMY FOR TESTS
    # python manage.py gen-dummy
fi

# Start Django server
python manage.py runserver 0.0.0.0:8000
