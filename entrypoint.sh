#! /bin/sh
set -e

# Create the database tables
# sqlite3 app.db < schema.sql

# Run the migration script to populate the app_pronunciation table
python migrate_add_pronounciation.py

# Run the migration script to populate the app_unique_index table
python migrate_add_unique_index.py

# Populate the database with vocabulary from words.json
python import_words.py

# Start the Flask application
exec "$@"