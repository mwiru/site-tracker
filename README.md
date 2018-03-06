# Site-tracker
This series will be follows the development of a web analytics solution called. The goal of this series is to have a working application that will enable users to:

- Register with the application.
- Add sites to their account.
- Install tracking codes on their site(s) to track various events as the events occur.
- View reports on their site(s)’ event activity.

## Technology Stack
- Python
- Flask
- React
- HTML
- BootsrapCSS
- CSS
- PostgreSQL

## Create and activate virtualenv

```
python3.6 -m venv env
source env/bin/activate
```

## Set enviroment variables

Update **app/config** and then run:

```
set FLASK_CONFIG="app.config.DevelopmentConfig"
```

or 

```
set FLASK_CONFIG="app.config.DevelopmentConfig"
```

Set a SECRET_KEY

```
set SECRET_KEY="This-is-it-for-me"
```

## Requirements

```
pip install -r requirements
```

## Create DB

Create psql databases

```
CREATE DATABASE sitetracker_db;
CREATE DATABASE sitetracker_test;
```

## Run the Application

```
python tracking.py
```

Access the application at the address **http://localhost:5000/**

## Testing

```
python test.py
```

## Contribute
Would you like to make **Site-Tracker** a better platform? See CONTRIBUTING.md for the steps to contribute.
