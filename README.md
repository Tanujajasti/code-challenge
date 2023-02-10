[![Python Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# Code Challenge Template

Tech Stack:
 - Database used: SQLite3
 - Server: Python Flask Server
 - Postman: To test the rest API functionalities

Pre-requisites:

    1. Install SQLite3 database
    2. Install Python & pipenv
    3. Install Python packages with `pipenv install`


Project Structure:

    1) ddl
        a) stg_create_table.sql - Staging the data from the txt files
        b) tgt_create_table.sql - Target data with increment values from txt files
        c) create_stats_table.sql - Stats table to store the weather stats
    2) wx_data - Input folder with weather station data files
    3) yld_data - Input folder with yield data files
    4) Pipfile
    5) Pipfile.lock (Auto-generated lock file)
    6) main.db - local SQLite Database file
    7) RESTAPI.postman_collection.json - Postman Collection to test the Rest API 
    8) README.md


Setup Working Application:

    1. Install the required tools and libraries
    2. To launch the virtual environment, run `pipenv shell`
    3. To insert Data, run `python insert_data.py`
    4. To start the API, run `python app.py` which will start the Flask server and integrate with SQLite DB
    5. Import the Postman Collection and run the examples, below are the Sample API requests
        a. http://127.0.0.1:5000/api/weather/stats?year=2014
        b. http://127.0.0.1:5000/api/weather/stats?year=2014&station_id=USC00110338
        c. http://127.0.0.1:5000/api/weather?date=20140101&limit=10
        d. http://127.0.0.1:5000/api/weather?date=20140101&station_id=USC00110338&limit=10


## AWS Future Implementation

- Creating API as a lambda function
- To expose Lambda func as API Gateway and configure, AWS SAM template can be used.
- Data can be stored and accessed from AWS Redshift
    - Also, S3 can be used as a file source and that can be loaded into AWS Redshift through COPY command
- Connection String/creds can be stored in the Secrets Manager for the security
