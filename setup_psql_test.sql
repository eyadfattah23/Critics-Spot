CREATE DATABASE goodreads_clone_test_db;

CREATE USER goodreads_clone_test WITH PASSWORD 'Goodreads_clone_test_pwd123';

GRANT ALL PRIVILEGES ON DATABASE goodreads_clone_test_db TO goodreads_clone_test;
