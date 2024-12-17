# goodreads-clone
A back-end clone to goodreads.com platform,which is a huge platform for book readers, authors and reviews,


## commands used:
1. `psql -U goodreads_clone_dev -d goodreads_clone_dev_db -h localhost -W` ==> access the database using psql terminal.

2. `pip3 install psycopg2-binary` ==> the PostgreSQL Driver to allow Django to work with PostgreSQL

3. `pip3 freeze > requirements.txt ` ==> get all required packages

4. `sudo -u postgres psql` ==> open the psql as the superuser postgres

5. `python3 -m venv goodreads_clone_venv` to create a virtual environment
6. `source goodreads_clone_venv/bin/activate` to run this venv
