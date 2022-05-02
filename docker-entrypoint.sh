#!/bin/bash

echo "Waiting for MySql to start"
./wait-for-it.sh mysql:3306

echo "Migrating the database"
python manage.py migrate

echo "Starting the server"
python manage.py runserver 0.0.0.0:8000