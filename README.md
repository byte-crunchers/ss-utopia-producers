# Overview:

Welcome to the producers repository, built by Wyatt and Henry.
This repository houses multiple producer files that all (with one exception) write data to a database.
For production, this is a MySQL database, for testing it is an H2 database

For general usage, see the top-level script `fill_db.py`. This script will fill either the MySQL connection or the H2 connection.
To select which connection, use it as an argument e.g. 'python fill_db.py mysql'
This will generate random data and fill the given database.

# Testing:

Use the following script as a guideline for testing:
```bash
python fill_db.py h2
coverage run -m pytest
coverage xml
```
This will generage a coverage.xml file.

## YOU MUST set the H2 environment variable to the h2 jar

