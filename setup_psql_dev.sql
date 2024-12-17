CREATE DATABASE goodreads_clone_dev_db;

CREATE USER goodreads_clone_dev WITH PASSWORD 'Goodreads_clone_dev_pwd123';

GRANT ALL PRIVILEGES ON DATABASE goodreads_clone_dev_db TO goodreads_clone_dev;
