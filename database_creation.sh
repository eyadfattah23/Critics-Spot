#!/usr/bin/env bash
sudo psql -U postgres -c "CREATE DATABASE goodreads_clone_test_db;"
sudo psql -U postgres -c "CREATE USER goodreads_clone_test WITH PASSWORD 'Goodreads_clone_test_pwd123';"
sudo psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE goodreads_clone_test_db TO goodreads_clone_test;"
sudo psql -U postgres -c "ALTER USER goodreads_clone_test CREATEDB;"

sudo psql -U postgres -c "CREATE DATABASE goodreads_clone_dev_db;"
sudo psql -U postgres -c "CREATE USER goodreads_clone_dev WITH PASSWORD 'Goodreads_clone_dev_pwd123';"
sudo psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE goodreads_clone_dev_db TO goodreads_clone_dev;"
sudo psql -U postgres -c "ALTER USER goodreads_clone_dev CREATEDB;"
